import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { sanitizeFileName } from '../dist/security.js';
import { loadGoogleDriveConfigFromEnv } from '../dist/drive-client.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const cli = path.join(__dirname, '..', 'dist', 'cli.js');

test('sanitizeFileName strips traversal and unsafe characters', () => {
  assert.equal(sanitizeFileName('../../../etc/passwd'), 'passwd');
  assert.equal(sanitizeFileName('report:draft?.md'), 'report_draft_.md');
  assert.equal(sanitizeFileName(''), 'untitled');
});

test('loadGoogleDriveConfigFromEnv fails without credentials', () => {
  const saved = {
    GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET,
    GOOGLE_REFRESH_TOKEN: process.env.GOOGLE_REFRESH_TOKEN,
  };
  delete process.env.GOOGLE_CLIENT_ID;
  delete process.env.GOOGLE_CLIENT_SECRET;
  delete process.env.GOOGLE_REFRESH_TOKEN;

  try {
    assert.throws(
      () => loadGoogleDriveConfigFromEnv(),
      /Missing Google Drive credentials/
    );
  } finally {
    for (const [key, value] of Object.entries(saved)) {
      if (value === undefined) delete process.env[key];
      else process.env[key] = value;
    }
  }
});

test('CLI mirror requires folder-id', () => {
  const proc = spawnSync('node', [cli, 'mirror', '--output-dir', '/tmp/out'], {
    encoding: 'utf-8',
  });
  assert.equal(proc.status, 1);
  assert.match(proc.stderr, /folder-id/i);
});

test('CLI mirror rejects missing OAuth env', () => {
  const proc = spawnSync(
    'node',
    [cli, 'mirror', '--folder-id', 'test-folder', '--output-dir', '/tmp/out'],
    {
      encoding: 'utf-8',
      env: {
        PATH: process.env.PATH ?? '',
      },
    }
  );
  assert.equal(proc.status, 1);
  assert.match(proc.stderr, /Missing Google Drive credentials/i);
});
