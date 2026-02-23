---
type: re-anchor
project: connected-brain-setup
session: 001
date: 2026-02-23
previous: none
context-blocks-used: []
---

# Re-anchor — Connected Brain Setup + LLM Bridge

## State at End of Session

The connected-brain system is substantially built and the first real project
(llm-bridge) has been run through the full workflow from inbox to execute-ready.

**Vault:** Fully structured at ~/connected-brain/vault/ with all numbered folders
(00-daily through 90-meeting-notes), _templates, _prompts, _attachments.
All ABOUT.md files created. Obsidian is pointed at vault/ as root.

**Git:** Repo initialized at ~/connected-brain/, pushed to
github.com/nelsonuwp/connected-brain. Credentials were accidentally committed
in first push (eaff67f) — filter-branch fix was given but unclear if it was
actually run. This needs to be confirmed. Four credentials were exposed:
Atlassian API token, Azure AD secret, Salesforce consumer key, Salesforce
consumer secret. Rotation status unknown.

**Obsidian plugins:** All installed and configured — Templater, Periodic Notes,
Obsidian Git, Calendar, Dataview, Tasks, QuickAdd. Config confirmed via
data.json review for each plugin.

**Templates:** All eight templates created and in vault/_templates/:
daily-briefing, weekly-review, meeting-note, initiative-spec, person-note,
context-block, delegation-brief, re-anchor.

**Prompt files:** All six created and in vault/_prompts/:
think-mode, specify-mode, execute-mode, meeting-summary, one-on-one-prep,
re-anchor-prompt.

**Hotkeys confirmed working:**
- Cmd+Shift+D → today's daily note
- Cmd+Shift+K → weekly note
- Cmd+Shift+E → insert template
- Cmd+Shift+I → inbox capture (QuickAdd)
- Cmd+Shift+M → promote to thinking (QuickAdd)
- Cmd+Shift+V → move current file
- Cmd+O → quick switcher
- Cmd+Shift+P → command palette

**Cursor rules:** Four .mdc files created for .cursor/rules/:
vault-routing.mdc, project-routing.mdc, context-blocks.mdc, llm-modes.mdc.
Unclear if these were copied into ~/connected-brain/.cursor/rules/ yet.

**Schemas:** Two context blocks created:
- vault/20-context/schemas/source-artifact.md
- vault/20-context/schemas/llm-io.md

Corresponding Python implementations in projects/_reference/schemas/:
- source_artifact.py (company_id removed, agnostic)
- llm_io.py (company_id removed, agnostic)

**LLM Bridge project — ready for Cursor execution:**
- Thinking note complete: vault/10-thinking/2026-02-22-llm-bridge.md (status: promoted)
- Initiative spec complete: vault/30-initiatives/026-02-22-llm-bridge.md (status: speccing)
- Work breakdown appended to initiative spec
- Think mode and Specify mode both run and logged in LLM Work Log
- Cursor execute prompt written and ready to paste

**llm-bridge project folder:** projects/llm-bridge/ exists with .env.example
and requirements.txt. The three Python files (config.py, ai_client.py,
bridge.py) have NOT been written by Cursor yet — that is the next session's
first task.

---

## Decisions Made

