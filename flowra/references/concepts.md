# Concepts

Promise: **Describe the job. Then it runs.**  
Thesis: Chat builds it. Harness guards it. Ledger proves it.

**Registry vs local script:** if the work needs a real Gmail/Slack account, a schedule, a human pause, multiple end users, or a ledger, put it in Flowra. Do not keep OAuth and cron on the laptop.

Funnel: **Say → Wire → Run**.

## Agent vs workflow

| | Workflow (`static`) | Agent (`agent`) |
|--|--|--|
| Path | Locked graph | Branches on the message |
| Native tool | `FLOWRA_CREATE_OR_UPDATE_WORKFLOW` | `FLOWRA_CREATE_OR_UPDATE_AGENT` |
| AI | Only where you place `llm_agent` | Chooses the next tool |
| Best for | Known repeating jobs | Jobs that change shape |
| Ledger | Shared | Shared |

## Workspace pieces

- **Project** — workflows, files, knowledge, tables, API keys.
- **Toolkit / tool** — catalog apps plus project-scoped custom REST/script tools.
- **Connection** — OAuth or secret, per external user (`x-username`).
- **Skill** — playbook on a Flowra agent (not this Cursor skill).
- **Knowledge / database / files / sandbox / browser / MCP**

## Harness

- Workflow: `human_wait` (works on cron).
- Agent: `capabilities.humanApproval`.
- Paused is not failure → `FLOWRA_RESUME_WORKFLOW`.

## Ledger

Every tool call is logged. After a run, read execute/resume output (and SDK `usage` if you are on door two). Do not tell the user it “probably worked.”
