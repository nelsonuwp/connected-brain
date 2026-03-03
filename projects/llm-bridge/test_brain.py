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
    for name in [
        "critique-idea.md",
        "critique-thinking.md",
        "critique-initiative.md",
        "explore.md",
        "normalize.md",
        "promote-idea-to-thinking.md",
        "promote-thinking-to-initiative.md",
        "specify-mode.md",
        "describe-context.md",
        "summarize-absorbed.md",  # required for absorb tests
    ]:
        src = DEFAULT_PROMPTS / name
        if src.exists():
            (prompts_dir / name).write_text(src.read_text(), encoding="utf-8")
        elif name == "explore.md":
            (prompts_dir / name).write_text(
                "---\nmodel: reasoning\ntemperature: reasoning\n---\nYou are a thinking partner.\n",
                encoding="utf-8",
            )
        elif name == "summarize-absorbed.md":
            (prompts_dir / name).write_text(
                "---\nmodel: workhorse\ntemperature: workhorse\n---\n"
                "Summarize the provided note into 3-5 bullet points highlighting key insights, "
                "constraints, and decisions. Output markdown bullet list only, no preamble.\n",
                encoding="utf-8",
            )
        else:
            (prompts_dir / name).write_text(f"System prompt: {name}\n", encoding="utf-8")
    return vault


@pytest.fixture
def env_with_vault(temp_vault, monkeypatch):
    """Set VAULT_ROOT to temp vault and ensure OPENROUTER_API_KEY is set (for import)."""
    monkeypatch.setenv("VAULT_ROOT", str(temp_vault))
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test-dummy")
    return temp_vault


def _run_brain(env: dict, *args: str) -> subprocess.CompletedProcess:
    """Run brain.py with given env and args."""
    cmd = [sys.executable, str(PROJECT_DIR / "brain.py")] + list(args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(PROJECT_DIR),
        env={**os.environ, **env},
    )


# ---------------------------------------------------------------------------
# Existing: Promote — idea
# ---------------------------------------------------------------------------

def test_idea_promote_dry_run(env_with_vault):
    """Expected: JSON payload, no archive, no 10-thinking/ file."""
    vault = env_with_vault
    (vault / "01-inbox" / "test-idea.md").write_text("My raw idea\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "idea", "promote", "01-inbox/test-idea.md", "--dry-run",
    )
    assert result.returncode == 0
    parsed = json.loads(result.stdout)
    assert "model" in parsed
    assert "messages" in parsed
    assert (vault / "01-inbox" / "test-idea.md").exists()
    assert not (vault / "01-inbox" / "archive").exists()
    assert not (vault / "10-thinking" / "test-idea.md").exists()


def test_idea_promote_live_mocked(env_with_vault):
    """Mock API. Archived original has status: promoted; new thinking note has LLM content."""
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
    # New file has LLM content
    assert (vault / "10-thinking" / "test-idea.md").read_text() == fake_output
    # Archived original has status: promoted
    archived = (vault / "01-inbox" / "archive" / "test-idea.md").read_text()
    assert "status: promoted" in archived


def test_idea_promote_api_failure(env_with_vault):
    """Mock returns None. Original untouched, no archive, no thinking file."""
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


# ---------------------------------------------------------------------------
# Existing: Promote — thinking
# ---------------------------------------------------------------------------

def test_thinking_promote_dry_run(env_with_vault):
    """Expected: JSON payload, no archive, no 30-initiatives/ file."""
    vault = env_with_vault
    (vault / "10-thinking" / "test-thinking.md").write_text("Thinking content\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "thinking", "promote", "10-thinking/test-thinking.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)
    assert (vault / "10-thinking" / "test-thinking.md").exists()
    assert not (vault / "10-thinking" / "archive").exists()


