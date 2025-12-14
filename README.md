# DSP – Data Source Publication  
**A Universal Metadata Standard for Enterprise Data, Agents, and AI**

---

## Overview

Enterprises today operate across **highly fragmented data ecosystems**: data lakes, warehouses, APIs, streaming platforms, logs, metrics systems, SaaS applications, graph databases, and legacy on-prem systems. Each system exposes metadata differently, using incompatible schemas, naming conventions, discovery mechanisms, and access patterns.

This fragmentation creates major bottlenecks for:

- Data discovery and reuse  
- Governance and lineage  
- Cross-system analytics  
- AI/ML pipelines  
- Agentic and autonomous systems  

**DSP (Data Source Publication)** is an open, technology-neutral specification and reference implementation that standardizes **how any data source is described**, regardless of where it lives or how it is accessed.

DSP does **not** move data.  
DSP does **not** replace cloud catalogs.  
DSP standardizes metadata so humans, tools, and agents can reason about data **consistently and automatically**.

## Documentation

https://subhashtalluri.github.io/dsp-spec-sdk-registry/

---

## What DSP Standardizes

DSP defines a single JSON manifest format that describes:

### 1. Data Sources
A *Source* represents any system that contains data:
- SQL databases and warehouses  
- Data lakes and file systems  
- Streaming platforms  
- APIs and SaaS systems  
- Logs, metrics, and observability stacks  
- NoSQL and document stores  
- Graph databases  
- Proprietary or legacy systems  

### 2. Datasets
Each source contains one or more *Datasets*:
- Tables, views  
- Topics, streams  
- API endpoints  
- File paths  
- Indexes  
- Node and edge sets  
- Metric series  
- Log streams  

### 3. Fields
Each dataset describes its fields:
- Name, type, nullability  
- Physical mapping (column name, JSON path, etc.)  
- Optional constraints  
- Optional semantic annotations  

### 4. Semantics (Optional but Powerful)
DSP supports rich semantic metadata:
- Domain (e.g. customer, network, operations)  
- Entity type and grain  
- Time semantics  
- Join hints across datasets  
- PII and sensitivity indicators  
- Business process context  

### 5. Access Metadata
DSP describes *how* data can be accessed:
- SQL query interfaces  
- HTTP APIs  
- Streaming subscriptions  
- File layouts (S3, HDFS, etc.)  

This makes DSP usable by:
- Humans (catalogs, documentation)  
- Tools (ETL, analytics, governance)  
- Agents (planning, reasoning, automation)  

---

## How DSP Fits with Cloud Catalogs (AWS Example)

DSP is designed to **sit on top of existing cloud-native catalogs**, not replace them.

On AWS:
- **AWS Glue Data Catalog** remains the system of record for:
  - Schemas  
  - Tables  
  - Partitions  
  - Iceberg metadata  
- **Lake Formation** handles governance and access control  
- **Athena, Redshift, EMR, Spark** use Glue directly for execution  

DSP complements this by:
- Providing a **logical, cross-platform metadata layer**  
- Normalizing metadata across AWS and non-AWS systems  
- Enabling unified discovery and lineage beyond a single cloud  

In short:
- Glue answers *where and how data is queried*  
- DSP answers *what the data represents across the enterprise*  

---

## DSP and Agentic Systems (MCP & A2A)

DSP is designed for **agent-native architectures**.

### DSP + MCP (Model Context Protocol)
DSP manifests can be exposed as MCP tools:
- `dsp_list_sources`  
- `dsp_search_datasets`  
- `dsp_get_manifest`  

Agents can dynamically:
1. Discover available datasets  
2. Fetch schemas and semantics  
3. Understand access patterns  
4. Plan queries, analytics, or actions  

### DSP + A2A (Agent-to-Agent)
DSP provides a shared language for agent collaboration:
- Agents exchange DSP references (source + dataset)  
- Receiving agents resolve the same manifest  
- No custom schema translation required  

DSP enables **interoperable, multi-agent reasoning** across teams, vendors, and platforms.

---

## Repository Structure

```text
dsp/
├── dsp-spec/        # DSP JSON Schema (dsp-1.0)
├── dsp-sdk/         # Python SDK and profiles
├── dsp-registry/    # Reference registry + UI
├── docs/            # Full documentation (mkdocs)
├── examples/        # Example DSP manifests
├── mcp-adapter/     # MCP tool definitions & handlers
└── mkdocs.yml
