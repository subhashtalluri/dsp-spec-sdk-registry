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


def from_file_catalog(
    source_id: str,
    endpoint: str,
    catalog: List[Dict[str, Any]],
    driver: str = "s3",
) -> Source:
    datasets: List[Dataset] = []

    for item in catalog:
        fields: List[Field] = []
        for f in item["fields"]:
            fields.append(
                Field(
                    name=f["name"],
                    type=f["type"],
                    nullable=f.get("nullable", True),
                    mapping=FieldMapping(physical_path=f["name"]),
                    semantics=FieldSemantics(),
                )
            )

        datasets.append(
            Dataset(
                dataset_id=item["dataset_id"],
                display_name=item.get("display_name"),
                kind="file",
                physical_name=item["path"],
                partitioning=item.get("partitioning"),
                fields=fields,
                semantics=DatasetSemantics(),
                access=DatasetAccess(
                    modes=["read"],
                    file_layout={
                        "path": item["path"],
                        "format": item.get("format", "parquet"),
                    },
                ),
            )
        )

    conn = Connection(
        type="file",
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
