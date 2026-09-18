from typing import Any, Optional

from fastapi import APIRouter, Query
from fastapi_versioning import version
from pydantic import BaseModel, Field

from dto.pocs.alerts_dto import PocResponseDTO
from dto.scans.scan_dtos import ScanGraphicsDTO, ScanListDTO, ScanOptionsDTO, ScanResponseDTO
from services.poc_service import PocService
from services.spider_foot_service import SpiderFootService

router = APIRouter()


class StartScanRequest(BaseModel):
    target: str = Field(min_length=1, max_length=2048)
    client: str = Field(min_length=1, max_length=255)
    usecase: str = "all"
    modules: list[str] = []
    event_types: list[str] = []


class ScanIdRequest(BaseModel):
    scanId: str = Field(min_length=1, max_length=128)


def serialize_scan(item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        return item
    fields = ["guid", "seed_target", "name", "started_at", "ended_at", "duration", "status", "risk_score", "risk_levels"]
    return {key: value for key, value in zip(fields, item)}


@router.post("/scan", response_model=ScanResponseDTO)
@version(1)
async def start_scan(request: StartScanRequest):
    result = SpiderFootService.start_scan(request.target, request.client, request.usecase, ",".join(request.modules), ",".join(request.event_types))
    status, scan_id = result[0], result[1]
    return ScanResponseDTO(target=request.target, identifier=request.client, scanId=scan_id, status=status, events={"status": status, "id": scan_id})


@router.post("/scan/stop")
@version(1)
async def stop_scan(request: ScanIdRequest):
    return SpiderFootService.stop_scan(request.scanId)


@router.post("/scan/delete")
@version(1)
async def delete_scan(request: ScanIdRequest):
    return SpiderFootService.delete_scan(request.scanId)


@router.post("/scan/rerun")
@version(1)
async def rerun_scan(request: ScanIdRequest):
    return SpiderFootService.rerun_scan(request.scanId)


@router.get("/scan/list", response_model=ScanListDTO)
@version(1)
async def scan_list(client: Optional[str] = Query(None, max_length=255)):
    events = [serialize_scan(item) for item in SpiderFootService.get_scan_list()]
    if client:
        events = [item for item in events if client in str(item.get("name", ""))]
    return ScanListDTO(status=200, events=events)


@router.get("/scan/{scan_id}/status")
@version(1)
async def scan_status(scan_id: str):
    return {"scanId": scan_id, "status": SpiderFootService.get_scan_status(scan_id)}


@router.post("/scan/options", response_model=ScanOptionsDTO)
@version(1)
async def scan_options(request: ScanIdRequest):
    return ScanOptionsDTO(scanId=request.scanId, status=200, options=SpiderFootService.get_scan_options(request.scanId))


@router.post("/scan/graphic", response_model=ScanGraphicsDTO)
@version(1)
async def scan_graphic(request: ScanIdRequest):
    return ScanGraphicsDTO(scanId=request.scanId, status=200, graphics=SpiderFootService.get_scan_graphics(request.scanId))


@router.post("/scan/events")
@version(1)
async def scan_events(request: ScanIdRequest):
    return {"status": 200, "events": SpiderFootService.get_scan_events(request.scanId)}


@router.get("/pocs", response_model=PocResponseDTO)
@version(1)
async def get_pocs(limit: int = 10, cve_id: Optional[str] = None):
    return PocResponseDTO(status=200, data=[poc.model_dump() for poc in PocService.get_pocs(limit=limit, cve_id=cve_id)])


@router.get("/alerts", response_model=PocResponseDTO)
@version(1)
async def get_alerts(limit: int = 10, cve_id: Optional[str] = None):
    return await get_pocs(limit, cve_id)
