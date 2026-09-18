from typing import Optional

from fastapi import APIRouter, Query
from fastapi_versioning import version

from services.threat_intelligence_service import ThreatIntelligenceService

router = APIRouter(prefix="/threat-intel", tags=["threat-intelligence"])


@router.get("/known-exploited")
@version(1)
async def known_exploited(limit: int = Query(25, ge=1, le=200), query: Optional[str] = Query(None, max_length=200)):
    return ThreatIntelligenceService.known_exploited(limit=limit, query=query)


@router.get("/cves")
@version(1)
async def recent_cves(limit: int = Query(20, ge=1, le=100), keyword: Optional[str] = Query(None, max_length=200), start_index: int = Query(0, ge=0)):
    return ThreatIntelligenceService.recent_cves(limit=limit, keyword=keyword, start_index=start_index)


@router.get("/epss/{cve_id}")
@version(1)
async def epss_score(cve_id: str):
    return ThreatIntelligenceService.epss(cve_id)
