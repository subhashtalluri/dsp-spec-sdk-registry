from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from dsp_sdk import Source, validate_source, DSPValidationError
from .storage import InMemoryStore

app = FastAPI(
    title="DSP Registry",
    description="Reference registry for DSP (Data Source Publication) manifests.",
    version="0.1.0",
)

store = InMemoryStore()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class UpsertResponse(BaseModel):
    source_id: str
    status: str


class ListSourcesResponse(BaseModel):
    sources: List[str]


class SearchResult(BaseModel):
    source_id: str
    dataset_id: str
    field_names: List[str]
    domain: Optional[str] = None


@app.get("/health", tags=["system"])
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.put("/dsp/sources/{source_id}", response_model=UpsertResponse, tags=["sources"])
def put_source(
    source_id: str = Path(..., description="Unique ID of the DSP source."),
    manifest: Dict[str, Any] = None,
) -> UpsertResponse:
    if manifest is None:
        raise HTTPException(status_code=400, detail="Missing manifest body")

    manifest["source_id"] = source_id

    try:
        src = Source.model_validate(manifest)
        validate_source(src)
    except DSPValidationError as exc:
        raise HTTPException(status_code=400, detail=f"Manifest validation failed: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid manifest: {exc}") from exc

    store.upsert(src)
    return UpsertResponse(source_id=source_id, status="ok")


@app.get("/dsp/sources", response_model=ListSourcesResponse, tags=["sources"])
def list_sources() -> ListSourcesResponse:
    ids = [s.source_id for s in store.list()]
    return ListSourcesResponse(sources=ids)


@app.get("/dsp/sources/{source_id}", tags=["sources"])
def get_source(source_id: str = Path(...)) -> Dict[str, Any]:
    src = store.get(source_id)
    if not src:
        raise HTTPException(status_code=404, detail="Source not found")
    return src.model_dump(mode="json")


@app.get("/dsp/search", response_model=List[SearchResult], tags=["search"])
def search(
    dataset_id: Optional[str] = Query(None),
    field_name: Optional[str] = Query(None),
    domain: Optional[str] = Query(None),
) -> List[SearchResult]:
    raw_results = store.search(dataset_id=dataset_id, field_name=field_name, domain=domain)
    return [SearchResult(**r) for r in raw_results]


@app.get("/ui", tags=["ui"])
def ui_index(request: Request):
    sources = store.list()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "sources": sources},
    )


@app.get("/ui/sources/{source_id}", tags=["ui"])
def ui_source_detail(request: Request, source_id: str = Path(...)):
    src = store.get(source_id)
    if not src:
        raise HTTPException(status_code=404, detail="Source not found")

    return templates.TemplateResponse(
        "source.html",
        {"request": request, "source": src},
    )
