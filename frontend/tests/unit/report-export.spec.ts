import { describe, expect, it } from 'vitest';
import { ReportExportService } from '@/services/ReportExportService';

const readBlob = (blob: Blob) => new Promise<string>((resolve, reject) => {
  const reader = new FileReader();
  reader.onload = () => resolve(String(reader.result));
  reader.onerror = () => reject(reader.error);
  reader.readAsText(blob);
});

describe('ReportExportService', () => {
  it('creates portable JSON with scan id and events', async () => {
    const text = await readBlob(ReportExportService.json('scan-1', [{ type: 'HOST', data: 'example.com' }]));
    expect(JSON.parse(text).scanId).toBe('scan-1');
  });
  it('escapes CSV quotes and commas', async () => {
    const text = await readBlob(ReportExportService.csv([{ type: 'NOTE', data: 'one, "two"' }]));
    expect(text).toContain('"one, ""two"""');
  });
});
