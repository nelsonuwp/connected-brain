# connected-brain

Personal operating system for a VP of Operations at a managed services company.
Connects human thinking, LLM workflows, codebases, business systems, and delegation flows.

## What lives here

```
connected-brain/
├── vault/        → Obsidian knowledge base (thinking, reference, leadership, ops)
└── projects/     → Code projects (self-contained, each a standalone unit)
```

## Design principles

- **Capture once, reuse everywhere.** Context blocks in vault/20-context/ get injected
  into LLM prompts instead of re-explaining the same thing repeatedly.
- **Separate thinking from execution.** Raw ideas live in vault/10-thinking. They get
  promoted to vault/30-initiatives before any code or delegation happens.
- **Projects are standalone.** Each project in projects/ owns its own config, schemas,
  and credentials. Nothing imports from _reference/ — it copies from it.
- **Cursor sees everything.** Open ~/connected-brain/ as the workspace root in Cursor,
  not a subfolder. This gives LLMs access to both vault context and project code.

## Key files

- .env          → master credential store (never committed)
- .env.example  → committed template listing all credential keys
- .gitignore    → ensures .env files, caches, and OS noise are excluded
- .cursorrules  → tells Cursor how to route ambiguous requests across vault and projects

## Numbering logic (vault folders)

| Range | Category   | What lives there                              |
|-------|------------|-----------------------------------------------|
| 00-09 | Time       | Daily notes, inbox                            |
| 10-19 | Thinking   | Active ideation, half-formed ideas            |
| 20-29 | Reference  | Reusable context blocks (APIs, schemas, etc.) |
| 30-39 | Execution  | Initiative specs                              |
| 40-49 | People     | Direct reports, stakeholders                  |
| 50-59 | Business   | Services (ops), catalog (sales), customers    |
| 60-69 | Records    | Decisions                                     |
| 70-79 | Delegation | Delegation briefs                             |
| 80-89 | Sessions   | LLM re-anchors                                |
| 90-99 | Comms      | Meeting notes                                 |
| _     | System     | Templates, prompts, attachments               |
