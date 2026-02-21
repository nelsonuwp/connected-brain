# _reference/schemas/

Canonical data shape definitions. One file per domain entity.

**Expected files:**
- jira_issue.py, jsm_ticket.py, gitlab_mr.py, briefing.py

**How to use:**
1. cp _reference/schemas/jira_issue.py your-project/schemas/jira_issue.py
2. Strip fields your project doesn't need
3. Your project owns its copy

**Note:** vault/20-context/schemas/ has the markdown explanation of these shapes.
This folder has the Python implementation. Keep them in sync.
