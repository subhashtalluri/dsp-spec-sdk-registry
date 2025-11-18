from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

DatasetKind = Literal[
    "table",
    "view",
    "stream",
    "file",
    "api",
    "graph_nodes",
    "graph_edges",
    "collection",
    "index",
    "log_stream",
    "time_series",
    "kv",
    "document",
    "custom",
]

FieldType = Literal[
    "string",
    "integer",
    "float",
    "decimal",
    "boolean",
    "date",
    "timestamp",
    "json",
    "array",
    "object",
]


class FieldSemantics(BaseModel):
    model_config = ConfigDict(extra="allow")

    business_role: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list)
    unit: Optional[str] = Field(default=None)
    pii: Optional[bool] = None


class FieldMapping(BaseModel):
    model_config = ConfigDict(extra="allow")

    physical_path: Optional[str] = Field(default=None)


class Field(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    type: FieldType
    display_name: Optional[str] = None
    description: Optional[str] = None
    nullable: Optional[bool] = None
    semantics: Optional[FieldSemantics] = None
    mapping: Optional[FieldMapping] = None
    constraints: Dict[str, Any] = Field(default_factory=dict)


class JoinHint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_dataset_id: str
    relationship: Literal["one_to_one", "one_to_many", "many_to_one", "many_to_many"]
    description: Optional[str] = None
    on: List[Dict[str, str]] = Field(
        description='List of {"local_field": "...", "remote_field": "..."} mappings.'
    )


class DatasetSemantics(BaseModel):
    model_config = ConfigDict(extra="allow")

    domain: Optional[str] = None
    entity_type: Optional[str] = None
    grain: Optional[str] = None
    time_columns: Dict[str, str] = Field(default_factory=dict)
    join_hints: List[JoinHint] = Field(default_factory=list)
    business_process: List[str] = Field(default_factory=list)


class DatasetAccess(BaseModel):
    model_config = ConfigDict(extra="allow")

    modes: List[Literal["read", "write", "sample", "subscribe"]] = Field(default_factory=list)
    query_interface: Optional[Dict[str, Any]] = None
    stream: Optional[Dict[str, Any]] = None
    file_layout: Optional[Dict[str, Any]] = None


class Dataset(BaseModel):
    model_config = ConfigDict(extra="allow")

    dataset_id: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    kind: DatasetKind
    physical_name: Optional[str] = None
    primary_key: List[str] = Field(default_factory=list)
    partitioning: Optional[Dict[str, Any]] = None
    dataset_version: Optional[str] = None
    fields: List[Field]
    semantics: Optional[DatasetSemantics] = None
    access: Optional[DatasetAccess] = None
    extra: Dict[str, Any] = Field(default_factory=dict)


class Connection(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str
    driver: Optional[str] = None
    endpoint: Optional[str] = None
    auth: Dict[str, Any] = Field(default_factory=dict)
    default_namespace: Optional[str] = None
    notes: Optional[str] = None


class Source(BaseModel):
    model_config = ConfigDict(extra="allow")

    version: str = Field(default="dsp-1.0")
    source_id: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    labels: List[str] = Field(default_factory=list)
    updated_at: Optional[str] = None
    connection: Connection
    datasets: List[Dataset]
    extra: Dict[str, Any] = Field(default_factory=dict)
