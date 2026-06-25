import { logger } from './logger';
import { sanitizeFileName } from './security';
import type { DocumentMetadata } from './types';

export const GLOSSARY_MIRROR_MIME_TYPES = [
  'application/vnd.google-apps.document',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain',
  'text/csv',
  'text/markdown',
  'text/x-markdown',
];

export async function listDocuments(
  drive: any,
  folderId?: string,
  mimeTypes: string[] = GLOSSARY_MIRROR_MIME_TYPES
): Promise<DocumentMetadata[]> {
  const query = [folderId ? `'${folderId}' in parents` : null, 'trashed = false']
    .filter(Boolean)
    .join(' and ');

  logger.info('listing documents', { folderId, mimeTypes });

  const response = await drive.files.list({
    q: query,
    fields: 'files(id,name,mimeType,size,modifiedTime,webViewLink)',
    orderBy: 'modifiedTime desc',
    pageSize: 100,
  });

  const documents: DocumentMetadata[] = (response.data.files ?? [])
    .map((file: any) => ({
      id: file.id,
      name: sanitizeFileName(file.name || ''),
      mimeType: file.mimeType,
      size: parseInt(file.size || '0', 10),
      modifiedTime: file.modifiedTime,
      webViewLink: file.webViewLink,
    }))
    .filter((doc: DocumentMetadata) => mimeTypes.includes(doc.mimeType));

  logger.info('documents listed', { count: documents.length });
  return documents;
}