def test_thinking_promote_live_mocked(env_with_vault):
    """Mock API. Archived original has status: promoted; new initiative spec has LLM content."""
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
    # New initiative spec has LLM content
    assert (vault / "30-initiatives" / "drafting" / "test-thinking.md").read_text() == fake
    # Archived original has status: promoted
    archived = (vault / "10-thinking" / "archive" / "test-thinking.md").read_text()
    assert "status: promoted" in archived


# ---------------------------------------------------------------------------
# New: status on promote — no-frontmatter edge case
# ---------------------------------------------------------------------------

def test_idea_promote_archived_gets_promoted_status_no_frontmatter(env_with_vault):
    """Idea with no frontmatter at all still gets status: promoted in archive."""
    vault = env_with_vault
    (vault / "01-inbox" / "bare-idea.md").write_text("Just text, no frontmatter\n", encoding="utf-8")
    fake_output = "---\ntype: thinking\nstatus: raw\n---\nFake.\n"
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock(fake_output)):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        runner.invoke(brain_mod.app, ["idea", "promote", "01-inbox/bare-idea.md"], env=env)
    archived = (vault / "01-inbox" / "archive" / "bare-idea.md").read_text()
    assert "status: promoted" in archived


# ---------------------------------------------------------------------------
# New: console logging — context loaded confirmation
# ---------------------------------------------------------------------------

def test_context_loaded_message_printed(env_with_vault):
    """When --context is passed, output confirms 'Context loaded: <path>'."""
    vault = env_with_vault
    ctx_file = vault / "20-context" / "myctx.md"
    ctx_file.write_text("Some context\n", encoding="utf-8")
    (vault / "01-inbox" / "ctxtest.md").write_text("Idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("Result.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(
            brain_mod.app,
            ["idea", "critique", "01-inbox/ctxtest.md", "--context", "20-context/myctx.md"],
            env=env,
        )
    assert result.exit_code == 0
    assert "Context loaded" in result.output
    assert "myctx.md" in result.output


def test_no_context_loaded_message_when_no_context(env_with_vault):
    """When no --context flag, 'Context loaded' should NOT appear in output."""
    vault = env_with_vault
    (vault / "01-inbox" / "noctx.md").write_text("Idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("Result.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "critique", "01-inbox/noctx.md"], env=env)
    assert result.exit_code == 0
    assert "Context loaded" not in result.output


def test_multiple_context_files_all_logged(env_with_vault):
    """Two --context files: both show 'Context loaded' lines."""
    vault = env_with_vault
    (vault / "20-context" / "ctx1.md").write_text("Context 1\n", encoding="utf-8")
    (vault / "20-context" / "ctx2.md").write_text("Context 2\n", encoding="utf-8")
    (vault / "01-inbox" / "multi-ctx.md").write_text("Idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("Result.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(
            brain_mod.app,
            ["idea", "critique", "01-inbox/multi-ctx.md",
             "--context", "20-context/ctx1.md",
             "--context", "20-context/ctx2.md"],
            env=env,
        )
    assert result.exit_code == 0
    assert result.output.count("Context loaded") == 2
    assert "ctx1.md" in result.output
    assert "ctx2.md" in result.output


# ---------------------------------------------------------------------------
# New: console logging — model resolution printed before LLM call
# ---------------------------------------------------------------------------

def test_model_resolution_logged(env_with_vault):
    """LLM commands print model string and temperature before calling API."""
    vault = env_with_vault
    (vault / "01-inbox" / "logtest.md").write_text("Idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("Result.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "critique", "01-inbox/logtest.md"], env=env)
    assert result.exit_code == 0
    # Should show model name and temp somewhere in output
    assert "temp=" in result.output or "temperature" in result.output.lower()
    # Should show the prompt name
    assert "critique-idea.md" in result.output


def test_token_count_printed_on_success(env_with_vault):
    """After successful LLM call, token counts appear in output."""
    vault = env_with_vault
    (vault / "01-inbox" / "tokentest.md").write_text("Idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("Result.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "critique", "01-inbox/tokentest.md"], env=env)
    assert result.exit_code == 0
    assert "prompt=10" in result.output
    assert "completion=50" in result.output
    assert "total=60" in result.output


