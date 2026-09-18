import time
from threading import Lock
from typing import Any, Dict, Optional

import requests
from fastapi import HTTPException


class ThreatIntelligenceService:
    """Free, keyless vulnerability intelligence from authoritative public feeds."""

    CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    NVD_CVES_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    EPSS_URL = "https://api.first.org/data/v1/epss"
    TIMEOUT = 20
    CACHE_TTL = 900
    _cache: Dict[str, tuple[float, Any]] = {}
    _lock = Lock()

    @classmethod
    def _get_json(cls, url: str, params: Optional[dict] = None) -> Any:
        key = f"{url}:{sorted((params or {}).items())}"
        now = time.time()
        with cls._lock:
            cached = cls._cache.get(key)
            if cached and now - cached[0] < cls.CACHE_TTL:
                return cached[1]
        try:
            response = requests.get(url, params=params, timeout=cls.TIMEOUT, headers={"Accept": "application/json", "User-Agent": "Sherlock/0.0.1"})
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise HTTPException(status_code=502, detail=f"Threat intelligence provider unavailable: {url}") from exc
        with cls._lock:
            cls._cache[key] = (now, payload)
        return payload

    @classmethod
    def known_exploited(cls, limit: int = 25, query: Optional[str] = None) -> Dict[str, Any]:
        payload = cls._get_json(cls.CISA_KEV_URL)
        records = payload.get("vulnerabilities", [])
        if query:
            needle = query.lower()
            records = [item for item in records if needle in " ".join(str(value) for value in item.values()).lower()]
        records = sorted(records, key=lambda item: item.get("dateAdded", ""), reverse=True)[:limit]
        return {"source": "CISA Known Exploited Vulnerabilities", "source_url": cls.CISA_KEV_URL, "catalog_version": payload.get("catalogVersion"), "count": len(records), "vulnerabilities": records}

    @classmethod
    def recent_cves(cls, limit: int = 20, keyword: Optional[str] = None, start_index: int = 0) -> Dict[str, Any]:
        params: Dict[str, Any] = {"resultsPerPage": limit, "startIndex": start_index}
        if keyword:
            params["keywordSearch"] = keyword
        payload = cls._get_json(cls.NVD_CVES_URL, params)
        return {"source": "NIST National Vulnerability Database", "source_url": cls.NVD_CVES_URL, "total_results": payload.get("totalResults", 0), "start_index": payload.get("startIndex", start_index), "vulnerabilities": payload.get("vulnerabilities", [])}

    @classmethod
    def epss(cls, cve: str) -> Dict[str, Any]:
        normalized = cve.strip().upper()
        if not normalized.startswith("CVE-"):
            raise HTTPException(status_code=422, detail="A CVE identifier is required")
        payload = cls._get_json(cls.EPSS_URL, {"cve": normalized})
        records = payload.get("data", [])
        if not records:
            raise HTTPException(status_code=404, detail=f"No EPSS score found for {normalized}")
        return {"source": "FIRST Exploit Prediction Scoring System", "source_url": cls.EPSS_URL, "result": records[0]}
