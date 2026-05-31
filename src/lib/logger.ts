type LogLevel = 'info' | 'warn' | 'error';

interface LogEntry {
  level: LogLevel;
  ts: string;        // ISO timestamp
  msg: string;
  [key: string]: unknown;
}

function log(level: LogLevel, msg: string, data?: Record<string, unknown>): void {
  const entry: LogEntry = { level, ts: new Date().toISOString(), msg, ...data };
  const out = JSON.stringify(entry);
  if (level === 'error') {
    console.error(out);
  } else {
    console.log(out);
  }
}

export const logger = {
  info:  (msg: string, data?: Record<string, unknown>) => log('info',  msg, data),
  warn:  (msg: string, data?: Record<string, unknown>) => log('warn',  msg, data),
  error: (msg: string, data?: Record<string, unknown>) => log('error', msg, data),
};
