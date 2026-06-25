type LogFields = Record<string, unknown>;

function formatFields(fields?: LogFields): string {
  if (!fields || Object.keys(fields).length === 0) {
    return '';
  }
  return ` ${JSON.stringify(fields)}`;
}

export const logger = {
  info(message: string, fields?: LogFields): void {
    console.log(`[googledrive] ${message}${formatFields(fields)}`);
  },
  warn(message: string, fields?: LogFields): void {
    console.warn(`[googledrive] ${message}${formatFields(fields)}`);
  },
  error(message: string, fields?: LogFields): void {
    console.error(`[googledrive] ${message}${formatFields(fields)}`);
  },
};
