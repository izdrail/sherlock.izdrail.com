from pydantic import BaseModel
from typing import List, Optional

from pydantic import BaseModel
from typing import Optional


class PocDTO(BaseModel):
    cve_id: str
    name: str
    owner: str
    full_name: str
    html_url: str
    description: Optional[str] = None
    stargazers_count: int
    nvd_description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    pushed_at: Optional[str] = None

    @classmethod
    def from_sqlite_row(cls, row):
        # Safeguard against type mismatches
        return cls(
            cve_id=str(row[1] or ""),  # Ensure cve_id is a string
            name=str(row[2] or ""),  # Ensure name is a string
            owner=str(row[3] or ""),  # Ensure owner is a string
            full_name=str(row[4] or ""),  # Ensure full_name is a string
            html_url=str(row[5] or ""),  # Ensure html_url is a string
            description=row[6] if isinstance(row[6], str) else None,
            stargazers_count=int(row[7]) if row[7] is not None else 0,  # Default to 0
            nvd_description=row[8] if isinstance(row[8], str) else None,
            created_at=row[9] if isinstance(row[9], str) else None,
            updated_at=row[10] if isinstance(row[10], str) else None,
            pushed_at=row[11] if isinstance(row[11], str) else None,
        )


class PocListDTO(BaseModel):
    pocs: List[PocDTO]


class PocResponseDTO(BaseModel):
    status: int
    data: List[PocDTO]
