# vault/

The Obsidian knowledge base. Everything you think, plan, track, and reference as a human
and as context for LLMs lives here.

## What this is NOT

- Not a project management tool (that's Jira/JSM)
- Not a communication tool (that's Slack/Teams/Outlook)
- Not a code repository (that's GitLab, and projects/ in this workspace)

## What this IS

A personal control plane that sits above all those tools. Information flows
INTO the vault from those systems (you capture it). Information flows OUT
of the vault into LLMs (you inject it) and into those systems (you route it).

## Folder map

| Folder            | Category   | What lives there                           |
|-------------------|------------|--------------------------------------------|
| 00-daily/         | Time       | Daily notes, weekly reviews                |
| 01-inbox/         | Time       | Raw captures, 48hr max shelf life          |
| 10-thinking/      | Thinking   | Ideas being developed, not yet specs       |
| 20-context/       | Reference  | Reusable LLM context blocks                |
| 30-initiatives/   | Execution  | Active initiative specs                    |
| 40-people/        | People     | Direct reports, 1:1 logs, capability maps  |
| 50-services/      | Business   | Internal OSOM service delivery units       |
| 51-catalog/       | Business   | External products and service offerings    |
| 52-customers/     | Business   | Customer accounts, segments, relationships |
| 60-decisions/     | Records    | Decision records (ADR style)               |
| 70-delegation/    | Delegation | Delegation briefs                          |
| 80-sessions/      | Sessions   | LLM re-anchors, session continuity         |
| 90-meeting-notes/ | Comms      | Meeting notes                              |
| _templates/       | System     | Note templates (Templater)                 |
| _prompts/         | System     | Reusable LLM prompt templates              |
| _attachments/     | System     | Binary attachments (auto-managed)          |

## open-loops.md

Single file at vault root. Everything occupying mental RAM that doesn't
belong to a specific initiative or person. Reviewed every Monday morning.