# ---------------------------------------------------------------------------
# New: Absorb — core behavior
# ---------------------------------------------------------------------------

def test_absorb_no_sources_exits_1(env_with_vault):
    """brain absorb root.md with no sources exits 1."""
    vault = env_with_vault
    (vault / "10-thinking" / "root.md").write_text("Root\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "absorb", "10-thinking/root.md",
    )
    assert result.returncode == 1


def test_absorb_missing_root_exits_1(env_with_vault):
    """brain absorb with nonexistent root exits 1."""
    vault = env_with_vault
    (vault / "01-inbox" / "src.md").write_text("Source\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "absorb", "10-thinking/missing-root.md", "01-inbox/src.md",
    )
    assert result.returncode == 1


def test_absorb_missing_source_exits_1(env_with_vault):
    """brain absorb with nonexistent source exits 1."""
    vault = env_with_vault
    (vault / "10-thinking" / "root2.md").write_text("Root\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "absorb", "10-thinking/root2.md", "01-inbox/missing-source.md",
    )
    assert result.returncode == 1


def test_absorb_appends_absorbed_section(env_with_vault):
    """Single source: root gets ## Absorbed section with Key Points and Raw Context."""
    vault = env_with_vault
    (vault / "10-thinking" / "absorb-root.md").write_text(
        "---\ntype: thinking\nstatus: raw\n---\nRoot content\n", encoding="utf-8"
    )
    (vault / "01-inbox" / "absorb-src.md").write_text(
        "---\ntype: idea\nstatus: raw\n---\nSource content\n", encoding="utf-8"
    )
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("- Key point 1\n- Key point 2")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(
            brain_mod.app,
            ["absorb", "10-thinking/absorb-root.md", "01-inbox/absorb-src.md"],
            env=env,
        )
    assert result.exit_code == 0
    root_text = (vault / "10-thinking" / "absorb-root.md").read_text()
    assert "## Absorbed — [[absorb-src]]" in root_text
    assert "### Key Points" in root_text
    assert "- Key point 1" in root_text
    assert "### Raw Context" in root_text
    assert "Source content" in root_text


def test_absorb_root_frontmatter_unchanged(env_with_vault):
    """Root note frontmatter is byte-identical before and after absorb."""
    vault = env_with_vault
    root_content = "---\ntype: thinking\nstatus: raw\n---\nRoot body\n"
    (vault / "10-thinking" / "fm-root.md").write_text(root_content, encoding="utf-8")
    (vault / "01-inbox" / "fm-src.md").write_text("Source body\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("- Point")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        runner.invoke(
            brain_mod.app,
            ["absorb", "10-thinking/fm-root.md", "01-inbox/fm-src.md"],
            env=env,
        )
    after = (vault / "10-thinking" / "fm-root.md").read_text()
    # Original content still present and unchanged at the start
    assert after.startswith(root_content)


def test_absorb_source_archived_with_correct_status(env_with_vault):
    """Source is moved to archive with status: absorbed to [[root_stem]]."""
    vault = env_with_vault
    (vault / "10-thinking" / "status-root.md").write_text("Root\n", encoding="utf-8")
    (vault / "01-inbox" / "status-src.md").write_text(
        "---\ntype: idea\nstatus: raw\n---\nSrc body\n", encoding="utf-8"
    )
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("- Point")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        runner.invoke(
            brain_mod.app,
            ["absorb", "10-thinking/status-root.md", "01-inbox/status-src.md"],
            env=env,
        )
    # Source no longer in original location
    assert not (vault / "01-inbox" / "status-src.md").exists()
    # Source is in archive with correct status
    archived = (vault / "01-inbox" / "archive" / "status-src.md").read_text()
    assert "absorbed to [[status-root]]" in archived


