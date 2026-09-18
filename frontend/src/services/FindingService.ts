export interface Finding { event_type?: string; source_data?: string; data?: unknown; last_seen?: string; confidence?: number }

export class FindingService {
  static deduplicate(findings: Finding[]): Finding[] {
    const seen = new Map<string, Finding>();
    for (const finding of findings) {
      const key = [finding.event_type, finding.source_data, JSON.stringify(finding.data)].join('|');
      const existing = seen.get(key);
      if (!existing || String(finding.last_seen ?? '') > String(existing.last_seen ?? '')) seen.set(key, finding);
    }
    return [...seen.values()].sort((a, b) => this.score(b) - this.score(a));
  }

  static score(finding: Finding): number {
    const type = String(finding.event_type ?? '').toUpperCase();
    if (/COMPROMISED|VULNERABILITY|MALICIOUS|LEAK|BREACH/.test(type)) return 90;
    if (/OPEN_PORT|ACCOUNT_EXTERNAL|AFFILIATE|EMAILADDR|PHONE_NUMBER/.test(type)) return 60;
    return 25;
  }

  static severity(finding: Finding): 'critical' | 'high' | 'medium' | 'low' {
    const score = this.score(finding);
    return score >= 90 ? 'critical' : score >= 70 ? 'high' : score >= 50 ? 'medium' : 'low';
  }

  static remediation(finding: Finding): string {
    const type = String(finding.event_type ?? '').toUpperCase();
    if (type.includes('COMPROMISED') || type.includes('BREACH')) return 'Reset the affected credential, enable MFA, and check for reused passwords.';
    if (type.includes('VULNERABILITY')) return 'Confirm the affected version, patch it, and verify the exposure is no longer reachable.';
    if (type.includes('OPEN_PORT')) return 'Confirm the service is required, restrict network access, and update the service.';
    if (type.includes('ACCOUNT_EXTERNAL')) return 'Confirm the account belongs to the subject and review its privacy and recovery settings.';
    return 'Verify the evidence and document whether it needs action.';
  }
}
