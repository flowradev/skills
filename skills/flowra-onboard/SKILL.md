---
name: flowra-onboard
description: >
  Connects and verifies the Flowra hosted MCP server (OAuth, project pick)
  and runs one safe read-only first win. Use when the user says "set me up",
  "how do I get started with Flowra", "connect Flowra MCP", "install Flowra",
  "what is Flowra MCP", or when FLOWRA_* tools are missing. Do not use to
  send mail, lock a workflow, register a custom toolkit, or debug a paused
  run — those belong to the flowra skill.
license: MIT
compatibility: Requires network access. Prefers the Flowra MCP server (https://mcp.flowra.dev/mcp) or @flowra/cli.
metadata:
  author: Flowra
  version: "0.2.0"
  homepage: https://flowra.dev
---

# Flowra onboard

Get the user to a **healthy MCP connection** and one **read-only** proof. Then stop. Do not build a workflow, send mail, or turn this into Operate/Build.

## When to use vs `flowra`

| Ask | Skill |
|---|---|
| First install, "set me up", missing `FLOWRA_*` tools, 401 | **This skill** |
| One action now, schedule, widget, custom toolkit, paused run | `flowra` |

If they already have six healthy `FLOWRA_*` tools and asked for a job, switch to `flowra`.

## 1. Diagnose

| State | How it looks | Do |
|---|---|---|
| Healthy | Six bound tools present: `FLOWRA_DISCOVER_TOOLS`, `FLOWRA_GET_TOOL_SCHEMAS`, `FLOWRA_MANAGE_CONNECTIONS`, `FLOWRA_MULTI_EXECUTE_TOOL`, `FLOWRA_JS_REMOTE_WORKBENCH`, `FLOWRA_REMOTE_BASH` | Skip to first win |
| Fresh install | Server listed, **Connect** still needed | Ask them to click **Connect** |
| Auth broken | Tools present but 401 / unauthorized | Reconnect the MCP server |
| Not connected | `FLOWRA_*` tools missing | Add the URL, then Connect |

Cursor: Settings → Cursor Settings → Tools & MCP → **Connect** next to `flowra`.

URL (OAuth, no headers, no API key in the repo):

```text
https://mcp.flowra.dev/mcp
```

Claude Code: `claude mcp add --transport http flowra https://mcp.flowra.dev/mcp`

CLI (no MCP): `npm i -g @flowra/cli` then `flowra login`. Verify with `flowra whoami`.

CI / no OAuth: they paste a project API key into **their** `.cursor/mcp.json` as `headers.x-api-key` + `x-username: project_default_user`. Never print the key. Never commit it.

## 2. First win (read-only)

After tools are healthy, prove the connection with **one read**:

1. `FLOWRA_DISCOVER_TOOLS` with `session: { generate_id: true }`, `includeInputSchemas: true`, and a list/search `useCase` (Gmail subjects, Slack channels, GitHub issues — whatever they already use).
2. If `hasActiveConnection` is false: `FLOWRA_MANAGE_CONNECTIONS` with `mode: "connect"`, `reinitiateAll: false`. Status `initiated` → show the one `redirectUrl` as a markdown link and **end the turn**. Re-check with `mode: "status"` only after they say they finished.
3. `FLOWRA_MULTI_EXECUTE_TOOL` with the **list/get/search** slug from DISCOVER and `syncResponseToWorkbench: false`.

Do **not** send, post, create, update, delete, pay, or `FLOWRA_CREATE_OR_UPDATE_WORKFLOW`. If they asked to send a test email, list first, then hand off to `flowra` (writes need an explicit yes).

Show what came back (subjects, titles, labels — not connection UUIDs). Do not guess success.

## 3. Hand off

Tell them they are ready. Next asks ("every weekday post to Slack", "this run is paused") use the `flowra` skill.

More MCP/CLI/SDK detail: [../flowra/references/mcp.md](../flowra/references/mcp.md), [../flowra/references/cli.md](../flowra/references/cli.md), [../flowra/references/sdk.md](../flowra/references/sdk.md).
