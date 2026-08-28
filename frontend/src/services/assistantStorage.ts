export interface ThreatAnalysisRecord {
  id: string;
  timestamp: string;
  scenario: string;
  riskLevel: 'High' | 'Medium' | 'Low' | 'Safe';
  score: number;
  threatTypes: string[];
  analysis: string;
  recommendations: string[];
}

export interface UrlCheckRecord {
  id: string;
  timestamp: string;
  url: string;
  status: 'safe' | 'suspicious' | 'malicious';
  riskScore: number;
  threatsDetected: string[];
  details: string;
  recommendations: string[];
}

export interface PasswordRecord {
  id: string;
  timestamp: string;
  length: number;
  strength: 'weak' | 'medium' | 'strong';
}

export interface ChatMessageItem {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
}

const STORAGE_KEYS = {
  ANALYSES: 'sherlock_threat_analyses',
  URL_CHECKS: 'sherlock_url_checks',
  PASSWORDS: 'sherlock_passwords_history',
  CHAT: 'sherlock_chat_history',
};

export class AssistantStorage {
  private static getItem<T>(key: string, defaultValue: T): T {
    try {
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : defaultValue;
    } catch {
      return defaultValue;
    }
  }

  private static setItem<T>(key: string, value: T): void {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.error('Failed to write to localStorage', e);
    }
  }

  static getAnalyses(): ThreatAnalysisRecord[] {
    return this.getItem<ThreatAnalysisRecord[]>(STORAGE_KEYS.ANALYSES, []);
  }

  static saveAnalysis(record: ThreatAnalysisRecord): void {
    const list = this.getAnalyses();
    list.unshift(record);
    this.setItem(STORAGE_KEYS.ANALYSES, list.slice(0, 50));
  }

  static getUrlChecks(): UrlCheckRecord[] {
    return this.getItem<UrlCheckRecord[]>(STORAGE_KEYS.URL_CHECKS, []);
  }

  static saveUrlCheck(record: UrlCheckRecord): void {
    const list = this.getUrlChecks();
    list.unshift(record);
    this.setItem(STORAGE_KEYS.URL_CHECKS, list.slice(0, 50));
  }

  static getPasswordHistory(): PasswordRecord[] {
    return this.getItem<PasswordRecord[]>(STORAGE_KEYS.PASSWORDS, []);
  }

  static savePasswordRecord(record: PasswordRecord): void {
    const list = this.getPasswordHistory();
    list.unshift(record);
    this.setItem(STORAGE_KEYS.PASSWORDS, list.slice(0, 50));
  }

  static getChatHistory(): ChatMessageItem[] {
    return this.getItem<ChatMessageItem[]>(STORAGE_KEYS.CHAT, []);
  }

  static saveChatMessage(msg: ChatMessageItem): void {
    const history = this.getChatHistory();
    history.push(msg);
    this.setItem(STORAGE_KEYS.CHAT, history.slice(-100));
  }

  static clearChatHistory(): void {
    localStorage.removeItem(STORAGE_KEYS.CHAT);
  }

  static getDashboardStats() {
    const analyses = this.getAnalyses();
    const urlChecks = this.getUrlChecks();
    const passwords = this.getPasswordHistory();

    const highThreats = analyses.filter(a => a.riskLevel === 'High' || a.riskLevel === 'Medium').length;
    const safeUrls = urlChecks.filter(u => u.status === 'safe').length;
    const unsafeUrls = urlChecks.filter(u => u.status !== 'safe').length;
    const strongPasswords = passwords.filter(p => p.strength === 'strong').length;

    return {
      totalAnalyses: analyses.length,
      highThreatsDetected: highThreats,
      totalUrlChecks: urlChecks.length,
      safeUrlsChecked: safeUrls,
      unsafeUrlsChecked: unsafeUrls,
      totalPasswordsGenerated: passwords.length,
      strongPasswordsCount: strongPasswords,
      recentAnalyses: analyses.slice(0, 5),
      recentUrlChecks: urlChecks.slice(0, 5),
    };
  }
}
