from __future__ import annotations

from typing import Dict, List, Optional

from dsp_sdk import Source


class InMemoryStore:
    """Simple in-memory store for DSP Source manifests."""

    def __init__(self) -> None:
        self._sources: Dict[str, Source] = {}

    def upsert(self, source: Source) -> None:
        self._sources[source.source_id] = source

    def get(self, source_id: str) -> Optional[Source]:
        return self._sources.get(source_id)

    def list(self) -> List[Source]:
        return list(self._sources.values())

    def search(
        self,
        dataset_id: Optional[str] = None,
        field_name: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> List[Dict]:
        results: List[Dict] = []

        for src in self._sources.values():
            for ds in src.datasets:
                if dataset_id and dataset_id not in ds.dataset_id:
                    continue

                if domain:
                    ds_domain = (ds.semantics.domain if ds.semantics else None)
                    if not ds_domain or domain.lower() not in ds_domain.lower():
                        continue

                field_names = [f.name for f in ds.fields]
                if field_name and field_name not in field_names:
                    continue

                results.append(
                    {
                        "source_id": src.source_id,
                        "dataset_id": ds.dataset_id,
                        "field_names": field_names,
                        "domain": (ds.semantics.domain if ds.semantics else None),
                    }
                )

        return results
