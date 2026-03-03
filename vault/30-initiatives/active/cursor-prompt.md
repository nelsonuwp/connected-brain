---
type: deliverable
initiative: "[[2026-03-02-type-aware injectable context blocks]]"
purpose: implementation prompt for Cursor Composer covering steps 4 and 5
---

# Cursor implementation prompt — type-aware context (steps 4 and 5)

Saved record of what was sent to Cursor for implementing dynamic type-based context injection in brain.py.

## Step 4 — Dynamic context loading in brain.py

- Parse frontmatter of the **target note** (the file argument) for the `type:` field.
- Construct path `20-context/types/{type}-{command}.md` under VAULT_ROOT (command is `critique` or `explore`).
- If file exists, read contents and inject into **system** context only. Order: [generic context] → [type block] → [command prompt]. Use segmented join: `segments = [generic_context, type_block, command_prompt]` then `"\n\n".join(filter(None, segments))`. Generic slot explicit, empty for v1. Do not put the type block in the user message; [STAGE: idea/thinking/initiative] stays in the user message for explore commands only.
- Add temporary debug logging (--debug flag) that prints the full system message to stderr so injection can be verified (only in the six explore/critique commands). Remove after verification.
- **Dry-run:** Assemble the full system message (including type block) before the dry-run branch so that `print_dry_run_payload(..., messages)` shows the complete payload with type block; verify injection without calling the API.

## Step 5 — Warning behavior

- If type field is missing: print `[WARN] Note has no type specified — proceeding without type-specific context` to stderr.
- If type field is present but not one of `code|business|content`: print `[WARN] Note has invalid type '{value}' — proceeding without type-specific context` to stderr.
- In both cases: exit code 0, command executes with generic context only (no type block).

## Out of scope

- Steps 1–3 (block drafting, audit, testing).
- Modifying prompt files.
- Changing any existing brain.py behavior outside of context loading for the six explore/critique commands.

## Commands affected

- idea critique, idea explore
- thinking critique, thinking explore
- initiative critique, initiative explore
