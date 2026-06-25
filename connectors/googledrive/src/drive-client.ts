import { google } from 'googleapis';
import { OAuth2Client } from 'google-auth-library';
import type { GoogleDriveConfig } from './types';

const DEFAULT_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob';

export function loadGoogleDriveConfigFromEnv(
  overrides: Partial<GoogleDriveConfig> = {}
): GoogleDriveConfig {
  const clientId = overrides.clientId ?? process.env.GOOGLE_CLIENT_ID ?? '';
  const clientSecret = overrides.clientSecret ?? process.env.GOOGLE_CLIENT_SECRET ?? '';
  const redirectUri =
    overrides.redirectUri ?? process.env.GOOGLE_REDIRECT_URI ?? DEFAULT_REDIRECT_URI;
  const refreshToken = overrides.refreshToken ?? process.env.GOOGLE_REFRESH_TOKEN ?? '';

  const missing = [
    ['GOOGLE_CLIENT_ID', clientId],
    ['GOOGLE_CLIENT_SECRET', clientSecret],
    ['GOOGLE_REFRESH_TOKEN', refreshToken],
  ]
    .filter(([, value]) => !value)
    .map(([name]) => name);

  if (missing.length > 0) {
    throw new Error(
      `Missing Google Drive credentials: ${missing.join(', ')}. ` +
        'Set env vars or pass config to the connector.'
    );
  }

  return { clientId, clientSecret, redirectUri, refreshToken };
}

export function createDriveClient(config?: Partial<GoogleDriveConfig>) {
  const resolved = loadGoogleDriveConfigFromEnv(config);
  const oauth2Client = new OAuth2Client(
    resolved.clientId,
    resolved.clientSecret,
    resolved.redirectUri
  );
  oauth2Client.setCredentials({ refresh_token: resolved.refreshToken });
  return google.drive({ version: 'v3', auth: oauth2Client });
}

export type DriveClient = ReturnType<typeof createDriveClient>;