def test_absorb_multi_source(env_with_vault):
    """Two sources: root gets two ## Absorbed sections; both sources archived."""
    vault = env_with_vault
    (vault / "10-thinking" / "multi-root.md").write_text("Root\n", encoding="utf-8")
    (vault / "01-inbox" / "multi-s1.md").write_text("Source 1\n", encoding="utf-8")
    (vault / "01-inbox" / "multi-s2.md").write_text("Source 2\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("- Point")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(
            brain_mod.app,
            ["absorb", "10-thinking/multi-root.md", "01-inbox/multi-s1.md", "01-inbox/multi-s2.md"],
            env=env,
        )
    assert result.exit_code == 0
    root_text = (vault / "10-thinking" / "multi-root.md").read_text()
    assert root_text.count("## Absorbed") == 2
    assert "[[multi-s1]]" in root_text
    assert "[[multi-s2]]" in root_text
    assert not (vault / "01-inbox" / "multi-s1.md").exists()
    assert not (vault / "01-inbox" / "multi-s2.md").exists()
    assert (vault / "01-inbox" / "archive" / "multi-s1.md").exists()
    assert (vault / "01-inbox" / "archive" / "multi-s2.md").exists()


def test_absorb_llm_failure_fallback(env_with_vault):
    """When LLM fails, fallback warning appears in Key Points; command still completes and archives source."""
    vault = env_with_vault
    (vault / "10-thinking" / "fallback-root.md").write_text("Root\n", encoding="utf-8")
    (vault / "01-inbox" / "fallback-src.md").write_text("Source\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=None):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(
            brain_mod.app,
            ["absorb", "10-thinking/fallback-root.md", "01-inbox/fallback-src.md"],
            env=env,
        )
    assert result.exit_code == 0
    root_text = (vault / "10-thinking" / "fallback-root.md").read_text()
    assert "[WARNING: LLM failed, Key Points skipped]" in root_text
    assert "### Raw Context" in root_text
    # Source still archived despite LLM failure
    assert (vault / "01-inbox" / "archive" / "fallback-src.md").exists()


def test_absorb_duplicate_warning(env_with_vault):
    """Absorbing same source twice prints WARNING but proceeds."""
    vault = env_with_vault
    (vault / "10-thinking" / "dup-root.md").write_text("Root\n", encoding="utf-8")
    (vault / "01-inbox" / "dup-src.md").write_text("Source\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    # First absorb
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("- Point")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        runner.invoke(
            brain_mod.app,
            ["absorb", "10-thinking/dup-root.md", "01-inbox/dup-src.md"],
            env=env,
        )
    # Restore source for second absorb
    (vault / "01-inbox" / "dup-src.md").write_text("Source\n", encoding="utf-8")
    # Second absorb — should warn
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("- Point")):
        result = runner.invoke(
            brain_mod.app,
            ["absorb", "10-thinking/dup-root.md", "01-inbox/dup-src.md"],
            env=env,
        )
    assert "WARNING" in result.output
    assert "absorbed" in result.output.lower()


def test_absorb_progress_logged(env_with_vault):
    """Absorb with two sources prints per-source progress and token counts."""
    vault = env_with_vault
    (vault / "10-thinking" / "prog-root.md").write_text("Root\n", encoding="utf-8")
    (vault / "01-inbox" / "prog-s1.md").write_text("Source 1\n", encoding="utf-8")
    (vault / "01-inbox" / "prog-s2.md").write_text("Source 2\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("- Point")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(
            brain_mod.app,
            ["absorb", "10-thinking/prog-root.md", "01-inbox/prog-s1.md", "01-inbox/prog-s2.md"],
            env=env,
        )
    assert result.exit_code == 0
    # Per-source progress (e.g. "1/2", "2/2")
    assert "1/2" in result.output
    assert "2/2" in result.output
    # Token counts appear (two LLM calls = two token lines)
    assert result.output.count("prompt=10") == 2
    # Final aggregate token line
    assert "Tokens total" in result.output
    # Final summary
    assert "Absorbed 2 source(s)" in result.output


