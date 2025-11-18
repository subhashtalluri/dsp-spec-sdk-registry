# DSP – Data Source Publication

This repository contains a complete reference implementation of **DSP (Data Source Publication)**:

- **dsp-spec/** – JSON Schema for DSP (`dsp-1.0.json`)
- **dsp-sdk/** – Python SDK (Pydantic models, IO, validation, profiles)
- **dsp-registry/** – FastAPI-based registry service + HTML catalog UI
- **docs/** – mkdocs documentation (overview, getting started, source types cookbook, registry, examples)
- **examples/** – Example DSP manifests for multiple source types
- **mcp-adapter/** – Example MCP adapter for exposing the DSP registry as tools

The goal is to provide a **technology-neutral, domain-agnostic** way for enterprises to publish
metadata about any data source in a single JSON shape, so humans, tools, and agents can discover
and reason about data consistently.
