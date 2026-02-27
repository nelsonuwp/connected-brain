# Connected Brain — System Overview

## The Problem

Ideas, decisions, and context live in too many places — Slack, email, browser
tabs, memory. When you sit down to do real work, you spend the first 20 minutes
reconstructing what you already knew. When you hand something to an LLM, you
spend another 10 minutes re-explaining context that exists somewhere but not
in the right shape. When you finish a project, the reasoning that produced the
decisions evaporates.

The result: you're always starting from scratch, and the quality of your
thinking is capped by how much you can hold in your head at once.

## The Solution

A single system that does three things:

1. **Moves ideas through a defined process** — from raw capture to executable
   initiative, with LLM assistance at each stage and a clear promotion gate
   between stages

2. **Stores context in a reusable form** — so you inject it into LLM sessions
   instead of re-explaining it, and so decisions made once don't get
   re-litigated

3. **Keeps a record of how you got there** — the thinking history, the
   critiques, the options considered, the decisions made

## The Mental Model

Each stage of the workflow locks one thing before you move to the next:

| Stage | What you're working out | What gets locked | You know it's ready when |
|---|---|---|---|
| Idea | Is this worth pursuing? | **The Why** | Critique scores ≥ 7 |
| Thinking | How might we solve this? | **The How** | Critique scores ≥ 7 |
| Initiative | What exactly are we building? | **The Path** | Critique scores ≥ 7 |
| Active | We're doing it | — | Done |

You don't spec something before you know why you're doing it. You don't execute
before you know what you're building. The promotions enforce this.

## The LLM Loop

At each stage, the loop is:

```
explore → critique → fix → explore → critique → fix → promote
```

- **Explore** surfaces directions, options, and tradeoffs. Max 3 per run.
  Tells you when you've explored enough.
- **Critique** scores the note 0–10, tells you what's strong, and tells you
  specifically what to fix to get to the next stage. 7+ means ready to promote.
- **Fix** is you, editing the note based on critique output.
- **Promote** is the LLM transforming the note into the next stage's format
  and moving it to the right folder.

## The Tools

- **Obsidian** — where everything lives. Notes, context, templates.
- **brain.py** — CLI that runs LLM operations against vault notes.
  You never copy-paste into a browser tab.
- **OpenRouter** — LLM provider. Three model tiers: reasoning, workhorse, nano.
- **Cursor** — where code gets built. Initiative specs feed directly into
  Cursor Composer sessions.
- **Jira** — task and execution tracking. brain.py and Obsidian track thinking;
  Jira tracks doing.

## How to Use These Docs

| Document | Read it when |
|---|---|
| `README.md` (this file) | You need to remember why this exists |
| `structure.md` | You're not sure where something belongs |
| `tooling.md` | You can't remember a command or hotkey |
| `playbook.md` | You're working through a real note and need step-by-step |
| `CHANGELOG.md` | You want to know why something is the way it is |