# ---------------------------------------------------------------------------
# Existing: dry-run for every LLM command
# ---------------------------------------------------------------------------

def test_idea_critique_dry_run(env_with_vault):
    vault = env_with_vault
    (vault / "01-inbox" / "foo.md").write_text("Idea\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "idea", "critique", "01-inbox/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)
    assert (vault / "01-inbox" / "foo.md").read_text() == "Idea\n"


def test_thinking_critique_dry_run(env_with_vault):
    vault = env_with_vault
    (vault / "10-thinking" / "foo.md").write_text("Thinking\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "thinking", "critique", "10-thinking/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)


def test_thinking_explore_dry_run(env_with_vault):
    vault = env_with_vault
    (vault / "10-thinking" / "foo.md").write_text("Thinking\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "thinking", "explore", "10-thinking/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)


def test_thinking_spec_dry_run(env_with_vault):
    vault = env_with_vault
    (vault / "10-thinking" / "foo.md").write_text("Thinking\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "thinking", "spec", "10-thinking/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)


def test_initiative_critique_dry_run(env_with_vault):
    vault = env_with_vault
    (vault / "30-initiatives" / "foo.md").write_text("Initiative\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "initiative", "critique", "30-initiatives/foo.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)


def test_context_dry_run(env_with_vault):
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


# ---------------------------------------------------------------------------
# Existing: critique/explore append behavior
# ---------------------------------------------------------------------------

