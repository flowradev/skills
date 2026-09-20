# MCP

Docs: [MCP in dashboard](https://docs.flowra.dev/product/mcp-in-dashboard)

Preferred path for OpenClaw, Hermes, Cursor, Claude, Windsurf. SDK is for your own backend.

## Endpoint

Hosted (no server ID). First authenticated request creates a default META server for the project:

```
https://mcp.flowra.dev/mcp
```

Client pages with copy-paste config: [flowra.dev/agents](https://flowra.dev/agents).

Named servers still work on the same host:

```
https://mcp.flowra.dev/mcp/{serverId}
```

GET = SSE. POST = JSON-RPC.

**OAuth (preferred for Cursor / Claude):** add the URL with no headers. The client opens Flowra sign-in (Google, GitHub, or email), you pick a project, then it uses a Bearer token.

**API key (CI / clients without OAuth):**

```http
x-api-key: <project-api-key>
x-username: project_default_user
```

Any `x-username` is an external user (created if missing). Never a project UUID. Server is shared per project; identity is the username.

Copy install JSON from **Dashboard → MCP → Install** when possible.

## Two profiles

**Builder** — pin these exact slugs (`FLOWRA_*` prefix is required):

1. `FLOWRA_DISCOVER_TOOLS`
2. `FLOWRA_GET_TOOL_SCHEMAS`
3. `FLOWRA_MULTI_EXECUTE_TOOL`
4. `FLOWRA_MANAGE_CONNECTIONS`
5. `FLOWRA_CREATE_OR_UPDATE_TOOLKIT`
6. `FLOWRA_CREATE_OR_UPDATE_TOOL`
7. `FLOWRA_HTTP_REQUEST`
8. `FLOWRA_CREATE_OR_UPDATE_WORKFLOW`
9. `FLOWRA_CREATE_OR_UPDATE_AGENT`
10. `FLOWRA_PATCH_WORKFLOW_GRAPH`
11. `FLOWRA_MANAGE_TRIGGER`
12. `FLOWRA_EXECUTE_WORKFLOW`
13. `FLOWRA_RESUME_WORKFLOW`
14. `FLOWRA_GET_WORKFLOW_OR_AGENT_BY_ID`
15. `FLOWRA_LIST_WORKFLOWS`

Create the server in the dashboard (or `flowra.mcp.create`) with `mode: "NORMAL"` and `selectedTools` set to that list. META mode injects discovery + sandbox extras; still pin the builder tools you need.

**Runtime** — pin only the catalog/custom action slugs the job needs. No create/delete tools.

MCP blocks `FLOWRA_DELETE_WORKFLOW` and `FLOWRA_DELETE_SKILL`. Other deletes: `confirm: false` preview, then `confirm: true`.

## Client configs

OAuth (preferred): same URL, no headers. Do not commit live keys.

### Cursor

```json
{
  "mcpServers": {
    "flowra": {
      "url": "https://mcp.flowra.dev/mcp",
      "transport": "http"
    }
  }
}
```

API key (CI / clients without OAuth): add `headers.x-api-key` and `headers.x-username`.

### Claude Code

```bash
claude mcp add --transport http flowra https://mcp.flowra.dev/mcp
```

### Windsurf / OpenClaw / Hermes

Same hosted URL, no headers. Copy the client snippet from **Dashboard → MCP → Install & Config → Sign in (OAuth)**.

Install this skill so the agent follows the builder sequence: `npx skills add flowradev/skills --skill flowra`. Hermes: copy this skill into `~/.hermes/skills/`.

## Flowra calling someone else's MCP

`FLOWRA_LOAD_EXTERNAL_MCP_TOOLS` then pin via `agent.tools.externalMcpConfigs`: `{ name, url, headers?, tools }`. That is the opposite direction of this file.
