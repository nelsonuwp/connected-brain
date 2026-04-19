"""Role-based persona prompts (YAML)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

_DIR = Path(__file__).resolve().parent


@dataclass
class Persona:
    slug: str
    label: str
    voice: str
    style_rules: list[str]


def load_personas() -> dict[str, Persona]:
    out: dict[str, Persona] = {}
    for path in sorted(_DIR.glob("*.yaml")):
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            slug = str(raw.get("slug", path.stem))
            out[slug] = Persona(
                slug=slug,
                label=str(raw.get("label", slug)),
                voice=str(raw.get("voice", "")).strip(),
                style_rules=list(raw.get("style_rules") or []),
            )
        except Exception as e:
            logger.warning("Skip persona %s: %s", path, e)
    return out


def persona_system_prompt(p: Persona) -> str:
    rules = "\n".join(f"- {r}" for r in p.style_rules)
    return f"{p.voice}\n\nStyle rules:\n{rules}".strip()


def list_persona_choices() -> list[dict[str, str]]:
    return [{"slug": p.slug, "label": p.label} for p in load_personas().values()]
