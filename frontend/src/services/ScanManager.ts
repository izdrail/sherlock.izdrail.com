import axios from 'axios';
import { Device } from '@capacitor/device';

/**
 * ScanManager
 *
 * @class ScanManager
 * @extends {Vue}
 *
 */
class ScanManager {

  static getDeviceId(): Promise<any> {
    const id = Device.getId();
    return id.identifier;
  }

  static async performScan(target: string): Promise<any> {
    const deviceid = Device.getId();
    const uri = 'backend/scan';  // Proxy path configured in vite.config.js
    const formData = {
      target: target,
      client: (await deviceid).identifier,
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
    const deviceid = Device.getId();
    const uri = 'backend/scan/stop';  // Proxy path configured in vite.config.js
    const formData = {
      scanId: scanID,
      client: (await deviceid).identifier,
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
      client: this.getDeviceId(),
    };
    try {
      const response = await axios.post(uri, formData, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      });
      console.log(response.data);
      return { status: "SUCCESS" };
    } catch (error) {
      throw new Error('Cannot connect to server ' + error + '');
    }
  }

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
  
  static async getClientScans(): Promise<any> {
    // Get the device ID
    const deviceId = await Device.getId();

    // Define the SQL query using the device ID
    const query = `
    SELECT * 
    FROM tbl_scan_instance
    WHERE name LIKE '%${deviceId.identifier}%';
  `;

    // Encode the query and device ID as URL parameters
    const url = `osint/query?query=${encodeURIComponent(query.trim())}`;

    try {
      // Send a GET request to the SQL query endpoint
      const response = await axios.get(url);

      // Return the server's response
      return response.data;

    } catch (error: any) {
      // Throw a meaningful error message
      throw new Error(`Cannot connect to server: ${error.message}`);
    }
  }

}

export default ScanManager;
