import axios from 'axios';
export interface BBotScan { id: string; target: string; preset: string; status: string; event_count: number; error?: string }
export class BBotService {
  static async presets(): Promise<string[]> { return (await axios.get('/backend/bbot/presets')).data.presets ?? []; }
  static async scans(): Promise<BBotScan[]> { return (await axios.get('/backend/bbot/scans')).data.scans ?? []; }
  static async start(target: string, preset: string): Promise<BBotScan> { return (await axios.post('/backend/bbot/scans', { target, preset })).data; }
  static async stop(id: string): Promise<BBotScan> { return (await axios.post(`/backend/bbot/scans/${id}/stop`)).data; }
  static async events(id: string): Promise<unknown[]> { return (await axios.get(`/backend/bbot/scans/${id}/events`, { params: { limit: 500 } })).data.events ?? []; }
}
