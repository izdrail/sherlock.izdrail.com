import axios from 'axios';

export interface KnownExploitedVulnerability {
  cveID: string;
  vendorProject: string;
  product: string;
  vulnerabilityName: string;
  dateAdded: string;
  dueDate: string;
  requiredAction: string;
  knownRansomwareCampaignUse?: string;
}

export class ThreatIntelligenceService {
  static async knownExploited(limit = 50, query = ''): Promise<KnownExploitedVulnerability[]> {
    const { data } = await axios.get('/backend/threat-intel/known-exploited', { params: { limit, query: query || undefined } });
    return data.vulnerabilities ?? [];
  }
}
