import axios from 'axios';
export interface SpiderFootEndpoint { method: 'GET'|'POST'; parameters: string[]; mutating: boolean }
export class SpiderFootService {
  static async catalog(): Promise<Record<string, SpiderFootEndpoint>> { return (await axios.get('/backend/spiderfoot/endpoints')).data.endpoints ?? {}; }
  static async invoke(name: string, spec: SpiderFootEndpoint, params: Record<string, unknown>): Promise<unknown> {
    return spec.method === 'POST' ? (await axios.post(`/backend/spiderfoot/${name}`, params)).data : (await axios.get(`/backend/spiderfoot/${name}`, { params: { params: JSON.stringify(params) } })).data;
  }
}
