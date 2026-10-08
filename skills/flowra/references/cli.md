# CLI

Terminal door when MCP is not connected (Hermes, Codex CLI, scripts). Cursor / OpenClaw should still prefer [mcp.md](mcp.md). The CLI can Operate (discover → connect → execute). It cannot Build workflows or agents.

```bash
npm i -g @flowra/cli
# or: pnpm add -g @flowra/cli
```

From the public SDK repo (optional): `pnpm --dir cli install && pnpm --dir cli build && (cd cli && npm link)`.

Never `pip install flowra` (unrelated PyPI package). Python SDK: `pip install flowra-sdk`.

## Auth

`flowra login` opens the same Flowra sign-in as MCP. Never print tokens.

```bash
flowra login                    # browser OAuth — pick a project
flowra login --key <paste>      # API key instead (CI)
flowra whoami                   # verify; FLOWRA_API_KEY overrides the file
```

`x-username` defaults to `project_default_user` (`--username` / `FLOWRA_USERNAME`).

## Operate

Same sequence as MCP. Never invent slugs. Do not pipe `discover` through `head`. Writes still need an explicit yes in chat.

```bash
flowra discover "Gmail list recent inbox emails"
flowra connect gmail            # stop if status=initiated; show redirectUrl; re-run after OAuth
flowra execute <TOOL_SLUG> -d '{...}'
```

Reuse `sessionId` from discover (`--session-id`). `connect --wait` polls; agents omit it.

Durable cron / HITL / ledger: still [workflows.md](workflows.md) via MCP or SDK — not this CLI.
