"""
LLM Bridge CLI. Vault I/O, archive/snapshot, Typer. idea/thinking/initiative: critique, explore, promote; context at root.
Calls ai_client.call() only; no HTTP logic here.
"""
import json
import os
import re
import shutil
import sys
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

# Type-aware context: valid note types for 20-context/types/{type}-{command}.md
VALID_NOTE_TYPES = frozenset({"code", "business", "content"})

# Help text: note and context accept absolute or vault-relative paths (drag-and-drop friendly).
PATH_ARG_HELP = "Absolute path or vault-relative path to the note file (e.g. drag-and-drop)."
CONTEXT_ARG_HELP = "Absolute path or vault-relative path to a context file; repeatable (e.g. drag-and-drop)."


@app.callback()
def _app_callback(
    ctx: typer.Context,
    debug: bool = typer.Option(False, "--debug", help="Print full system message to stderr (explore/critique only). Temporary."),
) -> None:
    """Root callback: pass debug flag to commands via context."""
    ctx.obj = ctx.obj or {}
    ctx.obj["debug"] = debug


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


def resolve_path(path_arg: str) -> tuple[Path, str]:
    """
    Resolve note or context path: accepts absolute path or vault-relative.
    Returns (full_path, display_str). Use full_path for I/O, display_str for [NOTE]/[CONTEXT] labels.
    """
    p = Path(path_arg.strip())
    if p.is_absolute():
        full = p.resolve()
        if not full.exists():
            raise FileNotFoundError(f"File not found: {path_arg}")
        if not full.is_file():
            raise FileNotFoundError(f"Not a file: {path_arg}")
        return full, str(full)
    full, vault_rel = resolve_under_vault(path_arg)
    return full, vault_rel


def read_file(path_arg: str) -> str:
    """Resolve path (absolute, vault-relative, or vault/...) and read file. UTF-8. Raises on missing file."""
    p = Path(path_arg.strip())
    if p.is_absolute():
        full = p.resolve()
        if not full.exists() or not full.is_file():
            raise FileNotFoundError(f"File not found: {path_arg}")
        return full.read_text(encoding="utf-8")
    full, _ = resolve_under_vault(path_arg)
    return full.read_text(encoding="utf-8")


def archive_file(full_path: Path, archive_filename: str) -> None:
    """Move file to {parent_folder}/archive/{archive_filename}. full_path may be anywhere."""
    parent = full_path.parent
    archive_dir = parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / archive_filename
    shutil.move(str(full_path), str(dest))


def snapshot_note_for_llm(full_path: Path) -> None:
    """Copy file to {parent_folder}/archive/{stem}-{YYYYMMDD-HHMMSS}.md. full_path may be anywhere."""
    parent = full_path.parent
    archive_dir = parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    stem = full_path.stem
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    dest_name = f"{stem}-{timestamp}.md"
    dest = archive_dir / dest_name
    shutil.copy2(str(full_path), str(dest))


def build_user_message(
    note_content: str,
    context_files: list[tuple[Path, str]],
    note_display_path: str,
) -> str:
    """Assemble user message: [CONTEXT: path] blocks first, then [NOTE: note_display_path]. context_files are (path, label)."""
    parts = []
    for path, label in context_files:
        content = path.read_text(encoding="utf-8")
        console.print(f"[dim]Context loaded: {label} ({len(content)} chars)[/dim]")
        parts.append(f"[CONTEXT: {label}]\n{content}")
    parts.append(f"[NOTE: {note_display_path}]\n{note_content}")
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


