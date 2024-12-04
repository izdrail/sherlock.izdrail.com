import axios from 'axios';

class AlertsService {
  static async getAlerts(): Promise<any> {
    try {
      const response = await axios.get('backend/alerts');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch alerts: ' + error);
    }
  }
}

export default AlertsService;
