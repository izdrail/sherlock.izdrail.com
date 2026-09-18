import { describe, expect, it } from 'vitest';
import { ScanNotificationService } from '@/services/ScanNotificationService';
describe('ScanNotificationService', () => {
  it('creates stable positive Android notification ids', () => {
    const one = ScanNotificationService.numericId('scan-123');
    expect(one).toBeGreaterThanOrEqual(0); expect(ScanNotificationService.numericId('scan-123')).toBe(one);
  });
});
