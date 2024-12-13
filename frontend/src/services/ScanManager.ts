import axios from 'axios';
import { Device } from '@capacitor/device';

class ScanManager {

  static async performScan(target: string): Promise<any> {
    const id = await Device.getId();
    const uri = 'backend/scan';  // Proxy path configured in vite.config.js
    const formData = {
      target: target,
      client: id.identifier
    };
    try {
      const response = await axios.post(uri, formData, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      });
      return {
        success: response.data["status"],
        scanID: response.data["scanId"],
        target: target,
      };
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }


  static async stopScan(scanID: string): Promise<any> {
    const uri = 'backend/scan/stop';  // Proxy path configured in vite.config.js
    const formData = {
      scanId: scanID,
    };
    try {
      const response = await axios.post(uri, formData, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      });
      return {
        success: response.data["status"],
        scanID: response.data["scanId"],
        target: response.data["target"],
      };
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }

  static async deleteScan(scanID: string): Promise<any> {
    const uri = 'backend/scan/delete';  // Proxy path configured in vite.config.js
    const formData = {
      target: scanID,
    };
    try {
      const response = await axios.post(uri, formData, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      });
      console.log(response.data);
      return {status:"SUCCESS"};
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }
  // Get results for a specific scan using GET request
  static async getResults(scanID: string): Promise<any> {
    const url = `osint/scanexportjsonmulti?ids=${scanID}`;
    try {
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }

  static async getStatus(scanID: string): Promise<any> {
    const url = `osint/scanstatus?id=${scanID}`;
    try {
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }

  static async getLogs(scanID: string): Promise<any> {
    const url = `osint/scanstatus?id=${scanID}`;
    try {
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }

  static async getAll(): Promise<any> {
    const url = `/backend/scan/list`;
    try {
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }

  static async getEvents(scanID: string): Promise<any> {
    const url = `/backend/scan/events`;
    const data = {
      scanId: scanID,
    };
    try {
      const response = await axios.post(url, data);
      return response.data;
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }
}

export default ScanManager;
