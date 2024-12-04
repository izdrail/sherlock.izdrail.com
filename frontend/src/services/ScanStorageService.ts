import { Preferences } from '@capacitor/preferences';

class ScanStorageService {
    private static storageKey = 'scans';

    static async saveScan(query: string, scanId: string, scanData: any): Promise<void> {
        const currentScans = await this.getAllScans();
        currentScans[scanId] = { query, scanData };
        await Preferences.set({
            key: this.storageKey,
            value: JSON.stringify(currentScans),
        });
    }

    static async getScan(scanId: string): Promise<any | null> {
        const currentScans = await this.getAllScans();
        return currentScans[scanId] || null;
    }

    static async getAllScans(): Promise<{ [key: string]: any }> {
        const { value } = await Preferences.get({ key: this.storageKey });
        return value ? JSON.parse(value) : {};
    }

    static async deleteScan(scanId: string): Promise<void> {
        const currentScans = await this.getAllScans();
        delete currentScans[scanId];
        await Preferences.set({
            key: this.storageKey,
            value: JSON.stringify(currentScans),
        });
    }

    static async clearAllScans(): Promise<void> {
        await Preferences.remove({ key: this.storageKey });
    }

    static async getScanByTarget(query: string): Promise<{ scanId: string; query: string; scanData: any } | null> {
        const allScans = await this.getAllScans();
        return Object.values(allScans).find(scan => scan.query === query) || null;
    }
}

export default ScanStorageService;