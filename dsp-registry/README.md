# DSP Registry (Reference Implementation)

The DSP Registry is a small HTTP service for storing and discovering DSP manifests.

It is:

- Generic (no domain-specific assumptions)
- Backed by an in-memory store (for demos and POCs)
- Built with FastAPI
- Designed to be easy to replace with your own storage (SQL, NoSQL, search, etc.)

## API

- `GET  /health` – health check
- `PUT  /dsp/sources/{source_id}` – create or update a DSP manifest
- `GET  /dsp/sources` – list all sources
- `GET  /dsp/sources/{source_id}` – retrieve a manifest
- `GET  /dsp/search` – search by dataset_id, field_name, or domain
- `GET  /ui` and `/ui/sources/{source_id}` – simple HTML catalog UI
