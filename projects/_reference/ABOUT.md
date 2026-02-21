# projects/_reference/

Pattern library. The source of truth for reusable implementations.

## Critical rule

Do not import from this folder. Copy from it.

WRONG:  from _reference.clients.jira import JiraClient
RIGHT:  cp _reference/clients/jira.py my-project/clients/jira.py

## Subfolders

- clients/   → working API client implementations
- schemas/   → canonical data shape definitions

## Relationship to vault/20-context/

| vault/20-context/apis/       | human-readable API reference  | inject into LLMs   |
| _reference/clients/          | Python implementation         | copy into projects |
| vault/20-context/schemas/    | human-readable schema def     | inject into LLMs   |
| _reference/schemas/          | Python dataclass              | copy into projects |

When one changes, update the other.
