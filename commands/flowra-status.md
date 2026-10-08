---
name: flowra-status
description: Check whether the Flowra MCP server is connected and healthy
---

Report Flowra MCP health. Do not mutate a project.

1. Are these six tools bound? `FLOWRA_DISCOVER_TOOLS`, `FLOWRA_GET_TOOL_SCHEMAS`, `FLOWRA_MANAGE_CONNECTIONS`, `FLOWRA_MULTI_EXECUTE_TOOL`, `FLOWRA_JS_REMOTE_WORKBENCH`, `FLOWRA_REMOTE_BASH`.
2. If missing: Not connected → add `https://mcp.flowra.dev/mcp` and ask the user to **Connect**.
3. If present but 401: Auth broken → reconnect.
4. If healthy: optional one DISCOVER with a harmless query to confirm the session. Do not connect new apps unless asked.
5. Reply with one of: **Healthy** / **Fresh install** / **Auth broken** / **Not connected**, plus what to click next.
