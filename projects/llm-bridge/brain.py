"""
LLM Bridge CLI. Vault I/O, archive/snapshot, Typer. idea/thinking/initiative: critique, explore, normalize, promote; context at root.
Calls ai_client.call() only; no HTTP logic here.
"""
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# Section timestamps (critique, explore, context) use Eastern for display
SECTION_TZ = ZoneInfo("America/New_York")
SECTION_TZ_LABEL = "ET"

import typer
import yaml
from rich.console import Console

from config import Config
from ai_client import call as ai_call

app = typer.Typer()
console = Console()

# Alias → Config (used by resolution waterfall)
MODEL_ALIAS_TO_STRING = {
    "reasoning": Config.MODEL_REASONING,
    "workhorse": Config.MODEL_WORKHORSE,
    "nano": Config.MODEL_NANO,
}
TEMPERATURE_ALIAS_TO_FLOAT = {
    "reasoning": Config.TEMPERATURE_REASONING,
    "workhorse": Config.TEMPERATURE_WORKHORSE,
    "nano": Config.TEMPERATURE_NANO,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def resolve_under_vault(path_arg: str) -> tuple[Path, str]:
    """
    Resolve a path argument to (full_path, vault_relative_str).
    Accepts vault-relative (01-inbox/foo.md) or repo-relative (vault/10-thinking/foo.md).
    Paths with .. are normalized. Result must be under VAULT_ROOT. Raises FileNotFoundError if not.
    """
    root = Config.VAULT_ROOT.resolve()
    p = Path(path_arg.strip())
    # If path starts with "vault/", treat as repo-relative: strip prefix and use rest under VAULT_ROOT
    if p.parts and p.parts[0] == "vault":
        rest = Path(*p.parts[1:]) if len(p.parts) > 1 else Path(".")
        full = (root / rest).resolve()
    else:
        full = (root / p).resolve()
    if full != root and not str(full).startswith(str(root) + os.sep):
        raise FileNotFoundError(f"Path is not under vault: {path_arg}")
    vault_rel = full.relative_to(root)
    return full, str(vault_rel)


def read_file(path_arg: str) -> str:
    """Resolve path (vault-relative or vault/...) and read file. UTF-8. Raises on missing file."""
    full, _ = resolve_under_vault(path_arg)
    return full.read_text(encoding="utf-8")


def archive_file(vault_relative_path: str, archive_filename: str) -> None:
    """Move file to {parent_folder}/archive/{archive_filename}. Creates archive/ if needed. Raises on failure."""
    full = Config.VAULT_ROOT / vault_relative_path
    parent = full.parent
    archive_dir = parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / archive_filename
    shutil.move(str(full), str(dest))


def snapshot_note_for_llm(note_path: str) -> None:
    """Copy note to {folder}/archive/{stem}-{YYYYMMDD-HHMMSS}.md. Raises on failure. Caller aborts if this fails."""
    full = Config.VAULT_ROOT / note_path
    parent = full.parent
    archive_dir = parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    stem = full.stem
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    dest_name = f"{stem}-{timestamp}.md"
    dest = archive_dir / dest_name
    shutil.copy2(str(full), str(dest))


def build_user_message(
    note_content: str,
    context_files: list[str],
    note_path: str,
) -> str:
    """Assemble user message: [CONTEXT: path] blocks first, then [NOTE: note_path]. Not used by context command."""
    parts = []
    for path in context_files:
        content = read_file(path)
        parts.append(f"[CONTEXT: {path}]\n{content}")
    parts.append(f"[NOTE: {note_path}]\n{note_content}")
    return "\n\n---\n\n".join(parts)


def append_to_note(note_path: str, llm_output: str, mode: str) -> None:
    """Atomic append: original + --- + ## LLM Output — {mode} — {timestamp} + llm_output. Removes .tmp on exception."""
    full = Config.VAULT_ROOT / note_path
    original = full.read_text(encoding="utf-8")
    ts = datetime.now(SECTION_TZ).strftime("%Y-%m-%d %H:%M")
    section = f"\n\n---\n\n## LLM Output — {mode} — {ts} {SECTION_TZ_LABEL}\n\n{llm_output}"
    new_content = original + section
    tmp_path = full.with_suffix(full.suffix + ".tmp")
    try:
        tmp_path.write_text(new_content, encoding="utf-8")
        os.replace(tmp_path, full)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def append_to_file(vault_relative_path: str, llm_output: str, mode: str) -> None:
    """Same atomic pattern as append_to_note; used by context command."""
    full = Config.VAULT_ROOT / vault_relative_path
    original = full.read_text(encoding="utf-8")
    ts = datetime.now(SECTION_TZ).strftime("%Y-%m-%d %H:%M")
    section = f"\n\n---\n\n## LLM Output — {mode} — {ts} {SECTION_TZ_LABEL}\n\n{llm_output}"
    new_content = original + section
    tmp_path = full.with_suffix(full.suffix + ".tmp")
    try:
        tmp_path.write_text(new_content, encoding="utf-8")
        os.replace(tmp_path, full)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def append_raw_to_file(vault_relative_path: str, content: str) -> None:
    """Atomic append of raw content (no timestamp or section wrapper). Used by absorb."""
    full = Config.VAULT_ROOT / vault_relative_path
    original = full.read_text(encoding="utf-8")
    if content and not content.startswith("\n"):
        content = "\n\n" + content
    new_content = original + content
    tmp_path = full.with_suffix(full.suffix + ".tmp")
    try:
        tmp_path.write_text(new_content, encoding="utf-8")
        os.replace(tmp_path, full)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def append_section(note_path: str, content: str, section_title: str) -> None:
    """
    Atomic append of a named heading section to a note.
    Format: \\n\\n---\\n\\n# {section_title} — {YYYY-MM-DD HH:MM} ET\\n\\n{content}
    Atomic via .tmp + os.replace. Removes .tmp on exception.
    """
    full = Config.VAULT_ROOT / note_path
    original = full.read_text(encoding="utf-8")
    ts = datetime.now(SECTION_TZ).strftime("%Y-%m-%d %H:%M")
    section = f"\n\n---\n\n# {section_title} — {ts} {SECTION_TZ_LABEL}\n\n{content}"
    new_content = original + section
    tmp_path = full.with_suffix(full.suffix + ".tmp")
    try:
        tmp_path.write_text(new_content, encoding="utf-8")
        os.replace(tmp_path, full)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


# Injected section boundaries: allow flexible newlines (\n+---\n+# Section) so manual edits don't break parsing
_INJECTED_BOUNDARY_PATTERNS = [
    re.compile(r"\n+---\n+# Critique"),
    re.compile(r"\n+---\n+# Explore"),
    re.compile(r"\n+---\n+# Thinking"),
    re.compile(r"\n+---\n+# Spec"),
]


def _find_first_injected_boundary(remainder: str) -> int:
    """Return index in remainder of the first injected section boundary, or -1 if none."""
    idx = -1
    for pat in _INJECTED_BOUNDARY_PATTERNS:
        m = pat.search(remainder)
        if m is not None and (idx < 0 or m.start() < idx):
            idx = m.start()
    return idx


def extract_current_version(full_content: str) -> tuple[str, str, str, bool]:
    """
    Extract the "Current Version" block for normalize. Frontmatter-aware; uses only
    # Critique / # Explore / # Thinking / # Spec as stop boundaries (not bare ---).
    Returns (current_text_for_llm, prefix, suffix, had_current_version_header).
    Reassemble: prefix + ("# Current Version\\n\\n" if not had_current_version_header else "") + normalized + suffix.
    """
    # Frontmatter: leading --- ... ---
    frontmatter = ""
    remainder = full_content
    if full_content.strip().startswith("---"):
        rest = full_content.lstrip()
        if rest.startswith("---"):
            end_fm = rest.find("\n---", 3)
            if end_fm >= 0:
                # Include closing --- and newline
                frontmatter = rest[: end_fm + 4]
                remainder = rest[end_fm + 4 :].lstrip("\n")
            else:
                remainder = rest

    boundary_idx = _find_first_injected_boundary(remainder)
    if boundary_idx < 0:
        boundary_idx = len(remainder)

    had_header = remainder.strip().startswith("# Current Version")
    if had_header:
        start = remainder.find("# Current Version") + len("# Current Version")
        while start < len(remainder) and remainder[start] in "\n\r":
            start += 1
        current_text = (remainder[start:boundary_idx] if boundary_idx <= len(remainder) else remainder[start:]).strip()
        prefix = frontmatter + remainder[:start]
        suffix = remainder[boundary_idx:] if boundary_idx < len(remainder) else ""
    else:
        current_text = (remainder[:boundary_idx] if boundary_idx < len(remainder) else remainder).strip()
        prefix = frontmatter
        suffix = remainder[boundary_idx:] if boundary_idx < len(remainder) else ""

    return current_text, prefix, suffix, had_header


def write_new_file(vault_relative_path: str, content: str) -> None:
    """Atomic write to path. Creates parent dirs if missing. Removes .tmp on exception. Used by promote commands."""
    full = Config.VAULT_ROOT / vault_relative_path
    full.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = full.with_suffix(full.suffix + ".tmp")
    try:
        tmp_path.write_text(content, encoding="utf-8")
        os.replace(tmp_path, full)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def load_prompt(name: str) -> dict:
    """
    Load prompt file from PROMPTS_ROOT. Parse optional YAML frontmatter between ---.
    Returns {"content": str, "model": str|None, "temperature": str|float|None}.
    Missing file: typer.Exit(1), no fallback.
    """
    path = Config.PROMPTS_ROOT / name
    if not path.exists():
        console.print(f"[red]Prompt file not found: {path}[/red]")
        raise typer.Exit(1)
    raw = path.read_text(encoding="utf-8")
    content = raw
    model_alias: str | None = None
    temperature_val: str | float | None = None

    if raw.startswith("---"):
        rest = raw[3:].lstrip("\n")
        idx = rest.find("\n---")
        if idx >= 0:
            frontmatter_block = rest[:idx].strip()
            content = rest[idx + 4:].lstrip("\n")
            if frontmatter_block:
                try:
                    fm = yaml.safe_load(frontmatter_block)
                    if isinstance(fm, dict):
                        model_alias = fm.get("model")
                        temperature_val = fm.get("temperature")
                except yaml.YAMLError:
                    pass

    return {"content": content, "model": model_alias, "temperature": temperature_val}


def _set_frontmatter_status(content: str, status: str) -> str:
    """
    Set status in frontmatter (add or overwrite). If no frontmatter, prepend minimal ---\\nstatus: {status}\\n---\\n\\n.
    Uses same --- delimiters and PyYAML as load_prompt. Returns full file content to write.
    """
    raw = content
    if raw.strip().startswith("---"):
        rest = raw.lstrip()
        if rest.startswith("---"):
            rest = rest[3:].lstrip("\n")
            idx = rest.find("\n---")
            if idx >= 0:
                frontmatter_block = rest[:idx].strip()
                body = rest[idx + 4 :].lstrip("\n")
                if frontmatter_block:
                    try:
                        fm = yaml.safe_load(frontmatter_block)
                        if isinstance(fm, dict):
                            fm["status"] = status
                            dumped = yaml.dump(fm, default_flow_style=False)
                            return "---\n" + dumped.strip() + "\n---\n\n" + body
                    except yaml.YAMLError:
                        pass
                return f"---\nstatus: {status}\n---\n\n" + (body or "")
    return f"---\nstatus: {status}\n---\n\n" + raw


def _set_killed_frontmatter(content: str) -> str:
    """Set status: killed in frontmatter. Delegates to _set_frontmatter_status."""
    return _set_frontmatter_status(content, "killed")


def _set_absorbed_frontmatter(content: str, root_stem: str) -> str:
    """Set status: absorbed to [[root_stem]] in frontmatter. For source notes after absorb."""
    return _set_frontmatter_status(content, f"absorbed to [[{root_stem}]]")


def resolve_model_and_temp(
    prompt: dict,
    cli_temperature: float | None,
) -> tuple[str, float]:
    """
    Resolution waterfall: model = frontmatter model alias → fallback workhorse → Config;
    temperature = CLI → frontmatter temperature alias → Config default for model alias.
    """
    model_alias = prompt.get("model") or "workhorse"
    model_string = MODEL_ALIAS_TO_STRING.get(model_alias)
    if model_string is None:
        console.print(f"[red]Unknown model alias in prompt: {model_alias}[/red]")
        raise typer.Exit(1)
    if cli_temperature is not None:
        temp = cli_temperature
    else:
        temp_alias = prompt.get("temperature") or model_alias
        temp = TEMPERATURE_ALIAS_TO_FLOAT.get(temp_alias)
        if temp is None:
            temp = TEMPERATURE_ALIAS_TO_FLOAT.get(model_alias, Config.TEMPERATURE_WORKHORSE)
    return model_string, float(temp)


def print_dry_run_payload(
    model: str,
    temperature: float,
    messages: list[dict],
    max_tokens: int = 4096,
) -> None:
    """Print exact JSON payload that would be sent. Truncate message content to 120 chars."""
    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [],
    }
    for m in messages:
        msg = dict(m)
        if isinstance(msg.get("content"), str) and len(msg["content"]) > 120:
            msg["content"] = msg["content"][:120] + "... [truncated]"
        payload["messages"].append(msg)
    print(json.dumps(payload, indent=2))


