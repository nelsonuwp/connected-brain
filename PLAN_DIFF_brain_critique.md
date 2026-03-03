# Planned diffs: brain.py and critique-idea.md

## 1. brain.py

### Docstring (line 2)
- Change: `idea/thinking/initiative: critique, explore, normalize, promote` → `idea/thinking/initiative: critique, explore, promote` (remove "normalize" from description).

### After _resolve_type_block_and_warn (after line 384) — ADD:

```python
def _resolve_task_prompt_and_warn(note_content: str, command: str) -> tuple[dict, str]:
    """Load task-{command}-{type}.md. type from frontmatter; default code on missing/invalid; warn to stderr."""
    fm = _parse_note_frontmatter(note_content)
    type_val = (fm.get("type") if fm else None) or None
    if type_val is not None and isinstance(type_val, str):
        type_val = type_val.strip() or None
    if type_val is None:
        print("[WARN] Note has no type specified — using task-{command}-code.md", file=sys.stderr)
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
```

### REMOVE idea_normalize (lines 564–597)
- Delete the entire block from `@idea_app.command("normalize")` through the end of `idea_normalize` (including the blank line before `@idea_app.command("promote")`).

### REPLACE idea_promote (lines 599–628)
- Add parameter: `as_task: bool = typer.Option(False, "--as-task", ...)`.
- After reading `note_content`: compute `use_task = as_task or (route and route.get("recommendation") == "task")` where `route = _parse_route_block(note_content)`.
- Load prompt: `promote-idea-to-task.md` if use_task else `promote-idea-to-thinking.md`.
- Build user_content and messages; resolve model/temp.
- Then: if dry_run → print_dry_run_payload and raise typer.Exit(0).
- LLM call; on failure exit 1.
- If use_task: promoted_content = _set_frontmatter_status(note_content, "promoted-to-task"); write_to_path(full_path, promoted_content); archive_file(full_path, filename); write_new_file("31-tasks/drafting/" + filename, result["content"]); print tokens and dest/archive.
- Else (thinking): promoted_content = _set_frontmatter_status(note_content, "promoted"); write_to_path(full_path, promoted_content); archive_file(full_path, filename); write_new_file("10-thinking/" + filename, result["content"]); same print.

### After initiative_complete, before Absorb (after line 1017) — ADD task_app block:
- task_app = typer.Typer(); app.add_typer(task_app, name="task").
- task explore: resolve path, read note, context_resolved; _resolve_task_prompt_and_warn(note_content, "explore"); system_content = prompt["content"]; build_user_message; dry_run handling; ai_call; append_section "Explore".
- task critique: same with "critique" and append_section "Critique".
- task activate: resolve path; vault_rel = full_path.resolve().relative_to(vault_root); if not startswith "31-tasks/drafting/" exit 1; dest_vault_rel = "31-tasks/active/" + full_path.name; read content; new_content = _set_frontmatter_status(content, "active"); write_new_file(dest_vault_rel, new_content); full_path.unlink(); print.
- task complete: same pattern; must be in 31-tasks/active/; dest 31-tasks/completed/; status complete.
- task kill: vault_rel under 31-tasks/ (drafting, active, or completed); new_content = _set_killed_frontmatter(content); write_to_path(full_path, new_content); archive_file(full_path, full_path.name); print. (archive_file moves, so original path is gone.)

---

## 2. critique-idea.md

### Append at end of file (after line 45 "Begin immediately with ## Score.")

```
After scoring, assess routing:
- If the why is self-evident, the how is already obvious, and execution is bounded → recommend: task
- Otherwise → recommend: thinking

Output as:

---route
recommendation: task | thinking
reason: one sentence
---
```

(No change to any existing line; append only.)
