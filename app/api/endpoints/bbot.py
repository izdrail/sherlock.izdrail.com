from fastapi import APIRouter, Query
from fastapi_versioning import version
from pydantic import BaseModel, Field

from services.bbot_manager import BBotManager

router = APIRouter(prefix="/bbot", tags=["bbot"])


class StartBBotScan(BaseModel):
    target: str = Field(min_length=1, max_length=253)
    preset: str = "subdomain-enum"


@router.get("/presets")
@version(1)
async def presets():
    return {"presets": sorted(BBotManager.ALLOWED_PRESETS)}


@router.post("/scans", status_code=202)
@version(1)
async def start_scan(request: StartBBotScan):
    return await BBotManager.start(request.target, request.preset)


@router.get("/scans")
@version(1)
async def list_scans():
    return {"scans": BBotManager.list()}


@router.get("/scans/{scan_id}")
@version(1)
async def scan_status(scan_id: str):
    return BBotManager.get(scan_id).snapshot()


@router.get("/scans/{scan_id}/events")
@version(1)
async def scan_events(scan_id: str, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500)):
    return BBotManager.events(scan_id, offset, limit)


@router.post("/scans/{scan_id}/stop")
@version(1)
async def stop_scan(scan_id: str):
    return await BBotManager.stop(scan_id)
