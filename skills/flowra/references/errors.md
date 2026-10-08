# Errors and recovery

`paused` is not failure. Read the execute/resume payload (status, `threadId`, `pauseMessage`, `viewFlowUrl`, `usage`) before retrying. Do not tell the user it “probably worked.” Do not start the run over.

Explain errors in plain language (“Your Slack connection needs to be re-authenticated” beats “Error 401”). Retry a failed call at most once, and only after fixing the input against the live schema.

Live field names change — if this file and the tool output disagree, trust the live tool output and schema. Tell the user this skill may be out of date.

Builder slugs run only as `tools[].toolSlug` inside `FLOWRA_MULTI_EXECUTE_TOOL`.

## Debug a run

Do not use `FLOWRA_GET_WORKFLOW_OR_AGENT_BY_ID` to debug a run — it returns the definition.

| Signal | Do |
|---|---|
| Failed or paused run | `FLOWRA_GET_WORKFLOW_EXECUTION` with `executionId` or `threadId` |
| One action failed | Then `FLOWRA_GET_TOOL_EXECUTION_LOGS` (`workflowId` / `toolSlug` / `logId`). Do not look for jsonl files on disk |
| Graph needs a one-node fix | `FLOWRA_PATCH_WORKFLOW_GRAPH` |
| New production run | Only after the user agrees |

`FLOWRA_RESUME_WORKFLOW` can take the `threadId` from `GET_WORKFLOW_EXECUTION`.

## Paused (human gate)

Status `paused` means a `human_wait` node or agent `humanApproval` stopped the run.

1. Show `pauseMessage` (and the payload to approve).
2. Resume with the **same** `threadId`:

```
FLOWRA_RESUME_WORKFLOW
{ "threadId": "<from execute or GET_WORKFLOW_EXECUTION>", "approved": true }
```

3. `approved: false` rejects. Do not call `FLOWRA_EXECUTE_WORKFLOW` again for the same pause.

## Failed or incomplete

| Signal | Do |
|---|---|
| Tool / node error in ledger | `GET_WORKFLOW_EXECUTION` then `GET_TOOL_EXECUTION_LOGS`; fix that slug or mapping; re-execute only after the user agrees |
| `draft` / validation error on save | Graph is incomplete; do not set `isActive: true` until it mocks clean |
| Wrong tool for the ID | Workflow id on `CREATE_OR_UPDATE_AGENT` (or reverse) → read first with `FLOWRA_GET_WORKFLOW_OR_AGENT_BY_ID` |
| Unknown / invented slug | `FLOWRA_DISCOVER_TOOLS` again; never guess `GMAIL_*` |
| Credits / balance too low | Stop; point at the live `usage` payload / dashboard. Do not retry paid calls in a loop |
| Self-invocation blocked | The workflow cannot execute itself |
| MCP tools missing | Add `https://mcp.flowra.dev/mcp`, click **Connect**, retry DISCOVER. A pinned NORMAL server is optional, not required |

## Connections

`FLOWRA_MANAGE_CONNECTIONS` with base toolkit slugs from DISCOVER (`gmail`, `slack`). Required: `toolkits`, `mode`, `reinitiateAll`. Canonical status table: [connections.md](connections.md).

## Execute vs resume

`FLOWRA_EXECUTE_WORKFLOW` runs a static workflow or an agent (same tool).

- Static: `testMode: true` (default) mocks tools and auto-approves `human_wait` — do not ask the user to approve, and the run does not appear in the executions/approvals list. `testMode: false` is a real run where `human_wait` pauses.
- Agent: `testMode: true` is a dry-run (no LLM call, no credits); `testMode: false` is a real, billed run.
- Inactive entities need `allowExecuteWhenInactive: true` for a production run.
- After a **failed** production run, inspect the ledger, then execute a **new** run if the user wants a retry.
- After **paused**, only `RESUME` with `threadId`.

## What to show the user

Always return what the API returned: `viewFlowUrl`, `embedScript`, `threadId`, `pauseMessage`, `usage` / ledger. If none of those exist, say the call did not complete — do not infer success from HTTP 200 alone.
