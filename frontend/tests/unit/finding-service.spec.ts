import { describe, expect, it } from 'vitest';
import { FindingService } from '@/services/FindingService';

describe('FindingService', () => {
  it('deduplicates equivalent evidence and keeps newest', () => {
    const result = FindingService.deduplicate([
      { event_type: 'EMAILADDR_COMPROMISED', source_data: 'HIBP', data: 'a@example.com', last_seen: '2025-01-01' },
      { event_type: 'EMAILADDR_COMPROMISED', source_data: 'HIBP', data: 'a@example.com', last_seen: '2026-01-01' },
    ]);
    expect(result).toHaveLength(1); expect(result[0].last_seen).toBe('2026-01-01');
  });
  it('sorts serious findings first and gives action', () => {
    const result = FindingService.deduplicate([{ event_type: 'DOMAIN_NAME' }, { event_type: 'VULNERABILITY' }]);
    expect(result[0].event_type).toBe('VULNERABILITY');
    expect(FindingService.remediation(result[0])).toContain('patch');
  });
});
