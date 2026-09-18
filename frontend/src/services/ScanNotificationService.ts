import { LocalNotifications } from '@capacitor/local-notifications';
import ScanManager from './ScanManager';

export class ScanNotificationService {
  private static timers = new Map<string, ReturnType<typeof setInterval>>();

  static async watch(scanId: string, target: string, intervalMs = 15000): Promise<void> {
    if (this.timers.has(scanId)) return;
    await LocalNotifications.requestPermissions();
    const check = async () => {
      try {
        const response = await ScanManager.getStatus(scanId);
        const raw = response?.status ?? response;
        const status = String(Array.isArray(raw) ? raw[0] : raw?.status ?? raw).toUpperCase();
        if (['FINISHED', 'FAILED', 'ABORTED'].includes(status)) {
          this.unwatch(scanId);
          await LocalNotifications.schedule({ notifications: [{ id: this.numericId(scanId), title: `Sherlock scan ${status.toLowerCase()}`, body: `${target} is ${status.toLowerCase()}. Tap to review the case.`, schedule: { at: new Date(Date.now() + 500) }, extra: { path: `/reports/${scanId}` } }] });
        }
      } catch (error) {
        console.warn('Scan status check failed', error);
      }
    };
    this.timers.set(scanId, setInterval(check, intervalMs));
    await check();
  }

  static unwatch(scanId: string): void {
    const timer = this.timers.get(scanId);
    if (timer) clearInterval(timer);
    this.timers.delete(scanId);
  }

  static numericId(scanId: string): number {
    return [...scanId].reduce((hash, char) => ((hash * 31) + char.charCodeAt(0)) | 0, 7) & 0x7fffffff;
  }
}
