import { Preferences } from '@capacitor/preferences';

export interface CaseMetadata {
  label: string;
  notes: string;
  updatedAt: string;
}

export type CaseMetadataMap = Record<string, CaseMetadata>;

const STORAGE_KEY = 'sherlock.case-metadata.v1';

export class CaseMetadataService {
  static async all(): Promise<CaseMetadataMap> {
    const { value } = await Preferences.get({ key: STORAGE_KEY });
    if (!value) return {};

    try {
      return JSON.parse(value) as CaseMetadataMap;
    } catch {
      return {};
    }
  }

  static async get(scanId: string): Promise<CaseMetadata> {
    const records = await this.all();
    return records[scanId] ?? { label: '', notes: '', updatedAt: '' };
  }

  static async save(scanId: string, label: string, notes: string): Promise<CaseMetadata> {
    const records = await this.all();
    const metadata = { label: label.trim(), notes: notes.trim(), updatedAt: new Date().toISOString() };
    records[scanId] = metadata;
    await Preferences.set({ key: STORAGE_KEY, value: JSON.stringify(records) });
    return metadata;
  }

  static async remove(scanId: string): Promise<void> {
    const records = await this.all();
    delete records[scanId];
    await Preferences.set({ key: STORAGE_KEY, value: JSON.stringify(records) });
  }
}
