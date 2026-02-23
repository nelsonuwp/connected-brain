"""
LLM Bridge CLI. Vault I/O, archive/snapshot, Typer. All eight commands are LLM operations.
Calls ai_client.call() only; no HTTP logic here.
"""
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import typer
from rich.console import Console

from config import Config
from ai_client import call as ai_call

app = typer.Typer()
console = Console()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_file(vault_relative_path: str) -> str:
    """Read file from VAULT_ROOT / path. UTF-8. Raises on missing file."""
    path = Config.VAULT_ROOT / vault_relative_path
    return path.read_text(encoding="utf-8")


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
    return "\n\n".join(parts)


def append_to_note(note_path: str, llm_output: str, mode: str) -> None:
    """Atomic append: original + --- + ## LLM Output — {mode} — {timestamp} + llm_output. Removes .tmp on exception."""
    full = Config.VAULT_ROOT / note_path
    original = full.read_text(encoding="utf-8")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    section = f"\n\n---\n\n## LLM Output — {mode} — {ts} UTC\n\n{llm_output}"
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
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    section = f"\n\n---\n\n## LLM Output — {mode} — {ts} UTC\n\n{llm_output}"
    new_content = original + section
    tmp_path = full.with_suffix(full.suffix + ".tmp")
    try:
        tmp_path.write_text(new_content, encoding="utf-8")
        os.replace(tmp_path, full)
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


def load_prompt(name: str) -> str:
    """Load prompt file from PROMPTS_ROOT. Raises if missing."""
    path = Config.PROMPTS_ROOT / name
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Idea
# ---------------------------------------------------------------------------

idea_app = typer.Typer()
app.add_typer(idea_app, name="idea")


