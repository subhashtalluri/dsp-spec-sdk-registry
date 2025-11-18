# DSP Registry Service

The DSP Registry is a small HTTP service that stores and indexes DSP manifests.

It provides:

- `GET  /health` – health check
- `PUT  /dsp/sources/{source_id}` – publish or update a manifest
- `GET  /dsp/sources` – list all sources
- `GET  /dsp/sources/{source_id}` – get a single manifest
- `GET  /dsp/search` – simple search over datasets and fields

The reference implementation is in `dsp-registry/` and uses FastAPI with an in-memory
store (suitable for demos, POCs, and as a blueprint for production).

---

## Running the registry

From the `dsp-registry` directory:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8080
```

The API will be available at `http://localhost:8080`.

Open the interactive docs:

- `http://localhost:8080/docs`

---

## Publishing a manifest

Assume you have `examples/sql_source.json` ready:

```bash
curl -X PUT   http://localhost:8080/dsp/sources/sql_example   -H "Content-Type: application/json"   --data-binary @../examples/sql_source.json
```

You should see a JSON response confirming the source was stored.

---

## Listing and retrieving manifests

List all sources:

```bash
curl http://localhost:8080/dsp/sources
```

Get a specific manifest:

```bash
curl http://localhost:8080/dsp/sources/sql_example
```

---

## Simple search

Search by `dataset_id`, `field_name`, or `domain`:

```bash
curl "http://localhost:8080/dsp/search?field_name=id"
```

The search API is deliberately simple; you can extend it with more fields, filters, and
backends (for example a real database or search engine) as needed.
