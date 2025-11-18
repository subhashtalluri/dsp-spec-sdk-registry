# DSP Examples

This repository includes example DSP manifests under `examples/`:

- `sql_source.json` – generic relational database / warehouse
- `stream_source.json` – generic streaming platform topics
- `api_source.json` – generic REST API based on an OpenAPI-like contract
- `file_source.json` – generic file-based dataset (for example object storage)
- `graph_source.json` – generic graph database with nodes and edges

Each example is intentionally domain-neutral.

You can use these as templates for your own systems:

1. Copy an example JSON file
2. Change `source_id`, `connection`, `datasets`, and `fields`
3. Validate against `dsp-1.0.json`
4. Commit or publish to the registry
