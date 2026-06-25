import * as fs from 'fs/promises';
import * as path from 'path';
import { listDocuments } from './list-documents';
import { logger } from './logger';
import { sanitizeFileName } from './security';
import type { DocumentMetadata, MirrorOptions, MirrorResult } from './types';

const MIME_EXPORT: Record<string, { exportMime: string; extension: string }> = {
  'application/vnd.google-apps.document': {
    exportMime: 'text/plain',
    extension: '.md',
  },
  'application/vnd.google-apps.spreadsheet': {
    exportMime: 'text/csv',
    extension: '.csv',
  },
};

const MIME_EXTENSION: Record<string, string> = {
  'text/plain': '.txt',
  'text/markdown': '.md',
  'text/x-markdown': '.md',
  'text/csv': '.csv',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
};

async function fetchDocumentText(drive: any, metadata: DocumentMetadata): Promise<Buffer> {
  const exportSpec = MIME_EXPORT[metadata.mimeType];
  if (exportSpec) {
    const response = await drive.files.export({
      fileId: metadata.id,
      mimeType: exportSpec.exportMime,
    });
    return Buffer.from(String(response.data), 'utf-8');
  }

  const response = await drive.files.get(
    { fileId: metadata.id, alt: 'media' },
    { responseType: 'arraybuffer' }
  );
  return Buffer.from(response.data as ArrayBuffer);
}

function targetFileName(metadata: DocumentMetadata): string {
  const exportSpec = MIME_EXPORT[metadata.mimeType];
  if (exportSpec) {
    const base = metadata.name.replace(/\.[^.]+$/, '');
    return `${base}${exportSpec.extension}`;
  }

  const extension = MIME_EXTENSION[metadata.mimeType];
  if (extension && !metadata.name.toLowerCase().endsWith(extension)) {
    return `${metadata.name}${extension}`;
  }
  return metadata.name;
}

async function uniqueOutputPath(outputDir: string, fileName: string): Promise<string> {
  const safeName = sanitizeFileName(fileName);
  const candidate = path.join(outputDir, safeName);
  if (!path.resolve(candidate).startsWith(path.resolve(outputDir))) {
    throw new Error(`Unsafe output path rejected: ${safeName}`);
  }

  const { name, ext } = path.parse(candidate);
  let counter = 1;
  while (true) {
    const attempt = counter === 1 ? candidate : path.join(outputDir, `${name}-${counter}${ext}`);
    try {
      await fs.access(attempt);
      counter += 1;
    } catch {
      return attempt;
    }
  }
}

export async function syncFolderToMirror(
  drive: any,
  options: MirrorOptions
): Promise<MirrorResult> {
  const { folderId, outputDir } = options;
  const batchSize = options.batchSize ?? 5;
  const mimeTypes = options.mimeTypes;

  await fs.mkdir(outputDir, { recursive: true });

  const documents = await listDocuments(drive, folderId, mimeTypes);
  const files: string[] = [];
  const skipped: MirrorResult['skipped'] = [];
  const failed: MirrorResult['failed'] = [];

  for (let i = 0; i < documents.length; i += batchSize) {
    const batch = documents.slice(i, i + batchSize);
    await Promise.all(
      batch.map(async (metadata) => {
        try {
          const content = await fetchDocumentText(drive, metadata);
          const fileName = targetFileName(metadata);
          const absolutePath = await uniqueOutputPath(outputDir, fileName);
          await fs.writeFile(absolutePath, content);
          files.push(absolutePath);
          logger.info('mirrored document', { name: metadata.name, path: absolutePath });
        } catch (error) {
          failed.push({
            id: metadata.id,
            name: metadata.name,
            error: error instanceof Error ? error.message : String(error),
          });
          logger.error('mirror failed', { id: metadata.id, name: metadata.name });
        }
      })
    );
  }

  const syncedAt = new Date().toISOString();
  const manifest = {
    synced_at: syncedAt,
    folder_id: folderId,
    files,
    skipped,
    failed,
  };
  await fs.writeFile(
    path.join(outputDir, 'mirror-manifest.json'),
    JSON.stringify(manifest, null, 2),
    'utf-8'
  );

  return {
    outputDir,
    folderId,
    syncedAt,
    mirroredCount: files.length,
    skippedCount: skipped.length,
    failedCount: failed.length,
    files,
    skipped,
    failed,
  };
}
