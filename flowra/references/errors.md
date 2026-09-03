# Errors and recovery

`paused` is not failure. Read the execute/resume payload (status, `threadId`, `pauseMessage`, `viewFlowUrl`, `usage`) before retrying. Do not tell the user it “probably worked.” Do not start the run over.

Live field names change — if this file and the tool output disagree, trust the output and https://docs.flowra.dev/llms.txt.

## Paused (human gate)

Status `paused` means a `human_wait` node or agent `humanApproval` stopped the run.

1. Show `pauseMessage` (and the payload to approve).
2. Resume with the **same** `threadId`:

```
FLOWRA_RESUME_WORKFLOW
{ "threadId": "<from execute>", "approved": true }
```

3. `approved: false` rejects. Do not call `FLOWRA_EXECUTE_WORKFLOW` again for the same pause.

Missing `threadId` → `FLOWRA_GET_WORKFLOW_OR_AGENT_BY_ID` / list runs from the execute response. Do not invent one.

## Failed or incomplete

| Signal | Do |
|---|---|
| Tool / node error in ledger | Fix that slug or mapping; re-execute only after the user agrees |
| `draft` / validation error on save | Graph is incomplete; do not set `isActive: true` until it mocks clean |
| Wrong tool for the ID | Workflow id on `CREATE_OR_UPDATE_AGENT` (or reverse) → read first with `FLOWRA_GET_WORKFLOW_OR_AGENT_BY_ID` |
| Unknown / invented slug | `FLOWRA_DISCOVER_TOOLS` again; never guess `GMAIL_*` |
| Credits / balance too low | Stop; point at [billing.md](billing.md). Do not retry paid calls in a loop |
| Self-invocation blocked | The workflow cannot execute itself |

## Connections

`FLOWRA_MANAGE_CONNECTIONS` with base toolkit slugs from DISCOVER (`gmail`, `slack`). Full table: [connections.md](connections.md).

| status | Do |
|---|---|
| `initiated` | Show `redirectUrl`; wait; call again. Do not reuse an expired link — request a new one |
| `requires_parameters` | Ask listed fields; `specifyCustomAuth` |
| `requires_challenge` | OTP → `challengeResponse` |
| `needs_setup` | Owner adds app credentials in the dashboard |
| `failed` | Read `errorMessage`; reconnect that toolkit; do not rotate the project API key unless the key itself is invalid |
| MCP tools missing | Confirm builder pins ([mcp.md](mcp.md)), reconnect the MCP server, retry DISCOVER |

OAuth in the wrong Google/Slack account: retry in a clean browser profile. Do not paste client secrets into chat.

## Execute vs resume

- Static workflow: first run `testMode: true`. Production needs active connections (`testMode: false`).
- Agent runs are always live; `testMode` is ignored.
- After a **failed** production run, inspect the ledger, then execute a **new** run if the user wants a retry.
- After **paused**, only `RESUME` with `threadId`.

## What to show the user

Always return what the API returned: `viewFlowUrl`, `embedScript`, `threadId`, `pauseMessage`, `usage` / ledger. If none of those exist, say the call did not complete — do not infer success from HTTP 200 alone.
