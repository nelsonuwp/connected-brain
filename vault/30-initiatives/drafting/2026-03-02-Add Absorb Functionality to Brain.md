---
type: initiative
status: drafting
---
## One-Line Purpose

Enable directional, programmatic consolidation of source notes into a root note while preserving traceability and automatically archiving sources.

## Context

The current system breaks down when ideas overlap or evolve non-linearly across stages. Related ideas emerge at different times, useful context gets stranded in earlier notes, and manual consolidation is inconsistent and loses traceability. Because manual copy-pasting breaks workflow and is highly annoying, the effort is often abandoned, leaving fragmented idea spaces. Absorb provides a repeatable, low-friction CLI mechanism to consolidate while enforcing programmatic flow and preserving exactly where ideas came from.

## Success Looks Like

1. **Zero duplicate notes** created for the same idea space over a 4-week observation period. (Definition of duplicate: two notes with identical ## One-Line Purpose or heavily overlapping first 100 words. Verified by manual review of 01-inbox and 10-thinking at the end of the period).
    
2. **Instant execution:** The absorb operation completes programmatically in < 1 minute per source note.
    
3. **High utility:** Absorbed sections are actively referenced, measured by the absorbed content appearing in the git diff of subsequent edits to the root note within 2 weeks of the operation.
    

## Constraints

- **Directional:** One root note, one or more source notes per operation.
    
- **Top-level command:** Must be invoked via positional arguments: brain absorb <root_path> <source_path_1> [<source_path_2> ...]. First argument is the target, the rest are inputs.
    
- **Status update:** Source notes must be updated to status: absorbed to [[root]] and moved to their stage-specific archive folder.
    
- **Enforced structure:** The script must programmatically enforce the section structure: ## Absorbed — [[source]], containing ### Key Points (LLM-generated) and ### Raw Context (copied verbatim).
    
- **No linking changes:** Existing links and backlinks are not modified.
    
- **No transclusion:** Content is physically copied to ensure portability.
    

## Open Questions

- **Summarization quality:** How consistent or high-quality will the LLM-generated Key Points be? Decision trigger: If 3 out of 10 absorbs produce Key Points that omit critical context (as judged by manual review), downgrade to pasting Raw Context only.
    
- **Root note size limits:** At what point does a root note become too bloated to be useful? Decision trigger: If any root note exceeds 500 lines or 3000 words after an absorb, manually split the note and revisit the UX.
    
- **Cross-stage confusion:** Will absorbing across stages create confusion? Decision trigger: Acceptable risk. If a post-mortem reveals a broken workflow due to cross-stage context loss, add validation warnings to the command.
    

## Work Breakdown

### Files / Deliverables

- **CLI Command:** A new top-level Typer command in brain.py: @app.command("absorb") utilizing variable-length positional arguments.
    
- **Prompt File:** Create vault/_prompts/summarize-absorbed.md with frontmatter mapping to MODEL_WORKHORSE and system prompt template: "Summarize the provided raw note into 3-5 bullet points highlighting key insights, constraints, and decisions. Output format: markdown bullet list only, no preamble."
    
- **Frontmatter update logic:** Modify or wrap _set_frontmatter_status in brain.py to create _set_absorbed_frontmatter(content: str, parent_note_name: str) which writes status: absorbed to [[parent_note_name]].
    
- **Archiving logic:** Reuse existing archive_file helper in brain.py to route to appropriate stage archives.
    

### Sequence

1. **Scaffold the CLI:** Build the @app.command("absorb") in brain.py with positional Typer arguments (first arg = root, rest = list of sources). Testable outcome: Command parses arguments and raises FileNotFoundError with exit code 1 if any specified file does not exist.
    
2. **Build extraction & formatting:** Implement reading the source file(s) and assembling the ## Absorbed and ### Raw Context text. Testable outcome: Running on dummy files correctly appends the raw text to the parent note.
    
3. **Implement LLM Summarization:** Add the ai_client.call step using MODEL_WORKHORSE to generate the ### Key Points bullet list. Testable outcome: LLM output is valid markdown, contains 3-5 bullet points, and does not exceed roughly 200 words.
    
4. **Build source archiving:** Implement the frontmatter update (absorbed to [[root]]) and trigger archive_file for each source note. Testable outcome: Source notes successfully move to their respective /archive/ folders with updated YAML.
    
5. **End-to-End Test:** Run the full flow on 2 overlapping idea notes into a single thinking note. Testable outcome: Root note contains exactly 2 new ## Absorbed sections, both source notes are correctly placed in 01-inbox/archive/, and git diff shows only the expected file modifications.
    

## Decisions Made

- **User Error is Permitted:** The command will allow you to do "stupid" things (like absorbing an already-absorbed note, or creating circular references). Simplicity and lack of friction are prioritized over complex safety rails.
    
- **Critical Errors Fail Hard:** The script will throw an immediate fatal error if the target root note or any of the source files do not exist.
    
- **Automated Summaries from Day 1:** Using claude-sonnet-4-5 (MODEL_WORKHORSE) to generate summaries automatically, rather than leaving it blank for manual entry.
    
- **Bulk absorbing:** Supported out of the box via multiple positional arguments for source files, allowing rapid multi-file consolidation in one command.
    

## Delegation State

|   |   |   |   |
|---|---|---|---|
|Person|Owns|By When|Level|
|Self|Full Implementation|2026-03-07|Execute|

## Validation Plan

- **Review Cadence:** Self will audit on 2026-03-16 by reviewing the git log for absorb operations and manually inspecting 5 random root notes. Must have at least 10 operations (tracked via git log --grep='absorb').
    
- **Rollback Trigger:** If any absorb operation takes > 2 minutes end-to-end, or if 3+ archive links are broken (verified by manual vault check or broken link tools), disable the command and revert to manual consolidation until the UX is fixed.