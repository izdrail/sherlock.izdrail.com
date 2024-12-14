from typing import Any, Dict, List
import requests
from fastapi import HTTPException

from dto.scans.scan_dtos import ScanEventsDTO
from dto.scans.scan_dtos import EventDTO

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


class BBotService:
    """Configuration for SpiderFoot API endpoints."""
    BASE_URL = "http://localhost:10002"
    START_SCAN = f"{BASE_URL}/startscan"
    SCAN_LIST = f"{BASE_URL}/scanlist"
    SCAN_OPTIONS = f"{BASE_URL}/scanopts?id="
    SCAN_GRAPHICS = f"{BASE_URL}/scanviz?id="
    STOP_SCAN = f"{BASE_URL}/stopscan?id="
    DELETE_SCAN = f"{BASE_URL}/scandelete?id="
    SCAN_EVENTS = f"{BASE_URL}/scanexportjsonmulti?ids="



class SpiderFootService:
    """Service to handle SpiderFoot API interactions."""

    @staticmethod
    def start_scan(target: str, identifier: str) -> Dict[str, Any]:
        post_data = {
            "scanname": identifier,
            "scantarget": target,
            "usecase": "all",
            "modulelist": "",
            "typelist": "",
        }
        response = requests.get(SpiderFootAPI.START_SCAN, params=post_data, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to start scan")
        return response.json()

    @staticmethod 
    def stop_scan(scan_id: str) -> Dict[str, Any]:
        response = requests.get(SpiderFootAPI.STOP_SCAN + scan_id,  headers=HEADERS)
        print(response.status_code)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to stop scan")
        return response.json()

    @staticmethod 
    def delete_scan(scan_id: str) -> Dict[str, Any]:
        response = requests.get(SpiderFootAPI.DELETE_SCAN + scan_id,  headers=HEADERS)
        print(response.status_code)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to delete scan with status code " + str(response.status_code))
        return {success: "SUCCESS", scan_id: scan_id, content: response.content}

    @staticmethod
    def get_scan_list() -> List[Dict[str, Any]]:
        response = requests.get(SpiderFootAPI.SCAN_LIST, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch scan list")
        return response.json()

    @staticmethod
    def get_scan_options(scan_id: str) -> Dict[str, Any]:
        response = requests.get(SpiderFootAPI.SCAN_OPTIONS + scan_id, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch scan options")
        return response.json()

    @staticmethod
    def get_scan_graphics(scan_id: str) -> Dict[str, Any]:
        response = requests.get(SpiderFootAPI.SCAN_GRAPHICS + scan_id, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch scan graphics")
        return response.json()

    @staticmethod
    def get_scan_events(scan_id: str) -> ScanEventsDTO:
        response = requests.get(SpiderFootAPI.SCAN_EVENTS + scan_id, headers=HEADERS)
        print(response.status_code)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch scan events")
        
        return response  # Returns a list of dictionaries