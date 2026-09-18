import { beforeEach, describe, expect, it, vi } from 'vitest';

const store = new Map<string, string>();
vi.mock('@capacitor/preferences', () => ({ Preferences: {
  get: vi.fn(async ({ key }: { key: string }) => ({ value: store.get(key) ?? null })),
  set: vi.fn(async ({ key, value }: { key: string; value: string }) => { store.set(key, value); }),
} }));

import { CaseMetadataService } from '@/services/CaseMetadataService';

describe('CaseMetadataService', () => {
  beforeEach(() => store.clear());
  it('stores trimmed labels and notes per scan', async () => {
    const saved = await CaseMetadataService.save('scan-1', ' Client review ', ' Follow up ');
    expect(saved.label).toBe('Client review');
    expect((await CaseMetadataService.get('scan-1')).notes).toBe('Follow up');
  });
  it('removes only the selected scan metadata', async () => {
    await CaseMetadataService.save('one', 'One', '');
    await CaseMetadataService.save('two', 'Two', '');
    await CaseMetadataService.remove('one');
    expect((await CaseMetadataService.get('one')).label).toBe('');
    expect((await CaseMetadataService.get('two')).label).toBe('Two');
  });
  it('recovers from malformed stored data', async () => {
    store.set('sherlock.case-metadata.v1', '{bad json');
    expect(await CaseMetadataService.all()).toEqual({});
  });
});
