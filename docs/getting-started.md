# Getting Started

This guide walks you through:

1. Creating a DSP manifest
2. Validating it against the DSP schema
3. Storing it in Git
4. (Optionally) publishing it to the DSP Registry

## 1. Create a minimal DSP manifest

A minimal manifest can be written by hand:

```json
{
  "version": "dsp-1.0",
  "source_id": "example_source",
  "connection": {
    "type": "custom"
  },
  "datasets": [
    {
      "dataset_id": "example_dataset",
      "kind": "custom",
      "fields": [
        { "name": "id", "type": "string" }
      ]
    }
  ]
}
```

Save as `examples/example_source.json`.

## 2. Validate against the DSP schema

From the `dsp-spec` directory:

```bash
pip install jsonschema
jsonschema -i ../examples/example_source.json specs/dsp-1.0.json
```

If no errors appear, the manifest is valid according to `dsp-1.0`.

## 3. Generate manifests with the DSP SDK

Instead of hand-writing manifests, you can use the SDK (Python).

Install the SDK locally:

```bash
cd dsp-sdk
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

Then create a manifest for a SQL database:

```python
from sqlalchemy import create_engine
from dsp_sdk.profiles.sql import introspect_sql
from dsp_sdk.core.io import save_source

engine = create_engine("postgresql://user:password@host:5432/dbname")

source = introspect_sql(
    source_id="example_sql_source",
    engine=engine,
    schemas=["public"],
)

save_source(source, "../examples/sql_source.json")
```

## 4. Store manifests in Git

Commit your DSP manifests in your own repo:

```bash
git add examples/sql_source.json
git commit -m "Add initial DSP manifest"
```

## 5. (Optional) Publish to the DSP Registry

See [Registry Service](dsp-registry.md) for how to run the reference registry and publish manifests to it using HTTP.
