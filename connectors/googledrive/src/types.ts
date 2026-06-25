export interface GoogleDriveConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  refreshToken: string;
}

export interface DocumentMetadata {
  id: string;
  name: string;
  mimeType: string;
  size: number;
  modifiedTime: string;
  webViewLink: string;
}

export interface MirrorOptions {
  folderId: string;
  outputDir: string;
  mimeTypes?: string[];
  batchSize?: number;
}

export interface MirrorFailure {
  id: string;
  name: string;
  error: string;
}

export interface MirrorResult {
  outputDir: string;
  folderId: string;
  syncedAt: string;
  mirroredCount: number;
  skippedCount: number;
  failedCount: number;
  files: string[];
  skipped: Array<{ id: string; name: string; mimeType: string; reason: string }>;
  failed: MirrorFailure[];
}
