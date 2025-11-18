from __future__ import annotations

from typing import Any, Callable, Dict, List

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


def _field_type_from_json_schema(field_schema: Dict[str, Any]) -> str:
    t = field_schema.get("type", "string")
    if isinstance(t, list):
        t = next((x for x in t if x != "null"), "string")

    if t == "integer":
        return "integer"
    if t == "number":
        return "float"
    if t == "boolean":
        return "boolean"
    if t == "string":
        fmt = field_schema.get("format")
        if fmt == "date-time":
            return "timestamp"
        if fmt == "date":
            return "date"
        return "string"
    if t == "object":
        return "object"
    if t == "array":
        return "array"
    return "json"


def _fields_from_json_schema(schema: Dict[str, Any]) -> List[Field]:
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    fields: List[Field] = []

    for name, prop in properties.items():
        fields.append(
            Field(
                name=name,
                type=_field_type_from_json_schema(prop),
                nullable=name not in required,
                mapping=FieldMapping(physical_path=f"$.{name}"),
                semantics=FieldSemantics(),
            )
        )

    return fields


def from_topics_with_json_schema(
    source_id: str,
    endpoint: str,
    topics: List[str],
    json_schema_lookup: Callable[[str], Dict[str, Any]],
    driver: str = "kafka",
) -> Source:
    datasets: List[Dataset] = []

    for topic in topics:
        schema = json_schema_lookup(topic)
        fields = _fields_from_json_schema(schema)

        datasets.append(
            Dataset(
                dataset_id=topic,
                display_name=topic,
                kind="stream",
                physical_name=topic,
                fields=fields,
                semantics=DatasetSemantics(),
                access=DatasetAccess(
                    modes=["subscribe"],
                    stream={
                        "type": driver,
                        "topic": topic,
                        "value_format": "json",
                    },
                ),
            )
        )

    conn = Connection(
        type="stream",
        driver=driver,
        endpoint=endpoint,
        auth={"method": "external"},
    )

    return Source(
        source_id=source_id,
        display_name=source_id,
        connection=conn,
        datasets=datasets,
    )
