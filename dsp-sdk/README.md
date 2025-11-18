# DSP SDK (Python)

This directory contains the Python SDK for the DSP (Data Source Publication) standard.

The SDK provides:

- Pydantic models for all DSP core objects (`Source`, `Dataset`, `Field`, etc.)
- JSON Schema validation (`dsp-1.0.json`)
- Load/save utilities for manifests
- Profiles to help generate manifests from real systems:
  - `sql`   – introspect relational databases / warehouses
  - `stream`– describe topics/streams using JSON Schemas
  - `api`   – derive datasets from OpenAPI specifications
  - `file`  – describe file-based datasets (for example object storage)
  - `graph` – describe node/edge sets from graph databases

The SDK is domain-independent and does not assume any particular industry.
