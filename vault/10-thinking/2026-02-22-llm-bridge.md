# LLM Bridge — Raw Thinking

CEO/board ask: n/a — this is a self-initiated tool

## Why I want this
Currently have to copy/paste notes into browser LLM sessions.
Context gets lost between sessions.
Want to run prompts against vault notes from terminal.

## What I think it should do
- Read a note from vault
- Read a prompt template from _prompts/
- Inject context blocks
- Call an LLM via OpenRouter
- Write output back into the note

## What I'm not sure about
- Should output go back into same note or a new file?
- How does this connect to the re-anchor system?
- Do I need a session concept baked in?
- Should it handle data (RunArtifact) or just notes?

## Reference
- Already have aiClient.py from old Gemini project — good retry/model pattern
- Have OpenRouter key in root .env
- Have prompt files in vault/_prompts/