import httpx

REGISTRY_BASE = "http://localhost:8080"


async def dsp_list_sources_handler(_input: dict) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{REGISTRY_BASE}/dsp/sources")
        r.raise_for_status()
        return r.json()


async def dsp_get_manifest_handler(tool_input: dict) -> dict:
    source_id = tool_input["source_id"]
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{REGISTRY_BASE}/dsp/sources/{source_id}")
        if r.status_code == 404:
            return {"error": f"Source '{source_id}' not found"}
        r.raise_for_status()
        return r.json()


async def dsp_search_datasets_handler(tool_input: dict) -> dict:
    params = {}
    for key in ("dataset_id", "field_name", "domain"):
        if key in tool_input and tool_input[key]:
            params[key] = tool_input[key]

    async with httpx.AsyncClient() as client:
        r = await client.get(f"{REGISTRY_BASE}/dsp/search", params=params)
        r.raise_for_status()
        return {"results": r.json()}
