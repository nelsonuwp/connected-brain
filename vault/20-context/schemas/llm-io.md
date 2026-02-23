---
type: context-block
schema-version: 1
topic: llm-api-data-format
scope: connected-brain
inject-into: any session involving ai_client.py, OpenRouter calls, or messages[] construction
created: 2026-02-23
---

# Context: LLM API Data Format (messages[])

## What This Is
This block defines the exact data structure that `ai_client.py` sends to the OpenRouter API. OpenRouter follows the OpenAI messages format exactly. Every call is a `POST` to `https://openrouter.ai/api/v1/chat/completions` with a JSON body containing a `messages` array.

This context block should be injected into any Cursor session where `ai_client.py` is being built, modified, or debugged.

---

## The Three Roles

Every message in the `messages[]` array has a `role`. There are three relevant roles for this project:

**`system`** — The rule-setter. Defines the AI's persona, output format, and behavioral constraints. Does not contain the task. Contains the rules of engagement. In `brain.py`, this is always the contents of the relevant `_prompts/` file (e.g. `_prompts/think-mode.md`).

**`user`** — The human's input. The actual data payload to be processed. In `brain.py`, this is assembled by `build_user_message()` and contains the labeled context blocks plus the note contents.

**`assistant`** — The AI's previous responses. Used to simulate conversation history. Not used in v1 of `brain.py` (single-shot calls only), but documented here for when multi-turn is added.

---

## Payload Pattern 1 — Single-Shot (Current Spec)

This is what `brain.py` constructs and sends for every command in v1. One system message, one user message, no history.

```python
messages = [
    {
        "role": "system",
        "content": "<contents of _prompts/think-mode.md>"
        # Behavioral rules, output format, persona.
        # Loaded from file by brain.py, passed as a string to ai_client.call()
    },
    {
        "role": "user",
        "content": (
            "[CONTEXT: 20-context/schemas/db-schema.md]\n"
            "Table: Users\nColumns: id, name, email\n\n"
            "[NOTE: 10-thinking/2026-02-22-llm-bridge.md]\n"
            "I need to build a Python CLI that reads an Obsidian note and calls OpenRouter."
        )
        # Assembled by build_user_message(note_content, context_files)
        # Context blocks come first, note comes last
    }
]
```

brain.py assembles `messages` and calls `ai_client.call()` with the full list. The transport layer builds the body and returns a minimal result:

```python
# brain.py assembles:
messages = [
    {"role": "system", "content": prompt["content"]},
    {"role": "user", "content": user_content}
]
# ai_client.call(model_string, temperature, messages) builds:
# json={ "model": model_string, "temperature": temperature, "messages": messages, "max_tokens": 4096 }
# ai_client.call() returns (on success):
# {"content": str, "tokens": {"prompt": int, "completion": int, "total": int}}
```

So brain owns message assembly; ai_client only POSTs and returns the transport dict (content + tokens) or `None` on failure.

---

## Transport Result vs LLMResponse

`ai_client.call()` returns a **transport result dict** — not a full LLMResponse. On success it returns only:

- `content` (str): the model’s reply text
- `tokens`: `{"prompt": int, "completion": int, "total": int}` from OpenRouter’s `usage`

LLMResponse is a separate, richer envelope (run_id, model, generated_at, mode, status, output, error, sources_used, tokens) used for writing response records to disk (future use). Do not conflate the two: the transport layer does not construct or populate LLMResponse.

---

## Payload Pattern 2 — Multi-Turn / Memory (Future)

If `brain.py` is ever extended to parse previous `## LLM Output` blocks from a note and send them back as history, the pattern becomes:

```python
messages = [
    {
        "role": "system",
        "content": "<contents of _prompts/think-mode.md>"
    },
    {
        "role": "user",
        "content": "I want to build an LLM bridge for Obsidian using Python."
        # First user turn — parsed from note history
    },
    {
        "role": "assistant",
        "content": "That sounds like a great workflow. I recommend using Typer for the CLI. What commands do you want to start with?"
        # Previous LLM output — parsed from ## LLM Output block in the note
    },
    {
        "role": "user",
        "content": "Let's start with noun-verb-file structure. Like: `thinking think <file>`."
        # Current user input
    }
]
```

The LLM treats the `assistant` messages as its own prior words. This creates the illusion of memory within a single note across multiple `brain.py` invocations.

---

## Payload Pattern 3 — Tool Calling (Future / Optional)

If `brain.py` is ever extended to allow the LLM to request data from external sources (e.g. searching the vault, querying Jira), the pattern becomes a two-step exchange. The LLM first responds with a `tool_calls` block instead of text. Your Python code runs the requested tool and sends the raw result back as a `tool` role message.

```python
# Step 1 — LLM requests a tool
messages = [
    {"role": "system", "content": "You have access to a vault search tool."},
    {"role": "user", "content": "What did I decide about the CLI architecture for the LLM Bridge?"},
    {
        "role": "assistant",
        "content": "",   # Empty — model is calling a tool instead of responding
        "tool_calls": [
            {
                "id": "call_abc123xyz",
                "type": "function",
                "function": {
                    "name": "search_vault",
                    "arguments": "{\"query\": \"CLI architecture LLM Bridge\"}"
                }
            }
        ]
    }
]

# Step 2 — Your Python code runs the search, then sends the result back
messages.append({
    "role": "tool",
    "tool_call_id": "call_abc123xyz",   # Must match the id above exactly
    "content": "File: 30-initiatives/026-02-22-llm-bridge.md\nContent: Shifted from generic flags to Noun→Verb→File subcommand routing using Typer."
})

# Step 3 — Send the full messages array again; LLM now responds with text
```

---

## Key Rules for `ai_client.py`

- `system` is always index 0 in the array
- `user` is always last for a single-shot call
- `assistant` and `user` must strictly alternate in multi-turn calls — two `user` messages in a row is invalid and will return a 400 error
- `tool_call_id` in the `tool` message must exactly match the `id` in the `tool_calls` block — any mismatch returns a 400 error
- `max_tokens` sets the ceiling on response length — 4096 is a safe default; increase for long spec outputs
- `timeout=120` — reasoning models (Opus) can take 30-60 seconds on complex calls; 120s prevents premature disconnects

---

## What the LLM Output Should NOT Contain

The system prompt in each `_prompts/` file should instruct the LLM to avoid:
- Preamble: "Sure! Here's my thinking:" — looks terrible appended to a Markdown note
- Sign-offs: "Let me know if you'd like me to expand on any of these points!" — same
- Meta-commentary about its own response length or confidence

The response should begin immediately with substantive content and end when the content is complete. Nothing more.