def append_to_file(full_path: Path, llm_output: str, mode: str) -> None:
    """Atomic append with timestamp/section. Used by context command. full_path may be anywhere."""
    original = full_path.read_text(encoding="utf-8")
    ts = datetime.now(SECTION_TZ).strftime("%Y-%m-%d %H:%M")
    section = f"\n\n---\n\n## LLM Output — {mode} — {ts} {SECTION_TZ_LABEL}\n\n{llm_output}"
    new_content = original + section
    tmp_path = full_path.with_suffix(full_path.suffix + ".tmp")
    try:
        tmp_path.write_text(new_content, encoding="utf-8")
        os.replace(tmp_path, full_path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def append_raw_to_file(vault_relative_path: str, content: str) -> None:
    """Atomic append of raw content (no timestamp or section wrapper). Used by absorb. Accepts vault-relative or absolute path."""
    p = Path(vault_relative_path)
    full = p.resolve() if p.is_absolute() else (Config.VAULT_ROOT / vault_relative_path).resolve()
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


def append_section(full_path: Path, content: str, section_title: str) -> None:
    """
    Atomic append of a named heading section to a note. full_path may be anywhere.
    Format: \\n\\n---\\n\\n# {section_title} — {YYYY-MM-DD HH:MM} ET\\n\\n{content}
    Atomic via .tmp + os.replace. Removes .tmp on exception.
    """
    original = full_path.read_text(encoding="utf-8")
    ts = datetime.now(SECTION_TZ).strftime("%Y-%m-%d %H:%M")
    section = f"\n\n---\n\n# {section_title} — {ts} {SECTION_TZ_LABEL}\n\n{content}"
    new_content = original + section
    tmp_path = full_path.with_suffix(full_path.suffix + ".tmp")
    try:
        tmp_path.write_text(new_content, encoding="utf-8")
        os.replace(tmp_path, full_path)
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


def write_to_path(full_path: Path, content: str) -> None:
    """Atomic overwrite of a file. full_path may be anywhere."""
    tmp_path = full_path.with_suffix(full_path.suffix + ".tmp")
    try:
        tmp_path.write_text(content, encoding="utf-8")
        os.replace(tmp_path, full_path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


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


def _parse_note_frontmatter(note_content: str) -> dict | None:
    """
    Parse YAML frontmatter from note content (leading --- ... ---).
    Returns frontmatter dict or None if no frontmatter or invalid YAML.
    """
    raw = note_content.strip()
    if not raw.startswith("---"):
        return None
    rest = raw[3:].lstrip("\n")
    idx = rest.find("\n---")
    if idx < 0:
        return None
    block = rest[:idx].strip()
    if not block:
        return None
    try:
        fm = yaml.safe_load(block)
        return fm if isinstance(fm, dict) else None
    except yaml.YAMLError:
        return None


def _load_type_block(vault_root: Path, type_value: str, command: str) -> str | None:
    """Load type block from vault 20-context/types/{type}-{command}.md if file exists. UTF-8."""
    path = vault_root / "20-context" / "types" / f"{type_value}-{command}.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip() or None


def _resolve_type_block_and_warn(note_content: str, command: str) -> str | None:
    """
    Parse note frontmatter for type; if valid load type block, else print warning to stderr and return None.
    Command is 'critique' or 'explore'. Returns type block content or None.
    """
    fm = _parse_note_frontmatter(note_content)
    type_val = (fm.get("type") if fm else None) or None
    if type_val is not None and isinstance(type_val, str):
        type_val = type_val.strip() or None
    if type_val is None:
        print("[WARN] Note has no type specified — proceeding without type-specific context", file=sys.stderr)
        return None
    if type_val not in VALID_NOTE_TYPES:
        print(f"[WARN] Note has invalid type '{type_val}' — proceeding without type-specific context", file=sys.stderr)
        return None
    return _load_type_block(Config.VAULT_ROOT.resolve(), type_val, command)


def _resolve_task_prompt_and_warn(note_content: str, command: str) -> tuple[dict, str]:
    """Load task-{command}-{type}.md. type from frontmatter; default code on missing/invalid; warn to stderr."""
    fm = _parse_note_frontmatter(note_content)
    type_val = (fm.get("type") if fm else None) or None
    if type_val is not None and isinstance(type_val, str):
        type_val = type_val.strip() or None
    if type_val is None:
        print(f"[WARN] Note has no type specified — using task-{command}-code.md", file=sys.stderr)
        type_val = "code"
    elif type_val not in VALID_NOTE_TYPES:
        print(f"[WARN] Note has invalid type '{type_val}' — using task-{command}-code.md", file=sys.stderr)
        type_val = "code"
    prompt_name = f"task-{command}-{type_val}.md"
    prompt = load_prompt(prompt_name)
    return prompt, prompt_name


def _parse_route_block(note_content: str) -> dict | None:
    """Find last ---route...--- block in note. Returns dict or None."""
    marker = "---route"
    last_idx = note_content.rfind("\n" + marker + "\n")
    if last_idx == -1:
        if note_content.startswith(marker + "\n"):
            segment = note_content[len(marker) + 1:]
        else:
            return None
    else:
        segment = note_content[last_idx + len(marker) + 2:]
    lines = segment.split("\n")
    block_lines = []
    for line in lines:
        if line.strip() == "---":
            break
        block_lines.append(line)
    block = "\n".join(block_lines).strip()
    if not block:
        return None
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    rec = data.get("recommendation")
    if rec not in ("task", "thinking"):
        return None
    return {"recommendation": rec, "reason": data.get("reason") or ""}


def _build_system_content_for_type_command(
    generic_context: str | None,
    type_block: str | None,
    command_prompt: str,
) -> str:
    """Assemble system message: [generic context] → [type block] → [command prompt]. Segmented join for future generic slot."""
    segments = [generic_context or "", type_block or "", command_prompt]
    return "\n\n".join(filter(None, segments))


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
    """Set status: absorbed in frontmatter and prepend 'absorbed into [[root_stem]]' as first line of body."""
    result = _set_frontmatter_status(content, "absorbed")
    # Insert "absorbed into [[root_stem]]" as first line of content (after frontmatter)
    sep = "\n---\n\n"
    idx = result.find(sep)
    if idx >= 0:
        after_sep = idx + len(sep)
        return result[:after_sep] + f"absorbed into [[{root_stem}]]\n\n" + result[after_sep:]
    return result


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


def _log_llm_call(model: str, temperature: float, prompt_name: str) -> None:
    """Print resolved model and temperature before each LLM call."""
    console.print(f"[dim]Calling {model} (temp={temperature}) with prompt '{prompt_name}'[/dim]")


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
    ctx: typer.Context,
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    context: list[str] = typer.Option([], "--context", "-c", help=CONTEXT_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print payload only"),
    temperature: float | None = typer.Option(None, "--temperature", "-t", help="Override temperature"),
) -> None:
    """Audit raw idea. Append # Critique section."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    context_resolved = [resolve_path(c) for c in context]
    prompt = load_prompt("critique-idea.md")
    type_block = _resolve_type_block_and_warn(note_content, "critique")
    system_content = _build_system_content_for_type_command("", type_block, prompt["content"])
    user_content = build_user_message(note_content, context_resolved, display_path)
    messages = [{"role": "system", "content": system_content}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if ctx.obj and ctx.obj.get("debug"):
        print(system_content, file=sys.stderr)  # Temporary: verify type-block injection; remove after verification
    _log_llm_call(model_string, temp, "critique-idea.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(full_path, result["content"], "Critique")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {display_path}")


@idea_app.command("explore")
def idea_explore(
    ctx: typer.Context,
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    context: list[str] = typer.Option([], "--context", "-c", help=CONTEXT_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print payload only"),
    temperature: float | None = typer.Option(None, "--temperature", "-t", help="Override temperature"),
) -> None:
    """Expand possibilities on idea. Append # Explore section."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    context_resolved = [resolve_path(c) for c in context]
    prompt = load_prompt("explore.md")
    type_block = _resolve_type_block_and_warn(note_content, "explore")
    system_content = _build_system_content_for_type_command("", type_block, prompt["content"])
    base_user = build_user_message(note_content, context_resolved, display_path)
    user_content = f"[STAGE: idea]\n\n{base_user}"
    messages = [{"role": "system", "content": system_content}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if ctx.obj and ctx.obj.get("debug"):
        print(system_content, file=sys.stderr)  # Temporary: verify type-block injection; remove after verification
    _log_llm_call(model_string, temp, "explore.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(full_path, result["content"], "Explore")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {display_path}")


@idea_app.command("promote")
def idea_promote(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
    as_task: bool = typer.Option(False, "--as-task", help="Force promote to task (31-tasks/drafting) regardless of critique route"),
) -> None:
    """LLM transforms idea → thinking or task note. Archive original, write new file to 10-thinking/ or 31-tasks/drafting/."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    use_task = as_task
    if not use_task:
        route = _parse_route_block(note_content)
        if route and route.get("recommendation") == "task":
            use_task = True
    if use_task:
        prompt = load_prompt("promote-idea-to-task.md")
    else:
        prompt = load_prompt("promote-idea-to-thinking.md")
    user_content = f"[NOTE: {display_path}]\n{note_content}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    prompt_name = "promote-idea-to-task.md" if use_task else "promote-idea-to-thinking.md"
    _log_llm_call(model_string, temp, prompt_name)
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; original untouched.[/red]")
        raise typer.Exit(1)
    filename = full_path.name
    if use_task:
        promoted_content = _set_frontmatter_status(note_content, "promoted-to-task")
        write_to_path(full_path, promoted_content)
        archive_file(full_path, filename)
        write_new_file("31-tasks/drafting/" + filename, result["content"])
        dest = f"31-tasks/drafting/{filename}"
    else:
        promoted_content = _set_frontmatter_status(note_content, "promoted")
        write_to_path(full_path, promoted_content)
        archive_file(full_path, filename)
        write_new_file("10-thinking/" + filename, result["content"])
        dest = f"10-thinking/{filename}"
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    archive_path = f"{full_path.parent}/archive/{filename}"
    console.print(f"Promoted → {dest} (original archived to {archive_path})")


@idea_app.command("kill")
def idea_kill(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
) -> None:
    """Move idea to archive and mark as killed. No LLM call."""
    full_path, _ = resolve_path(file)
    content = full_path.read_text(encoding="utf-8")
    new_content = _set_killed_frontmatter(content)
    write_to_path(full_path, new_content)
    filename = full_path.name
    archive_file(full_path, filename)
    archive_path = f"{full_path.parent}/archive/{filename}"
    console.print(f"Killed → {archive_path}")


@idea_app.command("complete")
def idea_complete(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
) -> None:
    """Mark idea complete and move to 30-initiatives/completed/. No LLM call."""
    full_path, _ = resolve_path(file)
    content = full_path.read_text(encoding="utf-8")
    new_content = _set_frontmatter_status(content, "complete")
    dest = f"30-initiatives/completed/{full_path.name}"
    write_new_file(dest, new_content)
    full_path.unlink()
    console.print(f"Completed → {dest}")


# ---------------------------------------------------------------------------
# Thinking
# ---------------------------------------------------------------------------

thinking_app = typer.Typer()
app.add_typer(thinking_app, name="thinking")


@thinking_app.command("critique")
def thinking_critique(
    ctx: typer.Context,
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    context: list[str] = typer.Option([], "--context", "-c", help=CONTEXT_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Audit thinking note. Append # Critique section."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    context_resolved = [resolve_path(c) for c in context]
    prompt = load_prompt("critique-thinking.md")
    type_block = _resolve_type_block_and_warn(note_content, "critique")
    system_content = _build_system_content_for_type_command("", type_block, prompt["content"])
    user_content = build_user_message(note_content, context_resolved, display_path)
    messages = [{"role": "system", "content": system_content}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if ctx.obj and ctx.obj.get("debug"):
        print(system_content, file=sys.stderr)  # Temporary: verify type-block injection; remove after verification
    _log_llm_call(model_string, temp, "critique-thinking.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(full_path, result["content"], "Critique")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {display_path}")


@thinking_app.command("explore")
def thinking_explore(
    ctx: typer.Context,
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    context: list[str] = typer.Option([], "--context", "-c", help=CONTEXT_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Deepen reasoning on thinking note. Append # Explore section."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    context_resolved = [resolve_path(c) for c in context]
    prompt = load_prompt("explore.md")
    type_block = _resolve_type_block_and_warn(note_content, "explore")
    system_content = _build_system_content_for_type_command("", type_block, prompt["content"])
    base_user = build_user_message(note_content, context_resolved, display_path)
    user_content = f"[STAGE: thinking]\n\n{base_user}"
    messages = [{"role": "system", "content": system_content}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if ctx.obj and ctx.obj.get("debug"):
        print(system_content, file=sys.stderr)  # Temporary: verify type-block injection; remove after verification
    _log_llm_call(model_string, temp, "explore.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(full_path, result["content"], "Explore")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {display_path}")


@thinking_app.command("spec")
def thinking_spec(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    context: list[str] = typer.Option([], "--context", "-c", help=CONTEXT_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Generate initiative spec content. Append # Spec section."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    context_resolved = [resolve_path(c) for c in context]
    prompt = load_prompt("specify-mode.md")
    user_content = build_user_message(note_content, context_resolved, display_path)
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    _log_llm_call(model_string, temp, "specify-mode.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(full_path, result["content"], "Spec")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {display_path}")


@thinking_app.command("normalize")
def thinking_normalize(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
    snapshot: bool = typer.Option(False, "--snapshot", help="Snapshot note to archive before overwriting"),
) -> None:
    """Rewrite # Current Version only for clarity. Preserves # Critique / # Explore."""
    full_path, display_path = resolve_path(file)
    full_content = full_path.read_text(encoding="utf-8")
    current_text, prefix, suffix, had_header = extract_current_version(full_content)
    prompt = load_prompt("normalize.md")
    user_content = f"[CURRENT VERSION CONTENT]\n{current_text}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if snapshot:
        snapshot_note_for_llm(full_path)
    _log_llm_call(model_string, temp, "normalize.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    normalized = result["content"].strip()
    if not had_header:
        new_content = prefix + "# Current Version\n\n" + normalized + suffix
    else:
        new_content = prefix + normalized + suffix
    write_to_path(full_path, new_content)
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Normalized {display_path}")


@thinking_app.command("promote")
def thinking_promote(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """LLM transforms thinking → initiative. Archive original, write new file to 30-initiatives/."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    prompt = load_prompt("promote-thinking-to-initiative.md")
    user_content = f"[NOTE: {display_path}]\n{note_content}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    _log_llm_call(model_string, temp, "promote-thinking-to-initiative.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; original untouched.[/red]")
        raise typer.Exit(1)
    filename = full_path.name
    promoted_content = _set_frontmatter_status(note_content, "promoted")
    write_to_path(full_path, promoted_content)
    archive_file(full_path, filename)
    dest = f"30-initiatives/drafting/{filename}"
    write_new_file(dest, result["content"])
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    archive_path = f"{full_path.parent}/archive/{filename}"
    console.print(f"Promoted → {dest} (original archived to {archive_path})")


@thinking_app.command("kill")
def thinking_kill(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
) -> None:
    """Move thinking note to archive and mark as killed. No LLM call."""
    full_path, _ = resolve_path(file)
    content = full_path.read_text(encoding="utf-8")
    new_content = _set_killed_frontmatter(content)
    write_to_path(full_path, new_content)
    filename = full_path.name
    archive_file(full_path, filename)
    archive_path = f"{full_path.parent}/archive/{filename}"
    console.print(f"Killed → {archive_path}")


@thinking_app.command("complete")
def thinking_complete(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
) -> None:
    """Mark thinking note complete and move to 30-initiatives/completed/. No LLM call."""
    full_path, _ = resolve_path(file)
    content = full_path.read_text(encoding="utf-8")
    new_content = _set_frontmatter_status(content, "complete")
    dest = f"30-initiatives/completed/{full_path.name}"
    write_new_file(dest, new_content)
    full_path.unlink()
    console.print(f"Completed → {dest}")


# ---------------------------------------------------------------------------
# Initiative
# ---------------------------------------------------------------------------

initiative_app = typer.Typer()
app.add_typer(initiative_app, name="initiative")


@initiative_app.command("critique")
def initiative_critique(
    ctx: typer.Context,
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    context: list[str] = typer.Option([], "--context", "-c", help=CONTEXT_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Audit initiative spec. Append # Critique section."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    context_resolved = [resolve_path(c) for c in context]
    prompt = load_prompt("critique-initiative.md")
    type_block = _resolve_type_block_and_warn(note_content, "critique")
    system_content = _build_system_content_for_type_command("", type_block, prompt["content"])
    user_content = build_user_message(note_content, context_resolved, display_path)
    messages = [{"role": "system", "content": system_content}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if ctx.obj and ctx.obj.get("debug"):
        print(system_content, file=sys.stderr)  # Temporary: verify type-block injection; remove after verification
    _log_llm_call(model_string, temp, "critique-initiative.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(full_path, result["content"], "Critique")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {display_path}")


@initiative_app.command("explore")
def initiative_explore(
    ctx: typer.Context,
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    context: list[str] = typer.Option([], "--context", "-c", help=CONTEXT_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Explore execution options and tradeoffs. Append # Explore section."""
    full_path, display_path = resolve_path(file)
    note_content = full_path.read_text(encoding="utf-8")
    context_resolved = [resolve_path(c) for c in context]
    prompt = load_prompt("explore.md")
    type_block = _resolve_type_block_and_warn(note_content, "explore")
    system_content = _build_system_content_for_type_command("", type_block, prompt["content"])
    base_user = build_user_message(note_content, context_resolved, display_path)
    user_content = f"[STAGE: initiative]\n\n{base_user}"
    messages = [{"role": "system", "content": system_content}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if ctx.obj and ctx.obj.get("debug"):
        print(system_content, file=sys.stderr)  # Temporary: verify type-block injection; remove after verification
    _log_llm_call(model_string, temp, "explore.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_section(full_path, result["content"], "Explore")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {display_path}")


@initiative_app.command("normalize")
def initiative_normalize(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
    snapshot: bool = typer.Option(False, "--snapshot", help="Snapshot note to archive before overwriting"),
) -> None:
    """Rewrite # Current Version only for clarity. Preserves # Critique / # Explore."""
    full_path, display_path = resolve_path(file)
    full_content = full_path.read_text(encoding="utf-8")
    current_text, prefix, suffix, had_header = extract_current_version(full_content)
    prompt = load_prompt("normalize.md")
    user_content = f"[CURRENT VERSION CONTENT]\n{current_text}"
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    if snapshot:
        snapshot_note_for_llm(full_path)
    _log_llm_call(model_string, temp, "normalize.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    normalized = result["content"].strip()
    if not had_header:
        new_content = prefix + "# Current Version\n\n" + normalized + suffix
    else:
        new_content = prefix + normalized + suffix
    write_to_path(full_path, new_content)
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Normalized {display_path}")


@initiative_app.command("promote")
def initiative_promote(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
) -> None:
    """Move file from drafting/ to active/, set status: active in frontmatter. No LLM call."""
    full_path, display_path = resolve_path(file)
    root = Config.VAULT_ROOT.resolve()
    if full_path.is_relative_to(root):
        vault_rel = str(full_path.relative_to(root))
        path = Path(vault_rel)
        if path.parent.name == "drafting":
            dest_vault_rel = str(path.parent.parent / "active" / path.name)
        else:
            dest_vault_rel = str(path.parent / "active" / path.name)
    else:
        dest_vault_rel = f"30-initiatives/active/{full_path.name}"
    content = full_path.read_text(encoding="utf-8")
    new_content = _set_frontmatter_status(content, "active")
    write_new_file(dest_vault_rel, new_content)
    full_path.unlink()
    console.print(f"Promoted → {dest_vault_rel}")


@initiative_app.command("kill")
def initiative_kill(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
) -> None:
    """Move initiative spec to archive and mark as killed. No LLM call."""
    full_path, _ = resolve_path(file)
    content = full_path.read_text(encoding="utf-8")
    new_content = _set_killed_frontmatter(content)
    write_to_path(full_path, new_content)
    filename = full_path.name
    archive_file(full_path, filename)
    archive_path = f"{full_path.parent}/archive/{filename}"
    console.print(f"Killed → {archive_path}")


@initiative_app.command("complete")
def initiative_complete(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
) -> None:
    """Mark initiative complete and move to 30-initiatives/completed/. No LLM call."""
    full_path, _ = resolve_path(file)
    content = full_path.read_text(encoding="utf-8")
    new_content = _set_frontmatter_status(content, "complete")
    dest = f"30-initiatives/completed/{full_path.name}"
    write_new_file(dest, new_content)
    full_path.unlink()
    console.print(f"Completed → {dest}")


# ---------------------------------------------------------------------------
# Absorb (consolidate source notes into root, then archive sources)
# ---------------------------------------------------------------------------


@app.command("absorb")
def absorb_cmd(
    root_path: str = typer.Argument(..., help="Root note path (vault-relative or vault/...)"),
    sources: list[str] = typer.Argument(default=[], help="Source note path(s) to absorb into root"),
) -> None:
    """Consolidate source notes into root: append ## Absorbed sections (Key Points + Raw Context), then archive sources."""
    root_full_path, root_vault_rel = resolve_path(root_path)
    if not sources:
        console.print("[red]No source notes provided.[/red]")
        raise typer.Exit(1)
    root_content = read_file(root_path)
    root_stem = Path(root_vault_rel).stem
    source_infos = []
    for s in sources:
        full, vault_rel = resolve_path(s)
        source_content = full.read_text(encoding="utf-8")
        source_infos.append((full, vault_rel, source_content))
    for _, vault_rel, _ in source_infos:
        source_stem = Path(vault_rel).stem
        if f"## Absorbed — [[{source_stem}]]" in root_content:
            console.print(f"[yellow]WARNING: source already appears absorbed — {vault_rel}[/yellow]")
    prompt = load_prompt("summarize-absorbed.md")
    model_string, temp = resolve_model_and_temp(prompt, None)
    blocks = []
    llm_results = []
    for idx, (source_full_path, vault_rel, source_content) in enumerate(source_infos):
        source_stem = Path(vault_rel).stem
        console.print(f"[dim]Summarizing {vault_rel} ({idx + 1}/{len(source_infos)})...[/dim]")
        user_message = f"[NOTE: {vault_rel}]\n{source_content}"
        messages = [
            {"role": "system", "content": prompt["content"]},
            {"role": "user", "content": user_message},
        ]
        _log_llm_call(model_string, temp, "summarize-absorbed.md")
        result = ai_call(model_string, temp, messages)
        if result is None:
            key_points_block = "[WARNING: LLM failed, Key Points skipped]"
        else:
            llm_results.append(result)
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
    if llm_results:
        total_prompt = sum(r["tokens"]["prompt"] for r in llm_results)
        total_completion = sum(r["tokens"]["completion"] for r in llm_results)
        console.print(f"Tokens total: prompt={total_prompt}, completion={total_completion}, total={total_prompt + total_completion}")
    if blocks:
        append_raw_to_file(root_vault_rel, "\n\n" + "\n\n".join(blocks))
        console.print(f"[dim]Appended {len(blocks)} block(s) to {root_vault_rel}[/dim]")
    for source_full_path, vault_rel, source_content in source_infos:
        try:
            new_content = _set_absorbed_frontmatter(source_content, root_stem)
            write_to_path(source_full_path, new_content)
            archive_file(source_full_path, source_full_path.name)
        except Exception as e:
            console.print(f"[red]Archive failed for {vault_rel}: {e}[/red]")
            raise typer.Exit(1)
    console.print(f"Absorbed {len(blocks)} source(s) into {root_vault_rel}")


# ---------------------------------------------------------------------------
# Context (separate user message assembly — no [NOTE], no build_user_message)
# ---------------------------------------------------------------------------


@app.command("context")
def context_cmd(
    file: str = typer.Argument(..., help=PATH_ARG_HELP),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Summarize context block. User message is [CONTEXT: path] + contents only. Appends to context file."""
    full_path, display_path = resolve_path(file)
    content = full_path.read_text(encoding="utf-8")
    user_content = f"[CONTEXT: {display_path}]\n{content}"
    prompt = load_prompt("describe-context.md")
    messages = [{"role": "system", "content": prompt["content"]}, {"role": "user", "content": user_content}]
    model_string, temp = resolve_model_and_temp(prompt, temperature)
    if dry_run:
        print_dry_run_payload(model_string, temp, messages)
        raise typer.Exit(0)
    _log_llm_call(model_string, temp, "describe-context.md")
    result = ai_call(model_string, temp, messages)
    if result is None:
        console.print("[red]LLM call failed; file unchanged.[/red]")
        raise typer.Exit(1)
    append_to_file(full_path, result["content"], "describe-context")
    console.print(f"Tokens: prompt={result['tokens']['prompt']}, completion={result['tokens']['completion']}, total={result['tokens']['total']}")
    console.print(f"Appended to {display_path}")


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        app()
    except FileNotFoundError as e:
        console.print(f"[red]File not found: {e}[/red]")
        raise typer.Exit(1)
