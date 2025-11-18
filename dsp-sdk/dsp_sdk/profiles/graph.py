from __future__ import annotations

from typing import Any, Dict, List

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


def from_graph_catalog(
    source_id: str,
    endpoint: str,
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    driver: str = "generic",
) -> Source:
    datasets: List[Dataset] = []

    for node in nodes:
        fields: List[Field] = []
        for p in node.get("properties", []):
            fields.append(
                Field(
                    name=p["name"],
                    type=p["type"],
                    nullable=p.get("nullable", True),
                    mapping=FieldMapping(physical_path=p["name"]),
                    semantics=FieldSemantics(),
                )
            )

        datasets.append(
            Dataset(
                dataset_id=node["dataset_id"],
                display_name=node.get("label"),
                kind="graph_nodes",
                physical_name=node.get("label"),
                fields=fields,
                semantics=DatasetSemantics(
                    entity_type=node.get("label"),
                ),
                access=DatasetAccess(
                    modes=["read"],
                    query_interface={"type": "graph"},
                ),
            )
        )

    for edge in edges:
        fields: List[Field] = []
        for p in edge.get("properties", []):
            fields.append(
                Field(
                    name=p["name"],
                    type=p["type"],
                    nullable=p.get("nullable", True),
                    mapping=FieldMapping(physical_path=p["name"]),
                    semantics=FieldSemantics(),
                )
            )

        datasets.append(
            Dataset(
                dataset_id=edge["dataset_id"],
                display_name=edge.get("type"),
                kind="graph_edges",
                physical_name=edge.get("type"),
                fields=fields,
                semantics=DatasetSemantics(
                    entity_type=edge.get("type"),
                    grain="one row per edge",
                ),
                access=DatasetAccess(
                    modes=["read"],
                    query_interface={"type": "graph"},
                ),
            )
        )

    conn = Connection(
        type="graph",
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
