import os
from dataclasses import dataclass
from typing import Any, Dict, FrozenSet

import requests
from fastapi import HTTPException


@dataclass(frozen=True)
class EndpointSpec:
    method: str
    params: FrozenSet[str]
    mutating: bool = False


class SpiderFootGateway:
    """Validated access to SpiderFoot's supported web API without arbitrary URL or SQL proxying."""

    BASE_URL = os.getenv("SPIDERFOOT_URL", "http://localhost:10002").rstrip("/")
    TIMEOUT = float(os.getenv("SPIDERFOOT_TIMEOUT", "30"))
    ENDPOINTS: Dict[str, EndpointSpec] = {
        "ping": EndpointSpec("GET", frozenset()),
        "eventtypes": EndpointSpec("GET", frozenset()),
        "modules": EndpointSpec("GET", frozenset()),
        "correlationrules": EndpointSpec("GET", frozenset()),
        "scanlist": EndpointSpec("GET", frozenset()),
        "scanstatus": EndpointSpec("GET", frozenset({"id"})),
        "scanopts": EndpointSpec("GET", frozenset({"id"})),
        "scanlog": EndpointSpec("GET", frozenset({"id", "limit", "rowId", "reverse"})),
        "scanerrors": EndpointSpec("GET", frozenset({"id", "limit"})),
        "scansummary": EndpointSpec("GET", frozenset({"id", "by"})),
        "scancorrelations": EndpointSpec("GET", frozenset({"id"})),
        "scaneventresults": EndpointSpec("GET", frozenset({"id", "eventType", "filterfp", "correlationId"})),
        "scaneventresultsunique": EndpointSpec("GET", frozenset({"id", "eventType", "filterfp"})),
        "search": EndpointSpec("GET", frozenset({"id", "eventType", "value"})),
        "scanhistory": EndpointSpec("GET", frozenset({"id"})),
        "scanelementtypediscovery": EndpointSpec("GET", frozenset({"id", "eventType"})),
        "scanviz": EndpointSpec("GET", frozenset({"id", "gexf"})),
        "scanvizmulti": EndpointSpec("GET", frozenset({"ids", "gexf"})),
        "scanexportjsonmulti": EndpointSpec("GET", frozenset({"ids"})),
        "scanexportlogs": EndpointSpec("GET", frozenset({"id", "dialect"})),
        "scancorrelationsexport": EndpointSpec("GET", frozenset({"id", "filetype", "dialect"})),
        "scaneventresultexport": EndpointSpec("GET", frozenset({"id", "type", "filetype", "dialect"})),
        "scaneventresultexportmulti": EndpointSpec("GET", frozenset({"ids", "filetype", "dialect"})),
        "scansearchresultexport": EndpointSpec("GET", frozenset({"id", "eventType", "value", "filetype", "dialect"})),
        "startscan": EndpointSpec("POST", frozenset({"scanname", "scantarget", "modulelist", "typelist", "usecase"}), True),
        "stopscan": EndpointSpec("POST", frozenset({"id"}), True),
        "scandelete": EndpointSpec("POST", frozenset({"id"}), True),
        "rerunscan": EndpointSpec("POST", frozenset({"id"}), True),
        "rerunscanmulti": EndpointSpec("POST", frozenset({"ids"}), True),
        "clonescan": EndpointSpec("POST", frozenset({"id"}), True),
        "resultsetfp": EndpointSpec("POST", frozenset({"id", "resultids", "fp"}), True),
    }

    @classmethod
    def catalog(cls) -> Dict[str, Any]:
        return {name: {"method": spec.method, "parameters": sorted(spec.params), "mutating": spec.mutating} for name, spec in sorted(cls.ENDPOINTS.items())}

    @classmethod
    def invoke(cls, endpoint: str, params: Dict[str, Any]) -> requests.Response:
        spec = cls.ENDPOINTS.get(endpoint)
        if not spec:
            raise HTTPException(status_code=404, detail="Unsupported SpiderFoot endpoint")
        unknown = set(params) - spec.params
        if unknown:
            raise HTTPException(status_code=422, detail=f"Unsupported parameters for {endpoint}: {', '.join(sorted(unknown))}")
        clean = {key: value for key, value in params.items() if value is not None}
        try:
            if spec.method == "POST":
                response = requests.post(f"{cls.BASE_URL}/{endpoint}", data=clean, timeout=cls.TIMEOUT)
            else:
                response = requests.get(f"{cls.BASE_URL}/{endpoint}", params=clean, timeout=cls.TIMEOUT)
        except requests.RequestException as exc:
            raise HTTPException(status_code=502, detail="SpiderFoot is unavailable") from exc
        if not response.ok:
            detail = response.text[:500] or f"SpiderFoot returned HTTP {response.status_code}"
            raise HTTPException(status_code=response.status_code, detail=detail)
        return response
