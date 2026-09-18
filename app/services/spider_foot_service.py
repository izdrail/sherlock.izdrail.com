import os
from typing import Any, Dict, List

import requests
from fastapi import HTTPException

HEADERS = {"Accept": "application/json"}


class SpiderFootAPI:
    BASE_URL = os.getenv("SPIDERFOOT_URL", "http://localhost:10002").rstrip("/")
    TIMEOUT = float(os.getenv("SPIDERFOOT_TIMEOUT", "30"))


class SpiderFootService:
    @staticmethod
    def _request(path: str, params: Dict[str, Any] | None = None) -> Any:
        try:
            response = requests.get(f"{SpiderFootAPI.BASE_URL}/{path}", params=params, headers=HEADERS, timeout=SpiderFootAPI.TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            status = getattr(exc.response, "status_code", 502)
            detail = getattr(exc.response, "text", "")[:500] or "SpiderFoot is unavailable"
            raise HTTPException(status_code=status, detail=detail) from exc
        try:
            return response.json()
        except ValueError:
            return {"status": "SUCCESS", "content": response.text}

    @classmethod
    def start_scan(cls, target: str, identifier: str, usecase: str = "all", modules: str = "", types: str = "") -> Any:
        return cls._request("startscan", {"scanname": identifier, "scantarget": target, "usecase": usecase, "modulelist": modules, "typelist": types})

    @classmethod
    def stop_scan(cls, scan_id: str) -> Any:
        return cls._request("stopscan", {"id": scan_id})

    @classmethod
    def delete_scan(cls, scan_id: str) -> Any:
        result = cls._request("scandelete", {"id": scan_id})
        return {"status": "SUCCESS", "scan_id": scan_id, "result": result}

    @classmethod
    def rerun_scan(cls, scan_id: str) -> Any:
        return cls._request("rerunscan", {"id": scan_id})

    @classmethod
    def get_scan_list(cls) -> List[Any]:
        return cls._request("scanlist")

    @classmethod
    def get_scan_options(cls, scan_id: str) -> Dict[str, Any]:
        return cls._request("scanopts", {"id": scan_id})

    @classmethod
    def get_scan_graphics(cls, scan_id: str) -> Dict[str, Any]:
        return cls._request("scanviz", {"id": scan_id})

    @classmethod
    def get_scan_events(cls, scan_id: str) -> Any:
        return cls._request("scanexportjsonmulti", {"ids": scan_id})

    @classmethod
    def get_scan_status(cls, scan_id: str) -> Any:
        return cls._request("scanstatus", {"id": scan_id})