# ---------------------------------------------------------------------------
# Idea
# ---------------------------------------------------------------------------

idea_app = typer.Typer()
app.add_typer(idea_app, name="idea")


@idea_app.command("critique")
def idea_critique(
    file: str = typer.Argument(..., help="Path: vault-relative (01-inbox/foo.md) or repo-relative (vault/01-inbox/foo.md)"),
    context: list[str] = typer.Option([], "--context", "-c", help="Context file(s), repeatable"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print payload only"),
    temperature: float | None = typer.Option(None, "--temperature", "-t", help="Override temperature"),
) -> None:
    """Audit raw idea. Append # Critique section."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    context_rel = [resolve_under_vault(c)[1] for c in context]
    prompt = load_prompt("critique-idea.md")
    user_content = build_user_message(note_content, context_rel, vault_rel)
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(vault_rel, result["content"], "Critique")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {vault_rel}")


@idea_app.command("explore")
def idea_explore(
    file: str = typer.Argument(..., help="Path: vault-relative (01-inbox/foo.md) or repo-relative (vault/01-inbox/foo.md)"),
    context: list[str] = typer.Option([], "--context", "-c", help="Context file(s), repeatable"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print payload only"),
    temperature: float | None = typer.Option(None, "--temperature", "-t", help="Override temperature"),
) -> None:
    """Expand possibilities on idea. Append # Explore section."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    context_rel = [resolve_under_vault(c)[1] for c in context]
    prompt = load_prompt("explore.md")
    base_user = build_user_message(note_content, context_rel, vault_rel)
    user_content = f"[STAGE: idea]\n\n{base_user}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(vault_rel, result["content"], "Explore")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {vault_rel}")