def test_thinking_critique_appends_critique_section(env_with_vault):
    vault = env_with_vault
    (vault / "10-thinking" / "snap-note.md").write_text("Before critique\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("## Audit\n### What's Solid\nNone.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["thinking", "critique", "10-thinking/snap-note.md"], env=env)
    assert result.exit_code == 0
    full_note = (vault / "10-thinking" / "snap-note.md").read_text()
    assert "# Critique" in full_note
    assert "Before critique" in full_note
    archive_dir = vault / "10-thinking" / "archive"
    if archive_dir.exists():
        assert len(list(archive_dir.glob("snap-note-*.md"))) == 0


def test_thinking_explore_does_not_snapshot(env_with_vault):
    vault = env_with_vault
    (vault / "10-thinking" / "think-note.md").write_text("Before explore\n", encoding="utf-8")
    archive_dir = vault / "10-thinking" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("## Explore\n### The Central Tension\nFake.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["thinking", "explore", "10-thinking/think-note.md"], env=env)
    assert result.exit_code == 0
    assert len(list(archive_dir.glob("think-note-*.md"))) == 0
    full = (vault / "10-thinking" / "think-note.md").read_text()
    assert "# Explore" in full
    assert "Before explore" in full


# ---------------------------------------------------------------------------
# Existing: failure cases
# ---------------------------------------------------------------------------

def test_missing_file(env_with_vault):
    result = _run_brain(
        {"VAULT_ROOT": str(env_with_vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "idea", "critique", "01-inbox/nonexistent.md",
    )
    assert result.returncode != 0
    assert "not found" in result.stdout.lower() or "not found" in result.stderr.lower()


def test_missing_api_key(temp_vault):
    env = {**os.environ, "VAULT_ROOT": str(temp_vault), "OPENROUTER_API_KEY": ""}
    (temp_vault / "01-inbox" / "x.md").write_text("x\n", encoding="utf-8")
    result = _run_brain(env, "idea", "critique", "01-inbox/x.md")
    assert result.returncode != 0
    assert "OPENROUTER_API_KEY" in result.stderr or "OPENROUTER_API_KEY" in result.stdout


# ---------------------------------------------------------------------------
# Existing: load_prompt and build_user_message
# ---------------------------------------------------------------------------

def test_load_prompt_missing_file(env_with_vault):
    vault = env_with_vault
    with patch("brain.Config.PROMPTS_ROOT", vault / "_prompts"):
        import brain as brain_mod
        with pytest.raises(typer.Exit) as exc_info:
            brain_mod.load_prompt("nonexistent.md")
        assert exc_info.value.exit_code == 1


def test_load_prompt_no_frontmatter(env_with_vault):
    vault = env_with_vault
    (vault / "_prompts" / "no-fm.md").write_text("Just content\n", encoding="utf-8")
    with patch("brain.Config.PROMPTS_ROOT", vault / "_prompts"):
        import brain as brain_mod
        out = brain_mod.load_prompt("no-fm.md")
    assert out["content"] == "Just content\n"
    assert out["model"] is None
    assert out["temperature"] is None


def test_load_prompt_with_frontmatter(env_with_vault):
    vault = env_with_vault
    with patch("brain.Config.PROMPTS_ROOT", vault / "_prompts"):
        import brain as brain_mod
        out = brain_mod.load_prompt("explore.md")
    assert "thinking partner" in out["content"]
    assert out["model"] == "reasoning"
    assert out["temperature"] == "reasoning"


def test_build_user_message_separator(env_with_vault):
    vault = env_with_vault
    (vault / "20-context" / "ctx.md").write_text("ctx body", encoding="utf-8")
    with patch("brain.Config.VAULT_ROOT", vault):
        import brain as brain_mod
        from pathlib import Path
        ctx_path = vault / "20-context" / "ctx.md"
        context_resolved = [(ctx_path, "20-context/ctx.md")]
        result = brain_mod.build_user_message(
            "note body",
            context_resolved,
            "10-thinking/foo.md",
        )
    assert "[CONTEXT: 20-context/ctx.md]" in result
    assert "[NOTE: 10-thinking/foo.md]" in result
    assert "\n\n---\n\n" in result
    assert result.index("[NOTE:") > result.index("---")


# ---------------------------------------------------------------------------
# Existing: section accumulation and ordering
# ---------------------------------------------------------------------------

def test_critique_adds_critique_section(env_with_vault):
    vault = env_with_vault
    (vault / "01-inbox" / "test-critique.md").write_text("My idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("### Gaps\n1. Unclear.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "critique", "01-inbox/test-critique.md"], env=env)
    assert result.exit_code == 0
    full = (vault / "01-inbox" / "test-critique.md").read_text()
    assert "# Critique" in full
    assert "My idea" in full
    assert not (vault / "01-inbox" / "archive" / "test-critique.md").exists()


def test_explore_adds_explore_section(env_with_vault):
    vault = env_with_vault
    (vault / "01-inbox" / "test-explore.md").write_text("My idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("### Possibilities\nOption A.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "explore", "01-inbox/test-explore.md"], env=env)
    assert result.exit_code == 0
    full = (vault / "01-inbox" / "test-explore.md").read_text()
    assert "# Explore" in full
    assert "My idea" in full


def test_normalize_overwrites_file(env_with_vault):
    vault = env_with_vault
    (vault / "01-inbox" / "test-normalize.md").write_text("Raw idea\n", encoding="utf-8")
    fake_rewritten = "Clear idea."
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock(fake_rewritten)):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "normalize", "01-inbox/test-normalize.md"], env=env)
    assert result.exit_code == 0
    full = (vault / "01-inbox" / "test-normalize.md").read_text()
    assert "# Current Version" in full
    assert fake_rewritten in full


def test_normalize_preserves_sections(env_with_vault):
    vault = env_with_vault
    content = "# Current Version\n\nOld body\n\n---\n\n# Explore\n\nExplore content\n\n---\n\n# Critique\n\nCritique content\n"
    (vault / "01-inbox" / "test-preserve.md").write_text(content, encoding="utf-8")
    fake_rewritten = "New body."
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock(fake_rewritten)):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "normalize", "01-inbox/test-preserve.md"], env=env)
    assert result.exit_code == 0
    full = (vault / "01-inbox" / "test-preserve.md").read_text()
    assert "New body." in full
    assert "Explore content" in full
    assert "Critique content" in full
    assert "Old body" not in full


