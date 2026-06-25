import * as path from 'path';

const MAX_FILENAME_LENGTH = 255;
const UNSAFE_FILENAME_CHARS = /[\\/:*?"<>|]/g;
const PATH_TRAVERSAL_PATTERN = /(?:^|[\\/])\.\.?(?:[\\/]|$)/g;
const MULTIPLE_SEPARATORS = /[\\/]+/g;

function stripControlCharacters(value: string): string {
  let sanitized = '';
  for (const char of value) {
    const codePoint = char.charCodeAt(0);
    if ((codePoint >= 0 && codePoint <= 31) || codePoint === 127) {
      sanitized += ' ';
    } else {
      sanitized += char;
    }
  }
  return sanitized;
}

export function sanitizeFileName(originalName: string): string {
  const normalized = originalName.normalize('NFKC');
  const withoutControlChars = stripControlCharacters(normalized);
  const withoutTraversal = withoutControlChars.replace(PATH_TRAVERSAL_PATTERN, '/');
  const collapsedSeparators = withoutTraversal.replace(MULTIPLE_SEPARATORS, '/');
  const basename = path.basename(collapsedSeparators).trim();
  const safeCharacters = basename.replace(UNSAFE_FILENAME_CHARS, '_');
  const condensedDots = safeCharacters.replace(/\.\.+/g, '.');
  const cleaned = condensedDots.replace(/\s+/g, ' ').trim();
  const fallbackName = cleaned.length > 0 ? cleaned : 'untitled';
  return fallbackName.slice(0, MAX_FILENAME_LENGTH);
}
