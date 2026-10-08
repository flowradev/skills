# MCP

Docs: [MCP in dashboard](https://docs.flowra.dev/product/mcp-in-dashboard) · [Use MCP in Cursor](https://docs.flowra.dev/recipes/use-mcp-in-cursor)

Preferred path for OpenClaw, Hermes, Cursor, Claude, Windsurf. SDK is for your own backend.

## Endpoint

Hosted (no server ID). First authenticated request creates a default META server for the project:

```
https://mcp.flowra.dev/mcp
```

That default server binds six tools. Builder slugs (`FLOWRA_CREATE_OR_UPDATE_WORKFLOW`, and so on) are **not** bound — discover them and run them through `FLOWRA_MULTI_EXECUTE_TOOL`. No pin step is required.

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

## Optional: pinned NORMAL server

A named server with `mode: "NORMAL"` and `selectedTools` can bind builder slugs as direct tools. That is optional. Use it only when the user asked to pin tools or a client cannot call MULTI_EXECUTE.

Typical builder pin list (`FLOWRA_*` prefix required):

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
16. `FLOWRA_GET_WORKFLOW_EXECUTION`
17. `FLOWRA_GET_TOOL_EXECUTION_LOGS`

Create the server in the dashboard (or `flowra.mcp.create`) with `mode: "NORMAL"` and `selectedTools` set to that list.

**Runtime** — pin only the catalog/custom action slugs the job needs. No create/delete tools.

Deletes (`FLOWRA_DELETE_WORKFLOW`, and similar) are slugs. Run them via MULTI_EXECUTE: `confirm: false` first, show the preview, then `confirm: true` only after an explicit yes. Do not assume MCP blocks them.

## Client configs

OAuth (preferred): same URL, no headers. Do not commit live keys.

### Cursor

```json
{
  "mcpServers": {
    "flowra": {
      "url": "https://mcp.flowra.dev/mcp"
    }
  }
}
```

In Cursor: Settings → Cursor Settings → Tools & MCP → **Connect** next to `flowra`.

API key (CI / clients without OAuth): add `headers.x-api-key` and `headers.x-username` in the user's own `.cursor/mcp.json`, not in this plugin.

### Claude Code

```bash
claude mcp add --transport http flowra https://mcp.flowra.dev/mcp
```

### Windsurf / OpenClaw / Hermes

Same hosted URL, no headers. Copy the client snippet from **Dashboard → MCP → Install & Config → Sign in (OAuth)**.

Install this skill so the agent follows the builder sequence: `npx skills add flowradev/skills --skill flowra`. Hermes: copy this skill into `~/.hermes/skills/`.

## Flowra calling someone else's MCP

`FLOWRA_LOAD_EXTERNAL_MCP_TOOLS` only lists tools. It does not save them.

- Immediate use in chat: `FLOWRA_CALL_EXTERNAL_MCP_TOOL` with the same `url` / `headers` and the unprefixed tool name.
- Persist on an agent only if the user asked: `agent.tools.externalMcpConfigs: [{ name, url, headers?, tools }]`.
- HTTP/SSE only. `stdio` / `npx` / `uvx` / local process MCP is not supported.
- Do not put external MCP slugs in `agent.tools.pinnedSlugs` or in a NORMAL server's `selectedTools` (`pinnedSlugs`).
