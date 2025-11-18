# DSP Specification (`dsp-1.0`)

This directory contains the core DSP JSON Schema:

- `specs/dsp-1.0.json`

A **DSP manifest** is a JSON document that describes:

- A **source** – a system that contains data.
- One or more **datasets** – logical datasets (tables, views, topics, APIs, files, node sets, etc.).
- **Fields** – attributes/columns/properties within each dataset.
- Optional **semantics** – domain, entity type, grain, relationships.
- Optional **access** metadata – how to read or subscribe to the dataset.

The schema is intentionally generic and **does not assume any specific domain**.
It is suitable for relational databases, warehouses, streams, APIs, NoSQL, files,
search engines, logs, metrics, graphs, and more.

## Validation

Use any JSON Schema validator that supports draft 2020-12:

```bash
pip install jsonschema
jsonschema -i your_manifest.json specs/dsp-1.0.json
```
