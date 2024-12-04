from typing import Any, Dict, List
from pydantic import BaseModel


class ScanResponseDTO(BaseModel):
    target: str
    scanId: str
    status: str
    events: Dict[str, Any]


class ScanListDTO(BaseModel):
    status: int
    events: List[Dict[Any, Any]]


class ScanOptionsDTO(BaseModel):
    scanId: str
    status: int
    options: Dict[str, Any]


class ScanGraphicsDTO(BaseModel):
    scanId: str
    status: int
    graphics: Dict[str, Any]

# Define EventDTO model
class EventDTO(BaseModel):
    event: str
    type: str
    module: str
    last_seen: str

# Define ScanEventsDTO model
class ScanEventsDTO(BaseModel):
    scanId: str
    status: int
    events: List[EventDTO]  # Ensure this is expecting a list of EventDTO instances

class AnalysisDTO(BaseModel):
    scanId: str
    status: int
    response: Dict[str, Any]
    entities: List[Dict[str, str]]
    transformer: Any