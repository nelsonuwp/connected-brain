"""
Tests for brain.py. Uses a temporary vault (VAULT_ROOT env) so the real vault is untouched.
Expected terminal output and filesystem state documented per test.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import typer

# Success/failure mock shapes for ai_client.call (brain imports it as ai_call)
FAKE_TOKENS = {"prompt": 10, "completion": 50, "total": 60}


def _success_mock(content: str) -> dict:
    return {"content": content, "tokens": FAKE_TOKENS}

# Set VAULT_ROOT to a temp dir before importing brain (which imports config).
# pytest runs with workspace as cwd; we'll set env in fixtures.
TESTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TESTS_DIR
REPO_ROOT = TESTS_DIR.parent.parent  # connected-brain
DEFAULT_VAULT = REPO_ROOT / "vault"
DEFAULT_PROMPTS = DEFAULT_VAULT / "_prompts"


@pytest.fixture(scope="module")
def temp_vault(tmp_path_factory):
    """Create a temporary vault with minimal structure and prompt files."""
    vault = tmp_path_factory.mktemp("vault")
    (vault / "01-inbox").mkdir()
    (vault / "10-thinking").mkdir()
    (vault / "30-initiatives").mkdir()
    (vault / "20-context").mkdir(parents=True)
    prompts_dir = vault / "_prompts"
    prompts_dir.mkdir()
    # Copy or create minimal prompt files so load_prompt works
    for name in [
        "refine-idea.md",
        "promote-idea-to-thinking.md",
        "refine-thinking.md",
        "think-mode.md",
        "specify-mode.md",
        "promote-thinking-to-initiative.md",
        "refine-initiative.md",
        "describe-context.md",
    ]:
        src = DEFAULT_PROMPTS / name
        if src.exists():
            (prompts_dir / name).write_text(src.read_text(), encoding="utf-8")
        elif name == "think-mode.md":
            # At least one fixture with valid YAML frontmatter for load_prompt/waterfall tests
            (prompts_dir / name).write_text(
                "---\nmodel: reasoning\ntemperature: reasoning\n---\nYou are a thinking partner.\n",
                encoding="utf-8",
            )
        else:
            (prompts_dir / name).write_text(f"System prompt: {name}\n", encoding="utf-8")
    return vault


@pytest.fixture
def env_with_vault(temp_vault, monkeypatch):
    """Set VAULT_ROOT to temp vault and ensure OPENROUTER_API_KEY is set (for import)."""
    monkeypatch.setenv("VAULT_ROOT", str(temp_vault))
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test-dummy")  # so config passes
    return temp_vault


def _run_brain(env: dict, *args: str) -> subprocess.CompletedProcess:
    """Run brain.py with given env and args. Env should include VAULT_ROOT and optionally OPENROUTER_API_KEY."""
    cmd = [sys.executable, str(PROJECT_DIR / "brain.py")] + list(args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(PROJECT_DIR),
        env={**os.environ, **env},
    )


# ---- Promote: idea promote ----
# Expected (dry-run): prints payload, no archive, no file in 10-thinking/.
# Expected (live+mock): 01-inbox/archive/<file> = original, 10-thinking/<file> = LLM output.
# Expected (API failure): original untouched, no archive, no 10-thinking/ file.


def test_idea_promote_dry_run(env_with_vault):
    """
    Expected terminal: exact JSON payload (model, temperature, max_tokens, messages).
    Expected filesystem: 01-inbox/test-idea.md still exists, no 01-inbox/archive/, no 10-thinking/.
    """
    vault = env_with_vault
    (vault / "01-inbox" / "test-idea.md").write_text("My raw idea\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "idea", "promote", "01-inbox/test-idea.md", "--dry-run",
    )
    assert result.returncode == 0
    assert "[NOTE:" in result.stdout
    parsed = json.loads(result.stdout)
    assert "model" in parsed
    assert "temperature" in parsed
    assert "max_tokens" in parsed
    assert "messages" in parsed
    assert len(parsed["messages"]) == 2
    assert parsed["messages"][0]["role"] == "system"
    assert parsed["messages"][1]["role"] == "user"
    assert (vault / "01-inbox" / "test-idea.md").exists()
    assert not (vault / "01-inbox" / "archive").exists()
    assert not (vault / "10-thinking" / "test-idea.md").exists()


def test_idea_promote_live_mocked(env_with_vault):
    """
    Mock ai_client.call to return transport dict. Run idea promote.
    Expected terminal: "Promoted → 10-thinking/test-idea.md (original archived to ...)".
    Expected filesystem: 01-inbox/archive/test-idea.md = original content; 10-thinking/test-idea.md = mock LLM output.
    """
    vault = env_with_vault
    (vault / "01-inbox" / "test-idea.md").write_text("My raw idea\n", encoding="utf-8")
    fake_output = "---\ntype: thinking\nstatus: raw\n---\n# Test\n## The Idea\nFake.\n"

    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock(fake_output)):
        import brain as brain_mod
        from typer.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "promote", "01-inbox/test-idea.md"], env=env)
    assert result.exit_code == 0
    assert "Promoted" in result.output
    assert (vault / "01-inbox" / "archive" / "test-idea.md").read_text() == "My raw idea\n"
    assert (vault / "10-thinking" / "test-idea.md").read_text() == fake_output


def test_idea_promote_api_failure(env_with_vault):
    """
    Mock ai_client.call to return None (failure). Run idea promote.
    Expected terminal: "LLM call failed; original untouched."
    Expected filesystem: original file unchanged, no archive of *this* file, no 10-thinking/ file.
    """
    vault = env_with_vault
    unique = "idea-promote-fail.md"
    (vault / "01-inbox" / unique).write_text("My raw idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=None):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "promote", f"01-inbox/{unique}"], env=env)
    assert result.exit_code == 1
    assert "unchanged" in result.output or "failed" in result.output.lower()
    assert (vault / "01-inbox" / unique).read_text() == "My raw idea\n"
    assert not (vault / "01-inbox" / "archive" / unique).exists()
    assert not (vault / "10-thinking" / unique).exists()


# ---- Promote: thinking promote ----


def test_thinking_promote_dry_run(env_with_vault):
    """Expected: JSON payload on stdout, no archive, no 30-initiatives/ file."""
    vault = env_with_vault
    (vault / "10-thinking" / "test-thinking.md").write_text("Thinking content\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "thinking", "promote", "10-thinking/test-thinking.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)  # dry-run outputs valid JSON
    assert (vault / "10-thinking" / "test-thinking.md").exists()
    assert not (vault / "10-thinking" / "archive").exists()
    assert not (vault / "30-initiatives" / "test-thinking.md").exists()


def test_thinking_promote_live_mocked(env_with_vault):
    """Expected: Promoted message; 10-thinking/archive/test-thinking.md = original; 30-initiatives/test-thinking.md = LLM output."""
    vault = env_with_vault
    (vault / "10-thinking" / "test-thinking.md").write_text("Thinking content\n", encoding="utf-8")
    fake = "---\ntype: initiative\nstatus: drafting\n---\n# Test\n## One-Line Purpose\nFake.\n"
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock(fake)):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["thinking", "promote", "10-thinking/test-thinking.md"], env=env)
    assert result.exit_code == 0
    assert "Promoted" in result.output
    assert (vault / "10-thinking" / "archive" / "test-thinking.md").read_text() == "Thinking content\n"
    assert (vault / "30-initiatives" / "test-thinking.md").read_text() == fake


# ---- Dry-run for every LLM command ----


def test_idea_refine_dry_run(env_with_vault):
    """Expected: JSON payload on stdout, no snapshot, no append."""
    vault = env_with_vault
    (vault / "01-inbox" / "foo.md").write_text("Idea\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "idea", "refine", "01-inbox/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)
    assert (vault / "01-inbox" / "foo.md").read_text() == "Idea\n"
    archive_dir = vault / "01-inbox" / "archive"
    assert not list(archive_dir.glob("foo-*.md")) if archive_dir.exists() else True


def test_thinking_refine_dry_run(env_with_vault):
    """Expected: JSON payload on stdout, no write."""
    vault = env_with_vault
    (vault / "10-thinking" / "foo.md").write_text("Thinking\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "thinking", "refine", "10-thinking/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)


def test_thinking_think_dry_run(env_with_vault):
    """Expected: JSON payload on stdout, no write."""
    vault = env_with_vault
    (vault / "10-thinking" / "foo.md").write_text("Thinking\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "thinking", "think", "10-thinking/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)


def test_thinking_spec_dry_run(env_with_vault):
    """Expected: JSON payload on stdout, no write."""
    vault = env_with_vault
    (vault / "10-thinking" / "foo.md").write_text("Thinking\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "thinking", "spec", "10-thinking/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)


def test_initiative_refine_dry_run(env_with_vault):
    """Expected: JSON payload on stdout, no write."""
    vault = env_with_vault
    (vault / "30-initiatives" / "foo.md").write_text("Initiative\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "initiative", "refine", "30-initiatives/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)


def test_context_dry_run(env_with_vault):
    """Expected: JSON payload; user message has [CONTEXT: ...]. No append."""
    vault = env_with_vault
    (vault / "20-context" / "bar.md").write_text("Context content\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "context", "20-context/bar.md", "--dry-run",
    )
    assert result.returncode == 0
    parsed = json.loads(result.stdout)
    assert "[CONTEXT:" in (parsed["messages"][1]["content"] if len(parsed["messages"]) > 1 else "")
    assert (vault / "20-context" / "bar.md").read_text() == "Context content\n"


# ---- Snapshot behavior ----


def test_thinking_refine_creates_snapshot(env_with_vault):
    """
    Run thinking refine with mocked API. Expect 10-thinking/archive/<stem>-<timestamp>.md to exist with pre-call content.
    """
    vault = env_with_vault
    (vault / "10-thinking" / "snap-note.md").write_text("Before refine\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("## Audit\n### What's Solid\nNone.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["thinking", "refine", "10-thinking/snap-note.md"], env=env)
    assert result.exit_code == 0
    archive_dir = vault / "10-thinking" / "archive"
    assert archive_dir.exists()
    archives = list(archive_dir.glob("snap-note-*.md"))
    assert len(archives) == 1
    assert archives[0].read_text() == "Before refine\n"
    full_note = (vault / "10-thinking" / "snap-note.md").read_text()
    assert "## LLM Output" in full_note
    assert "Before refine" in full_note


def test_thinking_think_does_not_snapshot(env_with_vault):
    """
    Run thinking think with mocked API. Expect NO new file in 10-thinking/archive/ from this run; only the note was appended to.
    """
    vault = env_with_vault
    (vault / "10-thinking" / "think-note.md").write_text("Before think\n", encoding="utf-8")
    archive_dir = vault / "10-thinking" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("## Think\n### The Central Tension\nFake.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["thinking", "think", "10-thinking/think-note.md"], env=env)
    assert result.exit_code == 0
    think_archives = list(archive_dir.glob("think-note-*.md"))
    assert len(think_archives) == 0
    full = (vault / "10-thinking" / "think-note.md").read_text()
    assert "## LLM Output" in full
    assert "Before think" in full


# ---- Failure cases ----


def test_missing_file(env_with_vault):
    """
    Run idea refine on nonexistent file.
    Expected terminal: "File not found" or similar, exit non-zero.
    Expected filesystem: no new files.
    """
    result = _run_brain(
        {"VAULT_ROOT": str(env_with_vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "idea", "refine", "01-inbox/nonexistent.md",
    )
    assert result.returncode != 0
    assert "not found" in result.stdout.lower() or "not found" in result.stderr.lower()


def test_missing_api_key(temp_vault):
    """
    Run any LLM command with OPENROUTER_API_KEY empty so config validation fails.
    Expected: process exits with message about OPENROUTER_API_KEY (config validation).
    Use subprocess; pass OPENROUTER_API_KEY="" to override inherited env.
    """
    env = {**os.environ, "VAULT_ROOT": str(temp_vault), "OPENROUTER_API_KEY": ""}
    (temp_vault / "01-inbox" / "x.md").write_text("x\n", encoding="utf-8")
    result = _run_brain(env, "idea", "refine", "01-inbox/x.md")
    assert result.returncode != 0
    assert "OPENROUTER_API_KEY" in result.stderr or "OPENROUTER_API_KEY" in result.stdout


# Alias validation moved to brain.py resolution waterfall. ai_client accepts full model
# strings only — invalid strings go to OpenRouter and return HTTP errors handled by
# existing retry/failure tests. test_bad_model_alias removed; to test unknown frontmatter
# alias, use a stub prompt with model: invalid_alias and assert brain errors without
# calling ai_client.


# ---- load_prompt and build_user_message ----


def test_load_prompt_missing_file(env_with_vault):
    """load_prompt with nonexistent file raises typer.Exit(1)."""
    vault = env_with_vault
    with patch("brain.Config.PROMPTS_ROOT", vault / "_prompts"):
        import brain as brain_mod
        with pytest.raises(typer.Exit) as exc_info:
            brain_mod.load_prompt("nonexistent.md")
        assert exc_info.value.exit_code == 1


def test_load_prompt_no_frontmatter(env_with_vault):
    """File with no --- block returns content as body, model and temperature None."""
    vault = env_with_vault
    (vault / "_prompts" / "no-fm.md").write_text("Just content\n", encoding="utf-8")
    with patch("brain.Config.PROMPTS_ROOT", vault / "_prompts"):
        import brain as brain_mod
        out = brain_mod.load_prompt("no-fm.md")
    assert out["content"] == "Just content\n"
    assert out["model"] is None
    assert out["temperature"] is None


def test_load_prompt_with_frontmatter(env_with_vault):
    """File with valid frontmatter returns parsed body and model/temperature aliases."""
    vault = env_with_vault
    # think-mode.md in fixture has frontmatter
    with patch("brain.Config.PROMPTS_ROOT", vault / "_prompts"):
        import brain as brain_mod
        out = brain_mod.load_prompt("think-mode.md")
    assert "thinking partner" in out["content"]
    assert out["model"] == "reasoning"
    assert out["temperature"] == "reasoning"


def test_build_user_message_separator(env_with_vault):
    """Assembled user message uses \\n\\n---\\n\\n between [CONTEXT] and [NOTE] blocks."""
    vault = env_with_vault
    (vault / "20-context" / "ctx.md").write_text("ctx body", encoding="utf-8")
    with patch("brain.Config.VAULT_ROOT", vault):
        import brain as brain_mod
        result = brain_mod.build_user_message(
            "note body",
            ["20-context/ctx.md"],
            "10-thinking/foo.md",
        )
    assert "[CONTEXT: 20-context/ctx.md]" in result
    assert "[NOTE: 10-thinking/foo.md]" in result
    assert "\n\n---\n\n" in result
    # Separator should appear between context and note
    assert result.index("[NOTE:") > result.index("---")
