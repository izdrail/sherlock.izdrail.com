import { describe, it, expect, beforeEach } from 'vitest';
import { AssistantStorage } from '@/services/assistantStorage';
import { AssistantService } from '@/services/assistantService';

describe('Assistant Storage & Services', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should save and retrieve threat analyses', () => {
    expect(AssistantStorage.getAnalyses().length).toBe(0);

    const record = {
      id: 'test_1',
      timestamp: new Date().toISOString(),
      scenario: 'Test phishing scenario',
      riskLevel: 'High' as const,
      score: 85,
      threatTypes: ['Phishing'],
      analysis: 'Test analysis',
      recommendations: ['Do not click links'],
    };

    AssistantStorage.saveAnalysis(record);
    const list = AssistantStorage.getAnalyses();
    expect(list.length).toBe(1);
    expect(list[0].scenario).toBe('Test phishing scenario');
  });

  it('should save and retrieve URL checks', () => {
    const urlRecord = {
      id: 'url_1',
      timestamp: new Date().toISOString(),
      url: 'http://malicious-login-phish.com',
      status: 'malicious' as const,
      riskScore: 90,
      threatsDetected: ['Phishing Keyword'],
      details: 'High risk',
      recommendations: ['Avoid site'],
    };

    AssistantStorage.saveUrlCheck(urlRecord);
    const list = AssistantStorage.getUrlChecks();
    expect(list.length).toBe(1);
    expect(list[0].url).toBe('http://malicious-login-phish.com');
  });

  it('should generate correct dashboard statistics', () => {
    AssistantStorage.saveAnalysis({
      id: '1',
      timestamp: new Date().toISOString(),
      scenario: 'Threat 1',
      riskLevel: 'High',
      score: 80,
      threatTypes: [],
      analysis: '',
      recommendations: [],
    });

    AssistantStorage.saveUrlCheck({
      id: 'u1',
      timestamp: new Date().toISOString(),
      url: 'https://safe-site.com',
      status: 'safe',
      riskScore: 5,
      threatsDetected: [],
      details: '',
      recommendations: [],
    });

    AssistantStorage.savePasswordRecord({
      id: 'p1',
      timestamp: new Date().toISOString(),
      length: 16,
      strength: 'strong',
    });

    const stats = AssistantStorage.getDashboardStats();
    expect(stats.totalAnalyses).toBe(1);
    expect(stats.highThreatsDetected).toBe(1);
    expect(stats.safeUrlsChecked).toBe(1);
    expect(stats.strongPasswordsCount).toBe(1);
  });

  it('should fall back gracefully in AssistantService if network is unavailable', async () => {
    const res = await AssistantService.analyzeThreat('urgent wire transfer request click link download invoice.exe');
    expect(res.riskLevel).toBe('High');
    expect(res.score).toBeGreaterThanOrEqual(70);

    const chatRes = await AssistantService.sendChatMessage('Tell me about phishing');
    expect(chatRes.reply.length).toBeGreaterThan(10);

    const urlRes = await AssistantService.checkUrl('http://paypal-login-verify.com');
    expect(urlRes.status).toBe('malicious');
  });
});
