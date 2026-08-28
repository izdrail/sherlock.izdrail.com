import axios from 'axios';
import { AssistantStorage, ThreatAnalysisRecord, UrlCheckRecord } from './assistantStorage';

const API_BASE_URL = 'http://localhost:10001/v1_0';

export class AssistantService {
  static async analyzeThreat(scenario: string): Promise<ThreatAnalysisRecord> {
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, { scenario });
      const record: ThreatAnalysisRecord = {
        id: 'analysis_' + Date.now(),
        timestamp: new Date().toISOString(),
        scenario,
        riskLevel: response.data.risk_level,
        score: response.data.score,
        threatTypes: response.data.threat_types,
        analysis: response.data.analysis,
        recommendations: response.data.recommendations,
      };
      AssistantStorage.saveAnalysis(record);
      return record;
    } catch (e) {
      // Fallback local heuristic analysis if API server is not running
      const text = scenario.toLowerCase();
      let score = 10;
      const threatTypes: string[] = [];

      if (text.includes('urgent') || text.includes('urgency') || text.includes('bank') || text.includes('wire') || text.includes('gift card')) {
        score += 35;
        threatTypes.push('Social Engineering / Urgency Tactic');
      }
      if (text.includes('click') || text.includes('http') || text.includes('login') || text.includes('password') || text.includes('link')) {
        score += 30;
        threatTypes.push('Phishing Attempt');
      }
      if (text.includes('attachment') || text.includes('.exe') || text.includes('zip') || text.includes('download')) {
        score += 25;
        threatTypes.push('Malware Risk');
      }

      score = Math.min(score, 95);
      const riskLevel: 'High' | 'Medium' | 'Low' | 'Safe' =
        score >= 70 ? 'High' : score >= 40 ? 'Medium' : score >= 20 ? 'Low' : 'Safe';

      const fallbackRecord: ThreatAnalysisRecord = {
        id: 'analysis_' + Date.now(),
        timestamp: new Date().toISOString(),
        scenario,
        riskLevel,
        score,
        threatTypes: threatTypes.length > 0 ? threatTypes : ['General Security Assessment'],
        analysis: `Evaluated threat level as ${riskLevel}. Please exercise extreme caution with unsolicited requests or credential forms.`,
        recommendations: [
          'Verify sender identity via trusted communication channels.',
          'Never share passwords, PINs, or sensitive credentials.',
          'Do not open suspicious attachments or click unverified links.',
        ],
      };
      AssistantStorage.saveAnalysis(fallbackRecord);
      return fallbackRecord;
    }
  }

  static async sendChatMessage(message: string, conversationId?: string): Promise<{ reply: string; conversationId: string; suggestions: string[] }> {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message,
        conversation_id: conversationId,
      });
      return {
        reply: response.data.reply,
        conversationId: response.data.conversation_id,
        suggestions: response.data.suggestions || [],
      };
    } catch (e) {
      // Fallback response generator
      const msgLower = message.toLowerCase();
      let reply = 'Always practice caution when dealing with unsolicited emails, suspicious messages, or unknown links.';
      let suggestions = ['Is this email a scam?', 'How to report phishing?', 'Password security tips'];

      if (msgLower.includes('phishing') || msgLower.includes('scam') || msgLower.includes('email')) {
        reply = 'Phishing is a cyber attack where attackers pretend to be trusted entities to steal credentials or money. Look out for fake domains, urgent language, and unexpected attachments.';
        suggestions = ['How to spot fake links?', 'What if I clicked a phishing link?', 'Report phishing'];
      } else if (msgLower.includes('password') || msgLower.includes('passphrase')) {
        reply = 'A strong password should be at least 14 characters, combining letters, numbers, and symbols. Avoid reuse and use a password manager.';
        suggestions = ['Generate a strong password', 'What is 2FA?', 'Are password managers safe?'];
      }

      return {
        reply,
        conversationId: conversationId || 'conv_' + Date.now(),
        suggestions,
      };
    }
  }

  static async checkUrl(url: string): Promise<UrlCheckRecord> {
    try {
      const response = await axios.post(`${API_BASE_URL}/url-check`, { url });
      const record: UrlCheckRecord = {
        id: 'url_' + Date.now(),
        timestamp: new Date().toISOString(),
        url,
        status: response.data.status,
        riskScore: response.data.risk_score,
        threatsDetected: response.data.threats_detected,
        details: response.data.details,
        recommendations: response.data.recommendations,
      };
      AssistantStorage.saveUrlCheck(record);
      return record;
    } catch (e) {
      // Local fallback heuristic
      const urlLower = url.toLowerCase();
      let riskScore = 10;
      const threatsDetected: string[] = [];

      if (urlLower.includes('login') || urlLower.includes('verify') || urlLower.includes('paypal') || urlLower.includes('bank')) {
        riskScore += 40;
        threatsDetected.push('Phishing Keyword Match');
      }
      if (!urlLower.startsWith('https://')) {
        riskScore += 20;
        threatsDetected.push('Unencrypted HTTP connection');
      }
      if (urlLower.includes('bit.ly') || urlLower.includes('tinyurl')) {
        riskScore += 25;
        threatsDetected.push('Shortened / Obfuscated Link');
      }

      riskScore = Math.min(riskScore, 95);
      const status: 'safe' | 'suspicious' | 'malicious' =
        riskScore >= 60 ? 'malicious' : riskScore >= 30 ? 'suspicious' : 'safe';

      const fallbackRecord: UrlCheckRecord = {
        id: 'url_' + Date.now(),
        timestamp: new Date().toISOString(),
        url,
        status,
        riskScore,
        threatsDetected: threatsDetected.length > 0 ? threatsDetected : ['No immediate threat detected'],
        details: `URL analyzed locally. Safety status evaluated as ${status.toUpperCase()}.`,
        recommendations: [
          'Verify the complete domain name before typing credentials.',
          'Ensure HTTPS is active and security certificate is valid.',
        ],
      };
      AssistantStorage.saveUrlCheck(fallbackRecord);
      return fallbackRecord;
    }
  }
}