def test_normalize_dry_run_no_write(env_with_vault):
    vault = env_with_vault
    (vault / "01-inbox" / "dry.md").write_text("Text\n", encoding="utf-8")
    result = _run_brain(
        {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"},
        "idea", "normalize", "01-inbox/dry.md", "--dry-run",
    )
    assert result.returncode == 0
    json.loads(result.stdout)
    assert (vault / "01-inbox" / "dry.md").read_text() == "Text\n"


def test_normalize_failure_no_write(env_with_vault):
    vault = env_with_vault
    (vault / "01-inbox" / "fail.md").write_text("Text\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=None):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "normalize", "01-inbox/fail.md"], env=env)
    assert result.exit_code == 1
    assert (vault / "01-inbox" / "fail.md").read_text() == "Text\n"


def test_multiple_sections_accumulate(env_with_vault):
    vault = env_with_vault
    (vault / "01-inbox" / "acc.md").write_text("Idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("Gaps.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        runner.invoke(brain_mod.app, ["idea", "critique", "01-inbox/acc.md"], env=env)
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("Options.")):
        runner.invoke(brain_mod.app, ["idea", "explore", "01-inbox/acc.md"], env=env)
    full = (vault / "01-inbox" / "acc.md").read_text()
    assert "# Critique" in full
    assert "# Explore" in full
    assert "Idea" in full


def test_append_section_order(env_with_vault):
    vault = env_with_vault
    (vault / "01-inbox" / "order.md").write_text("Idea\n", encoding="utf-8")
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("First.")):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        runner.invoke(brain_mod.app, ["idea", "critique", "01-inbox/order.md"], env=env)
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock("Second.")):
        runner.invoke(brain_mod.app, ["idea", "critique", "01-inbox/order.md"], env=env)
    full = (vault / "01-inbox" / "order.md").read_text()
    assert full.count("# Critique") == 2
    assert "First." in full
    assert "Second." in full


# PRE-EXISTING FAILURE: missing normalize.md in test vault. Unrelated to type-aware context changes.
def test_legacy_file_critique_then_normalize(env_with_vault):
    vault = env_with_vault
    content = "Original body\n\n---\n\n# Critique — 2026-01-01 12:00 UTC\n\nCritique text\n"
    (vault / "01-inbox" / "legacy.md").write_text(content, encoding="utf-8")
    fake_rewritten = "Normalized body."
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock(fake_rewritten)):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["idea", "normalize", "01-inbox/legacy.md"], env=env)
    assert result.exit_code == 0
    full = (vault / "01-inbox" / "legacy.md").read_text()
    assert "Critique text" in full
    assert "Normalized body." in full
    assert "Original body" not in full


def test_normalize_preserves_frontmatter(env_with_vault):
    vault = env_with_vault
    content = "---\ntype: thinking\nstatus: raw\n---\n\n# Current Version\n\nOld body\n"
    (vault / "10-thinking" / "fm.md").write_text(content, encoding="utf-8")
    fake_rewritten = "New body."
    env = {"VAULT_ROOT": str(vault), "OPENROUTER_API_KEY": "sk-dummy"}
    with patch("brain.Config.VAULT_ROOT", vault), patch("brain.ai_call", return_value=_success_mock(fake_rewritten)):
        from typer.testing import CliRunner
        import brain as brain_mod
        runner = CliRunner()
        result = runner.invoke(brain_mod.app, ["thinking", "normalize", "10-thinking/fm.md"], env=env)
    assert result.exit_code == 0
    full = (vault / "10-thinking" / "fm.md").read_text()
    assert "type: thinking" in full
    assert "status: raw" in full
    assert "New body." in full
    assert "Old body" not in full