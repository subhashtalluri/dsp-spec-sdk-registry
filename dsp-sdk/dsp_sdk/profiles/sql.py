from __future__ import annotations

from typing import Iterable, List, Optional

import sqlalchemy as sa

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


def _map_sql_type(sql_type: sa.types.TypeEngine) -> str:
    t = str(sql_type).lower()
    if any(x in t for x in ["int", "serial", "bigint", "smallint"]):
        return "integer"
    if any(x in t for x in ["decimal", "numeric", "money"]):
        return "decimal"
    if any(x in t for x in ["float", "double", "real"]):
        return "float"
    if "bool" in t:
        return "boolean"
    if "timestamp" in t or ("time" in t and "zone" in t):
        return "timestamp"
    if "date" in t:
        return "date"
    if "json" in t:
        return "json"
    return "string"


def introspect_sql(
    source_id: str,
    engine: sa.Engine,
    schemas: Optional[Iterable[str]] = None,
    include_views: bool = True,
    include_tables: bool = True,
) -> Source:
    inspector = sa.inspect(engine)
    schemas = list(schemas) if schemas is not None else inspector.get_schema_names()

    datasets: List[Dataset] = []

    for schema in schemas:
        table_names = inspector.get_table_names(schema=schema) if include_tables else []
        view_names = inspector.get_view_names(schema=schema) if include_views else []

        for name in table_names + view_names:
            kind = "table" if name in table_names else "view"
            cols = inspector.get_columns(name, schema=schema)
            pk = inspector.get_pk_constraint(name, schema=schema)
            pk_cols = pk.get("constrained_columns", []) if pk else []

            fields: List[Field] = []
            for col in cols:
                col_name = col["name"]
                col_type = col["type"]
                fields.append(
                    Field(
                        name=col_name,
                        type=_map_sql_type(col_type),
                        nullable=col.get("nullable", True),
                        mapping=FieldMapping(physical_path=col_name),
                        semantics=FieldSemantics(
                            business_role="primary_key" if col_name in pk_cols else None
                        ),
                    )
                )

            physical_name = f"{schema}.{name}"

            datasets.append(
                Dataset(
                    dataset_id=physical_name,
                    display_name=name,
                    kind=kind,
                    physical_name=physical_name,
                    primary_key=pk_cols,
                    fields=fields,
                    semantics=DatasetSemantics(),
                    access=DatasetAccess(
                        modes=["read"],
                        query_interface={
                            "type": "sql",
                            "dialect": str(engine.dialect.name),
                            "default_schema": schema,
                        },
                    ),
                )
            )

    conn = Connection(
        type="sql",
        driver=str(engine.dialect.name),
        endpoint=str(engine.url).replace(engine.url.password or "", "****"),
        auth={"method": "external"},
    )

    return Source(
        source_id=source_id,
        display_name=source_id,
        connection=conn,
        datasets=datasets,
    )
