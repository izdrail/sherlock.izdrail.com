import asyncio
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4

from bbot.scanner import Scanner
from fastapi import HTTPException


@dataclass
class ManagedScan:
    id: str
    target: str
    preset: str
    created_at: float = field(default_factory=time.time)
    status: str = "QUEUED"
    error: Optional[str] = None
    scanner: Optional[Scanner] = None
    task: Optional[asyncio.Task] = None
    events: deque = field(default_factory=lambda: deque(maxlen=2000))

    def snapshot(self) -> Dict[str, Any]:
        return {"id": self.id, "target": self.target, "preset": self.preset, "status": self.status, "created_at": self.created_at, "event_count": len(self.events), "error": self.error}


class BBotManager:
    """Process-local manager for bounded BBOT scans."""

    ALLOWED_PRESETS = {"subdomain-enum", "web-basic", "email-enum", "cloud-enum", "code-enum"}
    MAX_CONCURRENT = 2
    _scans: Dict[str, ManagedScan] = {}
    _lock = asyncio.Lock()

    @classmethod
    async def start(cls, target: str, preset: str = "subdomain-enum") -> Dict[str, Any]:
        target = target.strip()
        if not target or len(target) > 253 or any(char.isspace() for char in target):
            raise HTTPException(status_code=422, detail="Target must be a domain, IP address, network, URL, username or email without spaces")
        if preset not in cls.ALLOWED_PRESETS:
            raise HTTPException(status_code=422, detail=f"Unsupported preset. Choose one of: {', '.join(sorted(cls.ALLOWED_PRESETS))}")
        async with cls._lock:
            running = sum(scan.status in {"QUEUED", "STARTING", "RUNNING", "FINISHING"} for scan in cls._scans.values())
            if running >= cls.MAX_CONCURRENT:
                raise HTTPException(status_code=429, detail="Maximum concurrent BBOT scans reached")
            scan_id = str(uuid4())
            managed = ManagedScan(id=scan_id, target=target, preset=preset)
            cls._scans[scan_id] = managed
            managed.task = asyncio.create_task(cls._run(managed))
        return managed.snapshot()

    @classmethod
    async def _run(cls, managed: ManagedScan) -> None:
        try:
            managed.status = "STARTING"
            managed.scanner = Scanner(managed.target, name=f"sherlock-{managed.id[:8]}", presets=[managed.preset])
            async for event in managed.scanner.async_start():
                managed.status = managed.scanner.status
                try:
                    payload = event.json()
                except Exception:
                    payload = {"type": getattr(event, "type", "UNKNOWN"), "data": str(event)}
                managed.events.append(payload)
            managed.status = managed.scanner.status
        except asyncio.CancelledError:
            managed.status = "ABORTED"
            raise
        except Exception as exc:
            managed.status = "FAILED"
            managed.error = str(exc)

    @classmethod
    def list(cls) -> List[Dict[str, Any]]:
        return sorted((scan.snapshot() for scan in cls._scans.values()), key=lambda item: item["created_at"], reverse=True)

    @classmethod
    def get(cls, scan_id: str) -> ManagedScan:
        scan = cls._scans.get(scan_id)
        if not scan:
            raise HTTPException(status_code=404, detail="BBOT scan not found")
        if scan.scanner and scan.status not in {"FAILED", "ABORTED", "FINISHED"}:
            scan.status = scan.scanner.status
        return scan

    @classmethod
    async def stop(cls, scan_id: str) -> Dict[str, Any]:
        scan = cls.get(scan_id)
        if scan.scanner and not scan.scanner.stopped:
            await scan.scanner.async_stop()
            scan.status = scan.scanner.status
        elif scan.task and not scan.task.done():
            scan.task.cancel()
            scan.status = "ABORTED"
        return scan.snapshot()

    @classmethod
    def events(cls, scan_id: str, offset: int = 0, limit: int = 100) -> Dict[str, Any]:
        scan = cls.get(scan_id)
        records = list(scan.events)
        return {"scan": scan.snapshot(), "offset": offset, "count": len(records[offset:offset + limit]), "events": records[offset:offset + limit]}
