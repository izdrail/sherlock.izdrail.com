export class ReportExportService {
  static json(scanId: string, events: unknown[]): Blob {
    return new Blob([JSON.stringify({ scanId, exportedAt: new Date().toISOString(), events }, null, 2)], { type: 'application/json' });
  }

  static csv(events: Record<string, unknown>[]): Blob {
    const keys = [...new Set(events.flatMap(event => Object.keys(event)))];
    const quote = (value: unknown) => `"${String(value ?? '').replace(/"/g, '""')}"`;
    const rows = [keys.map(quote).join(','), ...events.map(event => keys.map(key => quote(event[key])).join(','))];
    return new Blob([rows.join('\n')], { type: 'text/csv;charset=utf-8' });
  }

  static download(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  }
}
