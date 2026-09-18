import { describe, expect, it } from 'vitest';
import { MobileIntegrationService } from '@/services/MobileIntegrationService';

describe('MobileIntegrationService', () => {
  it('routes custom URL analysis links', () => {
    expect(MobileIntegrationService.destination('sherlock://analyze?url=https%3A%2F%2Fexample.com')).toBe('/assistant/url-checker?url=https%3A%2F%2Fexample.com');
  });
  it('routes Sherlock case links', () => {
    expect(MobileIntegrationService.destination('https://sherlock.izdrail.com/reports/scan-123')).toBe('/reports/scan-123');
  });
  it('rejects unrelated links', () => {
    expect(MobileIntegrationService.destination('https://example.com/reports/scan-123')).toBeNull();
  });
});
