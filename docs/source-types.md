# Source Types Cookbook

This page shows **how to describe different kinds of enterprise data systems** using DSP.

For every system, the pattern is the same:

1. Define a **Source** (`source_id`, `connection`)
2. Define one or more **Datasets** (`dataset_id`, `kind`, `physical_name`)
3. Define **Fields** (`name`, `type`, `nullable`, `mapping`)
4. Optionally add **Semantics** (domain, entity_type, PII, join hints)
5. Optionally add **Access** metadata (SQL/search/stream/file)

DSP uses **one JSON shape** for all of them – the difference is mostly in:

- `connection.type`  
- `connection.driver`  
- `dataset.kind`  
- `dataset.access` details  

You can either hand-write the JSON or use the **DSP SDK profiles** where available.

(Full cookbook content omitted here for brevity in this comment, but in your actual
project you can paste the full Source Types Cookbook as previously generated.)