@idea_app.command("refine")
def idea_refine(
    file: str = typer.Argument(..., help="Vault-relative path, e.g. 01-inbox/foo.md"),
    context: list[str] = typer.Option([], "--context", "-c", help="Context file(s), repeatable"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print payload only"),
    temperature: float | None = typer.Option(None, "--temperature", "-t", help="Override temperature"),
) -> None:
    """Sharpen raw idea. Snapshot, then workhorse, append output."""
    note_content = read_file(file)
    system = load_prompt("refine-idea.md")
    user_msg = build_user_message(note_content, context, file)
    if dry_run:
        console.print("[bold]Dry run — assembled payload[/bold]")
        console.print(f"System prompt: {system[:200]}...")
        console.print(f"User message:\n{user_msg}")
        raise typer.Exit(0)
    snapshot_note_for_llm(file)
    result = ai_call("workhorse", system, user_msg, temperature=temperature, verbose=True)
    if not result:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_to_note(file, result, "refine-idea")
    console.print(f"Appended to {file}")


@idea_app.command("promote")
def idea_promote(
    file: str = typer.Argument(..., help="Vault-relative path, e.g. 01-inbox/foo.md"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """LLM transforms idea → thinking note. Archive original, write new file to 10-thinking/."""
    note_content = read_file(file)
    system = load_prompt("promote-idea-to-thinking.md")
    user_msg = f"[NOTE: {file}]\n{note_content}"
    if dry_run:
        console.print("[bold]Dry run — assembled payload[/bold]")
        console.print(f"System prompt: {system[:200]}...")
        console.print(f"User message:\n{user_msg}")
        raise typer.Exit(0)
    result = ai_call("reasoning", system, user_msg, temperature=temperature, verbose=True)
    if not result:
        console.print("[red]LLM call failed; original untouched.[/red]")
        raise typer.Exit(1)
    filename = Path(file).name
    archive_file(file, filename)
    dest = f"10-thinking/{filename}"
    write_new_file(dest, result)
    archive_path = f"{Path(file).parent}/archive/{filename}"
    console.print(f"Promoted → {dest} (original archived to {archive_path})")


# ---------------------------------------------------------------------------
# Thinking
# ---------------------------------------------------------------------------

thinking_app = typer.Typer()
app.add_typer(thinking_app, name="thinking")


@thinking_app.command("refine")
def thinking_refine(
    file: str = typer.Argument(..., help="Vault-relative path, e.g. 10-thinking/foo.md"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Audit thinking note. Snapshot, workhorse, append."""
    note_content = read_file(file)
    system = load_prompt("refine-thinking.md")
    user_msg = build_user_message(note_content, context, file)
    if dry_run:
        console.print("[bold]Dry run — assembled payload[/bold]")
        console.print(f"User message:\n{user_msg[:500]}...")
        raise typer.Exit(0)
    snapshot_note_for_llm(file)
    result = ai_call("workhorse", system, user_msg, temperature=temperature, verbose=True)
    if not result:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_to_note(file, result, "refine-thinking")
    console.print(f"Appended to {file}")


@thinking_app.command("think")
def thinking_think(
    file: str = typer.Argument(..., help="Vault-relative path, e.g. 10-thinking/foo.md"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Deep thinking. No snapshot — accumulation is intentional. Reasoning model, append."""
    note_content = read_file(file)
    system = load_prompt("think-mode.md")
    user_msg = build_user_message(note_content, context, file)
    if dry_run:
        console.print("[bold]Dry run — assembled payload[/bold]")
        console.print(f"User message:\n{user_msg[:500]}...")
        raise typer.Exit(0)
    result = ai_call("reasoning", system, user_msg, temperature=temperature, verbose=True)
    if not result:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_to_note(file, result, "think")
    console.print(f"Appended to {file}")


@thinking_app.command("spec")
def thinking_spec(
    file: str = typer.Argument(..., help="Vault-relative path, e.g. 10-thinking/foo.md"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Generate initiative spec content. Snapshot, reasoning, append."""
    note_content = read_file(file)
    system = load_prompt("specify-mode.md")
    user_msg = build_user_message(note_content, context, file)
    if dry_run:
        console.print("[bold]Dry run — assembled payload[/bold]")
        console.print(f"User message:\n{user_msg[:500]}...")
        raise typer.Exit(0)
    snapshot_note_for_llm(file)
    result = ai_call("reasoning", system, user_msg, temperature=temperature, verbose=True)
    if not result:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_to_note(file, result, "spec")
    console.print(f"Appended to {file}")


@thinking_app.command("promote")
def thinking_promote(
    file: str = typer.Argument(..., help="Vault-relative path, e.g. 10-thinking/foo.md"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """LLM transforms thinking → initiative. Archive original, write new file to 30-initiatives/."""
    note_content = read_file(file)
    system = load_prompt("promote-thinking-to-initiative.md")
    user_msg = f"[NOTE: {file}]\n{note_content}"
    if dry_run:
        console.print("[bold]Dry run — assembled payload[/bold]")
        console.print(f"User message:\n{user_msg[:500]}...")
        raise typer.Exit(0)
    result = ai_call("reasoning", system, user_msg, temperature=temperature, verbose=True)
    if not result:
        console.print("[red]LLM call failed; original untouched.[/red]")
        raise typer.Exit(1)
    filename = Path(file).name
    archive_file(file, filename)
    dest = f"30-initiatives/{filename}"
    write_new_file(dest, result)
    archive_path = f"{Path(file).parent}/archive/{filename}"
    console.print(f"Promoted → {dest} (original archived to {archive_path})")


# ---------------------------------------------------------------------------
# Initiative
# ---------------------------------------------------------------------------

initiative_app = typer.Typer()
app.add_typer(initiative_app, name="initiative")


@initiative_app.command("refine")
def initiative_refine(
    file: str = typer.Argument(..., help="Vault-relative path, e.g. 30-initiatives/foo.md"),
    context: list[str] = typer.Option([], "--context", "-c"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Audit initiative spec. Snapshot, workhorse, append."""
    note_content = read_file(file)
    system = load_prompt("refine-initiative.md")
    user_msg = build_user_message(note_content, context, file)
    if dry_run:
        console.print("[bold]Dry run — assembled payload[/bold]")
        console.print(f"User message:\n{user_msg[:500]}...")
        raise typer.Exit(0)
    snapshot_note_for_llm(file)
    result = ai_call("workhorse", system, user_msg, temperature=temperature, verbose=True)
    if not result:
        console.print("[red]LLM call failed; note unchanged.[/red]")
        raise typer.Exit(1)
    append_to_note(file, result, "refine-initiative")
    console.print(f"Appended to {file}")


# ---------------------------------------------------------------------------
# Context (separate user message assembly — no [NOTE], no build_user_message)
# ---------------------------------------------------------------------------


@app.command("context")
def context_cmd(
    file: str = typer.Argument(..., help="Vault-relative path to context file"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    temperature: float | None = typer.Option(None, "--temperature", "-t"),
) -> None:
    """Summarize context block. User message is [CONTEXT: path] + contents only. Appends to context file."""
    content = read_file(file)
    user_msg = f"[CONTEXT: {file}]\n{content}"
    system = load_prompt("describe-context.md")
    if dry_run:
        console.print("[bold]Dry run — assembled payload[/bold]")
        console.print(f"User message:\n{user_msg[:500]}...")
        raise typer.Exit(0)
    result = ai_call("nano", system, user_msg, temperature=temperature, verbose=True)
    if not result:
        console.print("[red]LLM call failed; file unchanged.[/red]")
        raise typer.Exit(1)
    append_to_file(file, result, "describe-context")
    console.print(f"Appended to {file}")


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        app()
    except FileNotFoundError as e:
        console.print(f"[red]File not found: {e}[/red]")
        raise typer.Exit(1)
