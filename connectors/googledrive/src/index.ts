export { createDriveClient, loadGoogleDriveConfigFromEnv } from './drive-client';
export { listDocuments, GLOSSARY_MIRROR_MIME_TYPES } from './list-documents';
export { syncFolderToMirror } from './mirror-sync';
export type {
  DocumentMetadata,
  GoogleDriveConfig,
  MirrorFailure,
  MirrorOptions,
  MirrorResult,
} from './types';

import { createDriveClient } from './drive-client';
import { syncFolderToMirror } from './mirror-sync';
import type { MirrorOptions, MirrorResult } from './types';

export class GoogleDriveMirrorConnector {
  constructor(private readonly drive = createDriveClient()) {}

  syncFolderToMirror(options: MirrorOptions): Promise<MirrorResult> {
    return syncFolderToMirror(this.drive, options);
  }
}

export default GoogleDriveMirrorConnector;