@idea_app.command("normalize")
def idea_normalize(
    file: str = typer.Argument(..., help="Path: vault-relative (01-inbox/foo.md) or repo-relative (vault/01-inbox/foo.md)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print payload only"),
    temperature: float | None = typer.Option(None, "--temperature", "-t", help="Override temperature"),
    snapshot: bool = typer.Option(False, "--snapshot", help="Snapshot note to archive before overwriting"),
) -> None:
    """Rewrite # Current Version only for clarity. Preserves # Critique / # Explore."""
    _, vault_rel = resolve_under_vault(file)
    full_content = read_file(file)
    current_text, prefix, suffix, had_header = extract_current_version(full_content)
    prompt = load_prompt("normalize.md")
    user_content = f"[CURRENT VERSION CONTENT]\n{current_text}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if snapshot:
        snapshot_note_for_llm(vault_rel)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    normalized = result["content"].strip()
    if not had_header:
        new_content = prefix + "# Current Version\n\n" + normalized + suffix
    else:
        new_content = prefix + normalized + suffix
    write_new_file(vault_rel, new_content)
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Normalized {vault_rel}")


@idea_app.command("promote")
def idea_promote(
    file: str = typer.Argument(..., help="Path: vault-relative (01-inbox/foo.md) or repo-relative (vault/01-inbox/foo.md)"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """LLM transforms idea → thinking note. Archive original, write new file to 10-thinking/."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    prompt = load_prompt("promote-idea-to-thinking.md")
    user_content = f"[NOTE: {vault_rel}]\n{note_content}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; original untouched.[/red]")
        raise typer.Exit(1)
    filename = Path(vault_rel).name
    archive_file(vault_rel, filename)
    dest = f"10-thinking/{filename}"
    write_new_file(dest, result["content"])
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    archive_path = f"{Path(vault_rel).parent}/archive/{filename}"
    console.print(f"Promoted → {dest} (original archived to {archive_path})")


@idea_app.command("kill")
def idea_kill(
    file: str = typer.Argument(..., help="Path: vault-relative or repo-relative"),
) -> None:
    """Move idea to archive and mark as killed. No LLM call."""
    _, vault_rel = resolve_under_vault(file)
    content = read_file(file)
    new_content = _set_killed_frontmatter(content)
    write_new_file(vault_rel, new_content)
    filename = Path(vault_rel).name
    archive_file(vault_rel, filename)
    archive_path = f"{Path(vault_rel).parent}/archive/{filename}"
    console.print(f"Killed → {archive_path}")


# ---------------------------------------------------------------------------
# Thinking
# ---------------------------------------------------------------------------

thinking_app = typer.Typer()
app.add_typer(thinking_app, name="thinking")


@thinking_app.command("critique")
def thinking_critique(
    file: str = typer.Argument(..., help="Path: vault-relative (10-thinking/foo.md) or repo-relative (vault/10-thinking/foo.md)"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Audit thinking note. Append # Critique section."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    context_rel = [resolve_under_vault(c)[1] for c in context]
    prompt = load_prompt("critique-thinking.md")
    user_content = build_user_message(note_content, context_rel, vault_rel)
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(vault_rel, result["content"], "Critique")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {vault_rel}")


@thinking_app.command("explore")
def thinking_explore(
    file: str = typer.Argument(..., help="Path: vault-relative (10-thinking/foo.md) or repo-relative (vault/10-thinking/foo.md)"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Deepen reasoning on thinking note. Append # Explore section."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    context_rel = [resolve_under_vault(c)[1] for c in context]
    prompt = load_prompt("explore.md")
    base_user = build_user_message(note_content, context_rel, vault_rel)
    user_content = f"[STAGE: thinking]\n\n{base_user}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(vault_rel, result["content"], "Explore")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {vault_rel}")


@thinking_app.command("spec")
def thinking_spec(
    file: str = typer.Argument(..., help="Path: vault-relative (10-thinking/foo.md) or repo-relative (vault/10-thinking/foo.md)"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Generate initiative spec content. Append # Spec section."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    context_rel = [resolve_under_vault(c)[1] for c in context]
    prompt = load_prompt("specify-mode.md")
    user_content = build_user_message(note_content, context_rel, vault_rel)
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(vault_rel, result["content"], "Spec")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {vault_rel}")


@thinking_app.command("normalize")
def thinking_normalize(
    file: str = typer.Argument(..., help="Path: vault-relative (10-thinking/foo.md) or repo-relative (vault/10-thinking/foo.md)"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
    snapshot: bool = typer.Option(False, "--snapshot", help="Snapshot note to archive before overwriting"),
) -> None:
    """Rewrite # Current Version only for clarity. Preserves # Critique / # Explore."""
    _, vault_rel = resolve_under_vault(file)
    full_content = read_file(file)
    current_text, prefix, suffix, had_header = extract_current_version(full_content)
    prompt = load_prompt("normalize.md")
    user_content = f"[CURRENT VERSION CONTENT]\n{current_text}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if snapshot:
        snapshot_note_for_llm(vault_rel)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    normalized = result["content"].strip()
    if not had_header:
        new_content = prefix + "# Current Version\n\n" + normalized + suffix
    else:
        new_content = prefix + normalized + suffix
    write_new_file(vault_rel, new_content)
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Normalized {vault_rel}")


@thinking_app.command("promote")
def thinking_promote(
    file: str = typer.Argument(..., help="Path: vault-relative (10-thinking/foo.md) or repo-relative (vault/10-thinking/foo.md)"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """LLM transforms thinking → initiative. Archive original, write new file to 30-initiatives/."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    prompt = load_prompt("promote-thinking-to-initiative.md")
    user_content = f"[NOTE: {vault_rel}]\n{note_content}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; original untouched.[/red]")
        raise typer.Exit(1)
    filename = Path(vault_rel).name
    archive_file(vault_rel, filename)
    dest = f"30-initiatives/drafting/{filename}"
    write_new_file(dest, result["content"])
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    archive_path = f"{Path(vault_rel).parent}/archive/{filename}"
    console.print(f"Promoted → {dest} (original archived to {archive_path})")


@thinking_app.command("kill")
def thinking_kill(
    file: str = typer.Argument(..., help="Path: vault-relative or repo-relative"),
) -> None:
    """Move thinking note to archive and mark as killed. No LLM call."""
    _, vault_rel = resolve_under_vault(file)
    content = read_file(file)
    new_content = _set_killed_frontmatter(content)
    write_new_file(vault_rel, new_content)
    filename = Path(vault_rel).name
    archive_file(vault_rel, filename)
    archive_path = f"{Path(vault_rel).parent}/archive/{filename}"
    console.print(f"Killed → {archive_path}")


# ---------------------------------------------------------------------------
# Initiative
# ---------------------------------------------------------------------------

initiative_app = typer.Typer()
app.add_typer(initiative_app, name="initiative")


@initiative_app.command("critique")
def initiative_critique(
    file: str = typer.Argument(..., help="Path: vault-relative (30-initiatives/foo.md) or repo-relative (vault/30-initiatives/foo.md)"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Audit initiative spec. Append # Critique section."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    context_rel = [resolve_under_vault(c)[1] for c in context]
    prompt = load_prompt("critique-initiative.md")
    user_content = build_user_message(note_content, context_rel, vault_rel)
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(vault_rel, result["content"], "Critique")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {vault_rel}")


@initiative_app.command("explore")
def initiative_explore(
    file: str = typer.Argument(..., help="Path: vault-relative (30-initiatives/foo.md) or repo-relative (vault/30-initiatives/foo.md)"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Explore execution options and tradeoffs. Append # Explore section."""
    _, vault_rel = resolve_under_vault(file)
    note_content = read_file(file)
    context_rel = [resolve_under_vault(c)[1] for c in context]
    prompt = load_prompt("explore.md")
    base_user = build_user_message(note_content, context_rel, vault_rel)
    user_content = f"[STAGE: initiative]\n\n{base_user}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(vault_rel, result["content"], "Explore")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {vault_rel}")


@initiative_app.command("normalize")
def initiative_normalize(
    file: str = typer.Argument(..., help="Path: vault-relative (30-initiatives/foo.md) or repo-relative (vault/30-initiatives/foo.md)"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
    snapshot: bool = typer.Option(False, "--snapshot", help="Snapshot note to archive before overwriting"),
) -> None:
    """Rewrite # Current Version only for clarity. Preserves # Critique / # Explore."""
    _, vault_rel = resolve_under_vault(file)
    full_content = read_file(file)
    current_text, prefix, suffix, had_header = extract_current_version(full_content)
    prompt = load_prompt("normalize.md")
    user_content = f"[CURRENT VERSION CONTENT]\n{current_text}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if snapshot:
        snapshot_note_for_llm(vault_rel)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    normalized = result["content"].strip()
    if not had_header:
        new_content = prefix + "# Current Version\n\n" + normalized + suffix
    else:
        new_content = prefix + normalized + suffix
    write_new_file(vault_rel, new_content)
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Normalized {vault_rel}")


@initiative_app.command("promote")
def initiative_promote(
    file: str = typer.Argument(..., help="Path: vault-relative (30-initiatives/drafting/foo.md) or repo-relative"),
) -> None:
    """Move file from drafting/ to active/, set status: active in frontmatter. No LLM call."""
    full_path, vault_rel = resolve_under_vault(file)
    path = Path(vault_rel)
    # Dest: drafting/x.md -> active/x.md; or 30-initiatives/x.md -> 30-initiatives/active/x.md
    if path.parent.name == "drafting":
        dest_vault_rel = path.parent.parent / "active" / path.name
    else:
        dest_vault_rel = path.parent / "active" / path.name
    content = full_path.read_text(encoding="utf-8")
    new_content = _set_frontmatter_status(content, "active")
    write_new_file(str(dest_vault_rel), new_content)
    full_path.unlink()
    console.print(f"Promoted → {dest_vault_rel}")


@initiative_app.command("kill")
def initiative_kill(
    file: str = typer.Argument(..., help="Path: vault-relative or repo-relative"),
) -> None:
    """Move initiative spec to archive and mark as killed. No LLM call."""
    _, vault_rel = resolve_under_vault(file)
    content = read_file(file)
    new_content = _set_killed_frontmatter(content)
    write_new_file(vault_rel, new_content)
    filename = Path(vault_rel).name
    archive_file(vault_rel, filename)
    archive_path = f"{Path(vault_rel).parent}/archive/{filename}"
    console.print(f"Killed → {archive_path}")


# ---------------------------------------------------------------------------
# Absorb (consolidate source notes into root, then archive sources)
# ---------------------------------------------------------------------------


@app.command("absorb")
def absorb_cmd(
    root_path: str = typer.Argument(..., help="Root note path (vault-relative or vault/...)"),
    sources: list[str] = typer.Argument(..., help="Source note path(s) to absorb into root"),
) -> None:
    """Consolidate source notes into root: append ## Absorbed sections (Key Points + Raw Context), then archive sources."""
    _, root_vault_rel = resolve_under_vault(root_path)
    root_content = read_file(root_path)
    root_stem = Path(root_vault_rel).stem
    source_infos = []
    for s in sources:
        _, vault_rel = resolve_under_vault(s)
        source_content = read_file(s)
        source_infos.append((vault_rel, source_content))
    for vault_rel, _ in source_infos:
        source_stem = Path(vault_rel).stem
        if f"## Absorbed — [[{source_stem}]]" in root_content:
            console.print(f"[yellow]WARNING: source already appears absorbed[/yellow]: {vault_rel}")
    prompt = load_prompt("summarize-absorbed.md")
    model_string, temp = resolve_model_and_temp(prompt, None)
    blocks = []
    for vault_rel, source_content in source_infos:
        source_stem = Path(vault_rel).stem
        user_message = f"[NOTE: {vault_rel}]\n{source_content}"
        messages = [
            {"role": "system", "content": prompt["content"]},
            {"role": "user", "content": user_message},
        ]
        result = ai_call(model_string, temp, messages)
        if result is None:
            key_points_block = "[WARNING: LLM failed, Key Points skipped]"
        else:
            key_points_block = result["content"].strip()
            console.print(
                f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}"
            )
        block = (
            f"## Absorbed — [[{source_stem}]]\n\n"
            "### Key Points\n\n"
            f"{key_points_block}\n\n"
            "### Raw Context\n\n"
            f"{source_content}"
        )
        blocks.append(block)
    if blocks:
        append_raw_to_file(root_vault_rel, "\n\n" + "\n\n".join(blocks))
    for vault_rel, source_content in source_infos:
        try:
            new_content = _set_absorbed_frontmatter(source_content, root_stem)
            write_new_file(vault_rel, new_content)
            archive_file(vault_rel, Path(vault_rel).name)
        except Exception as e:
            console.print(f"[red]Archive failed for {vault_rel}: {e}[/red]")
            raise typer.Exit(1)
    console.print(f"Absorbed {len(blocks)} source(s) into {root_vault_rel}")


# ---------------------------------------------------------------------------
# Context (separate user message assembly — no [NOTE], no build_user_message)
# ---------------------------------------------------------------------------


@app.command("context")
def context_cmd(
    file: str = typer.Argument(..., help="Path: vault-relative (20-context/foo.md) or repo-relative (vault/20-context/foo.md)"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Summarize context block. User message is [CONTEXT: path] + contents only. Appends to context file."""
    _, vault_rel = resolve_under_vault(file)
    content = read_file(file)
    user_content = f"[CONTEXT: {vault_rel}]\n{content}"
    prompt = load_prompt("describe-context.md")
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; file unchanged.[/red]")
        raise typer.Exit(1)
    append_to_file(vault_rel, result["content"], "describe-context")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {vault_rel}")


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        app()
    except FileNotFoundError as e:
        console.print(f"[red]File not found: {e}[/red]")
        raise typer.Exit(1)