- Vault lives at ~/connected-brain/vault/, projects at ~/connected-brain/projects/ → Clean separation of markdown and code
- Folder numbering uses decade logic (00-09 time, 10-19 thinking, etc.) → Scalable without renumbering
- 50-services = internal ops, 51-catalog = external products, 52-customers = accounts → [→ LOG TO 60-decisions/]
- Projects copy from _reference/, never import → Standalone bubble pattern for handoff/containerization [→ LOG TO 60-decisions/]
- .env files never committed, .env.example always committed → Security
- workspace.json excluded from git → Machine-specific, creates noisy diffs
- Cursor rules split into four .mdc files with globs → Only loads relevant rules per file context
- Thinking notes stay in 10-thinking/ permanently (status: promoted) → They are the reasoning record, not orphans
- "Promote" = insert template into existing note + move, OR QuickAdd macro for new note → Template only auto-applies on creation
- Output goes back into same note, not a new file → Note is the canonical record [→ LOG TO 60-decisions/]
- ai_client.py (transport) and bridge.py (vault I/O) are separate files → Single responsibility, Cursor can extend either independently [→ LOG TO 60-decisions/]
- --context accepts multiple space-separated files in one flag → Simpler to type than repeated flags [→ LOG TO 60-decisions/]
- All paths in bridge.py resolve relative to Config.VAULT_ROOT → User never types full absolute paths [→ LOG TO 60-decisions/]
- Atomic write uses temp file + os.replace() → Note is untouched on any failure [→ LOG TO 60-decisions/]
- "Jr dev" = Cursor/Composer, not a human → Code clarity requirement affects naming conventions

---

## What Works

- Vault folder structure created and committed
- All ABOUT.md files in place
- Obsidian vault pointed at correct root (vault/, not vault/Connected Brain/)
- All plugins installed and configured via data.json
- All hotkeys set in hotkeys.json
- All templates functional in _templates/
- All prompts written in _prompts/
- QuickAdd: Inbox Capture (Cmd+Shift+I) and Promote to Thinking (Cmd+Shift+M) both configured
- Full workflow validated on real project (llm-bridge): inbox → thinking → initiative → specify → execute-ready
- Initiative spec for llm-bridge is complete and Cursor-ready
- source_artifact.py and llm_io.py are agnostic (company_id removed)

---

## What Doesn't

- **Git history may still contain secrets.** The filter-branch command was provided but confirmation it ran successfully was never received. Until confirmed, treat the repo as potentially compromised.
- **Four credentials need rotation** (Atlassian API token, Azure AD app secret, Salesforce consumer key, Salesforce consumer secret). Rotation status unknown — must be confirmed before using those systems.
- **Cursor rules** (.cursor/rules/*.mdc) may not have been copied into the workspace yet. Confirm they exist at ~/connected-brain/.cursor/rules/ before starting Cursor session.
- **bridge.py, ai_client.py, config.py not written yet** — Cursor has not been run on the llm-bridge initiative.
- **No context blocks exist yet** in vault/20-context/ beyond the two schemas. business/osom-model.md and apis/ files are all empty stubs.
- **Daily briefing has not been tested** — Cmd+Shift+D behavior unconfirmed.

---

## Next Session Starts With

**First task:** Open Cursor with ~/connected-brain/ as workspace root. Paste the
execute mode prompt from the bottom of
vault/30-initiatives/026-02-22-llm-bridge.md into Composer. Let it build
config.py, ai_client.py, and bridge.py in that order. Test with:

```bash
cd ~/connected-brain/projects/llm-bridge
python bridge.py \
  --note 10-thinking/2026-02-22-llm-bridge.md \
  --mode think
```

Confirm the output appears appended to the note in Obsidian.

**Second task:** Confirm git history is clean (no secrets). Run:
```bash
cd ~/connected-brain
git log --oneline
git show eaff67f --stat
```
If .env still appears in that commit, run the filter-branch fix.

**Third task:** Create first real business context block at
vault/20-context/business/osom-model.md using the context-block template.
This is the most-injected context block in the system and nothing else works
well without it.

---

## Open Questions

- Were the four credentials (Atlassian, Azure AD, Salesforce x2) actually rotated?
- Was the git filter-branch command run and did it succeed?
- Were the .cursor/rules/ files copied into ~/connected-brain/.cursor/rules/?
- What is the VAULT_ROOT value to put in projects/llm-bridge/.env — is it ~/connected-brain/vault or an absolute path?

---

## Context Blocks Used

None formally injected. The following were referenced by content during this
session and should be pre-loaded next session if doing vault or bridge work:
- vault/20-context/schemas/llm-io.md
- vault/20-context/schemas/source-artifact.md
- vault/30-initiatives/026-02-22-llm-bridge.md (for Cursor execute session)
