import sqlite3
from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_versioning import VersionedFastAPI, version
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from dto.pocs.alerts_dto import PocResponseDTO
from dto.scans.scan_dtos import (
    ScanResponseDTO,
    ScanListDTO,
    ScanOptionsDTO,
    ScanGraphicsDTO,
    ScanEventsDTO,
    AnalysisDTO,
)
from pydantic import BaseModel
import spacy

from services.spider_foot_service import SpiderFootService
from services.poc_service import PocService

# Initialize Router
router = APIRouter()

# Load SpaCy Model
nlp = spacy.load("en_core_web_md")
nlp.max_length = 10000000
# Request Models
class ScanRequest(BaseModel):
    target: str


class CheckScan(BaseModel):
    scanId: str


EXCLUDED_ENTITY_TYPES = {"PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"}


@router.post("/security/scan", response_model=ScanResponseDTO)
@version(1)
async def scan(request: ScanRequest):
    # Start Scan
    result = SpiderFootService.start_scan(request.target)
    # Return Response
    return ScanResponseDTO(
        target=request.target,
        scanId=result[1],
        status=result[0],
        events={"status": result[0], "id": result[1]},
    )


@router.post("/security/scan/stop")
@version(1)
async def scan(request: ScanRequest):
    # Stop Scan
    result = SpiderFootService.stop_scan(request.target)
    # Return Response
    return result.json()




@router.post("/security/scan/delete")
@version(1)
async def scan(request: ScanRequest):
    # Stop Scan
    result = SpiderFootService.delete_scan(request.target)
    # Return Response
    return result.json()




@router.get("/security/scan/list", response_model=ScanListDTO)
@version(1)
async def scan_list():
    result = SpiderFootService.get_scan_list()
    print(result)

    # Map each sublist to a dictionary
    events = [
        {
            "scan_id": item[0],
            "scan_target": item[1],
            "scan_value": item[2],
            "start_time": item[3],
            "end_time": item[4],
            "completion_time": item[5],
            "status": item[6],
            "risk_score": item[7],
            "risk_levels": item[8]
        }
        for item in result
    ]

    return ScanListDTO(
        status=200,
        events=events,
    )



@router.post("/security/scan/options", response_model=ScanOptionsDTO)
@version(1)
async def scan_options(request: CheckScan):
    result = SpiderFootService.get_scan_options(request.scanId)
    return ScanOptionsDTO(
        scanId=request.scanId,
        status=200,
        options=result,
    )


@router.post("/security/scan/graphic", response_model=ScanGraphicsDTO)
@version(1)
async def scan_graphic(request: CheckScan):
    result = SpiderFootService.get_scan_graphics(request.scanId)
    return ScanGraphicsDTO(
        scanId=request.scanId,
        status=200,
        graphics=result,
    )


@router.post("/security/scan/events")
@version(1)
async def scan_events(request: CheckScan):
    result = SpiderFootService.get_scan_events(request.scanId)
    #print(result)
    return {
        "status": 200,
        "events": result.json()
    }


# Updated Endpoint
@router.post("/security/scan/analyze")
@version(1)
async def analyze_scan(request: CheckScan):
    """
    Analyze scan results using spaCy for Named Entity Recognition (NER).
    """
    
    try:
        results = SpiderFootService.get_scan_events(request.scanId)

        for event in results.json():
            print(event)
        
        # Add the "spacy_setfit" pipeline component to the spaCy model, and configure it with SetFit parameters
        doc = nlp(results.text)

        # Return formatted response
        return {
            "status": 200,
            "events": results.json(),
            "doc": doc.ents
        }
    except Exception as e:
        raise HTTPException()


@router.get("/security/pocs", response_model=PocResponseDTO)
@version(1)
async def get_pocs(
        limit: int = 10,
        cve_id: Optional[str] = None,
):
    pocs = PocService.get_pocs(limit=limit, cve_id=cve_id)
    
    serialized_pocs = [poc.model_dump() for poc in pocs]  # Use `.dict()` for Pydantic v1

    return PocResponseDTO(
        status=200,
        data=serialized_pocs
    )


#TODO : Add support for `cve_id`
@router.get("/security/alerts", response_model=PocResponseDTO)
@version(1)
async def get_pocs(
        limit: int = 10,
        cve_id: Optional[str] = None,
):
    pocs = PocService.get_pocs(limit=limit, cve_id=cve_id)
    serialized_pocs = [poc.model_dump() for poc in pocs]  # Use `.dict()` for Pydantic v1

    return PocResponseDTO(
        status=200,
        data=serialized_pocs
    )
