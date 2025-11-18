from __future__ import annotations

from typing import Any, Dict, List, Optional

from dsp_sdk.core.models import (
    Connection,
    Dataset,
    DatasetAccess,
    DatasetSemantics,
    Field,
    FieldMapping,
    FieldSemantics,
    Source,
)

from dsp_sdk.profiles.stream import _field_type_from_json_schema, _fields_from_json_schema


def _find_200_json_schema(method_obj: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    responses = method_obj.get("responses", {})
    res_200 = responses.get("200") or responses.get("default")
    if not res_200:
        return None

    content = res_200.get("content", {})
    app_json = content.get("application/json")
    if not app_json:
        return None

    schema = app_json.get("schema")
    return schema


def _dataset_from_path(
    path: str,
    method: str,
    method_obj: Dict[str, Any],
) -> Optional[Dataset]:
    schema = _find_200_json_schema(method_obj)
    if not schema:
        return None

    if schema.get("type") == "array" and "items" in schema:
        item_schema = schema["items"]
        fields = _fields_from_json_schema(item_schema)
        grain = "one row per array item"
    elif schema.get("type") == "object":
        fields = _fields_from_json_schema(schema)
        grain = "one row per response object"
    else:
        return None

    dataset_id = f"{method.upper()} {path}"
    physical_name = dataset_id

    return Dataset(
        dataset_id=dataset_id,
        display_name=dataset_id,
        kind="api",
        physical_name=physical_name,
        fields=fields,
        semantics=DatasetSemantics(grain=grain),
        access=DatasetAccess(
            modes=["read"],
            query_interface={
                "type": "http",
                "method": method.upper(),
                "path_template": path,
            },
        ),
    )


def from_openapi(source_id: str, openapi_spec: Dict[str, Any], server_url: Optional[str] = None) -> Source:
    paths = openapi_spec.get("paths", {})
    servers = openapi_spec.get("servers", [])
    endpoint = server_url or (servers[0]["url"] if servers else "unknown")

    datasets: List[Dataset] = []

    for path, path_item in paths.items():
        for method in ["get"]:
            method_obj = path_item.get(method)
            if not method_obj:
                continue

            ds = _dataset_from_path(path, method, method_obj)
            if ds:
                datasets.append(ds)

    conn = Connection(
        type="api",
        driver="rest",
        endpoint=endpoint,
        auth={"method": "external"},
    )

    return Source(
        source_id=source_id,
        display_name=source_id,
        connection=conn,
        datasets=datasets,
    )
