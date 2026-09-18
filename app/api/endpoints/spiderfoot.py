import json
from typing import Any, Dict

from fastapi import APIRouter, Body, Query, Response
from fastapi_versioning import version

from services.spiderfoot_gateway import SpiderFootGateway

router = APIRouter(prefix="/spiderfoot", tags=["spiderfoot"])


@router.get("/endpoints")
@version(1)
async def endpoint_catalog():
    return {"base_url": SpiderFootGateway.BASE_URL, "endpoints": SpiderFootGateway.catalog()}


def render_upstream(response: Response):
    content_type = response.headers.get("content-type", "application/json").split(";", 1)[0]
    if content_type == "application/json":
        try:
            return response.json()
        except (ValueError, json.JSONDecodeError):
            pass
    return Response(content=response.content, media_type=content_type, headers={"Content-Disposition": response.headers.get("content-disposition", "inline")})


@router.get("/{endpoint}")
@version(1)
async def read_endpoint(endpoint: str, params: str = Query("{}", description="JSON object of SpiderFoot parameters")):
    try:
        values = json.loads(params)
    except json.JSONDecodeError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="params must be a JSON object") from exc
    if not isinstance(values, dict):
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="params must be a JSON object")
    spec = SpiderFootGateway.ENDPOINTS.get(endpoint)
    if not spec or spec.method != "GET":
        from fastapi import HTTPException
        raise HTTPException(status_code=405, detail="Use the documented method from /spiderfoot/endpoints")
    return render_upstream(SpiderFootGateway.invoke(endpoint, values))


@router.post("/{endpoint}")
@version(1)
async def mutate_endpoint(endpoint: str, params: Dict[str, Any] = Body(default_factory=dict)):
    spec = SpiderFootGateway.ENDPOINTS.get(endpoint)
    if not spec or spec.method != "POST":
        from fastapi import HTTPException
        raise HTTPException(status_code=405, detail="Use the documented method from /spiderfoot/endpoints")
    return render_upstream(SpiderFootGateway.invoke(endpoint, params))
