import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class BaseConnector(ABC):

    @abstractmethod
    def get_schema(self, entry: dict) -> list[dict]:
        """Return list of field dicts: {name, type, nullable, notes}"""

    @abstractmethod
    def get_sample(self, entry: dict, limit: int = 5) -> list[dict]:
        """Return list of sample records as dicts"""

    def close(self):
        pass

    def render(self, entry: dict, schema: list[dict], sample: list[dict]) -> str:
        now = datetime.now().strftime("%Y-%m-%d")
        label = entry.get("table") or entry.get("object") or "Unknown"
        database = entry.get("database", "")
        schema_name = entry.get("schema", "")
        description = entry.get("description", "_No description provided._")

        source_parts = [p for p in [database, schema_name] if p]
        source_label = f"**Source:** {' / '.join(source_parts)}" if source_parts else ""

        col_rows = "\n".join(
            f"| {f['name']} | {f['type']} | {f.get('nullable', '')} | {f.get('notes', '')} |"
            for f in schema
        )
        columns_section = f"""## Columns

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
{col_rows}"""

        if sample:
            headers = list(sample[0].keys())
            header_row = "| " + " | ".join(str(h) for h in headers) + " |"
            sep_row = "| " + " | ".join("---" for _ in headers) + " |"
            data_rows = "\n".join(
                "| " + " | ".join(_safe_cell(r.get(h)) for h in headers) + " |"
                for r in sample
            )
            sample_section = f"""## Sample Data

{header_row}
{sep_row}
{data_rows}"""
        else:
            sample_section = "## Sample Data\n\n_No sample data available._"

        return f"""---
type: schema
object: {label}
updated: {now}
---

# {label}

{source_label}
**Description:** {description}

{columns_section}

{sample_section}

## Usage Notes

<!-- Hand-written: join keys, gotchas, common filters. Preserved on sync. -->
"""

    def merge(self, existing: str, new_content: str) -> str:
        """Overwrite Columns + Sample Data; preserve hand-written Usage Notes."""
        usage_notes = self._extract_section(existing, "Usage Notes")
        return self._replace_section(new_content, "Usage Notes", usage_notes)

    def _extract_section(self, content: str, heading: str) -> Optional[str]:
        pattern = rf"(## {re.escape(heading)}\n)(.*?)(?=\n## |\Z)"
        match = re.search(pattern, content, re.DOTALL)
        return match.group(2).strip() if match else None

    def _replace_section(self, content: str, heading: str, replacement: Optional[str]) -> str:
        if replacement is None:
            return content
        pattern = rf"(## {re.escape(heading)}\n)(.*?)(?=\n## |\Z)"
        return re.sub(pattern, f"## {heading}\n\n{replacement}\n", content, flags=re.DOTALL)


def _safe_cell(value) -> str:
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")[:80]
