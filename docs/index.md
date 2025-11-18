# DSP – Data Source Publication

DSP (Data Source Publication) is an open, technology-neutral standard for describing
enterprise data sources, datasets, and schemas in a single JSON format.

It lets any system – databases, streams, APIs, files, search, NoSQL, graphs, SaaS platforms –
publish a **DSP manifest** that describes:

- What data exists (datasets and fields)
- How it is structured (types, nullability, partitioning)
- How to access it (SQL, HTTP, topics, paths)
- Optional business semantics (domains, entity types, join hints, PII)

DSP does **not** move data. It standardizes **metadata** so tools, agents, catalogs, and humans
can discover and understand data consistently.

## Repository Layout

- `dsp-spec/` – DSP JSON Schema (`dsp-1.0.json`)
- `dsp-sdk/` – Python SDK with core models and profiles
- `dsp-registry/` – Reference registry service for publishing and discovering manifests
- `examples/` – Example DSP manifests for common data source types
- `docs/` – Documentation site powered by mkdocs

See [Getting Started](getting-started.md) to create your first DSP manifest.
