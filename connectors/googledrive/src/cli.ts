#!/usr/bin/env node
import * as path from 'path';
import { createDriveClient } from './drive-client';
import { syncFolderToMirror } from './mirror-sync';

function parseArgs(argv: string[]): Record<string, string | boolean> {
  const args: Record<string, string | boolean> = { _: false };
  const positionals: string[] = [];

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === 'mirror') {
      args._ = 'mirror';
      continue;
    }
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
      continue;
    }
    positionals.push(token);
  }

  if (positionals.length > 0 && !args._) {
    args._ = positionals[0];
  }
  return args;
}

async function runMirror(args: Record<string, string | boolean>): Promise<number> {
  const folderId =
    (args['folder-id'] as string | undefined) ?? process.env.GOOGLE_DRIVE_FOLDER_ID ?? '';
  const outputDir = (args['output-dir'] as string | undefined) ?? '';
  const batchSizeRaw = args['batch-size'] as string | undefined;

  if (!folderId) {
    console.error('error: --folder-id or GOOGLE_DRIVE_FOLDER_ID is required');
    return 1;
  }
  if (!outputDir) {
    console.error('error: --output-dir is required');
    return 1;
  }

  const drive = createDriveClient();
  const result = await syncFolderToMirror(drive, {
    folderId,
    outputDir: path.resolve(outputDir),
    batchSize: batchSizeRaw ? parseInt(batchSizeRaw, 10) : undefined,
  });

  console.log(
    JSON.stringify(
      {
        ok: result.failedCount === 0,
        mirroredCount: result.mirroredCount,
        failedCount: result.failedCount,
        outputDir: result.outputDir,
        manifest: path.join(result.outputDir, 'mirror-manifest.json'),
      },
      null,
      2
    )
  );
  return result.failedCount > 0 ? 1 : 0;
}

async function main(): Promise<number> {
  const args = parseArgs(process.argv.slice(2));
  const command = args._;

  if (command === 'mirror') {
    return runMirror(args);
  }

  console.error('usage: term-prep-drive mirror --folder-id ID --output-dir PATH');
  return 1;
}

main()
  .then((code) => {
    process.exitCode = code;
  })
  .catch((error) => {
    console.error('error:', error instanceof Error ? error.message : error);
    process.exitCode = 1;
  });
