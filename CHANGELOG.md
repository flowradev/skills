# Changelog

## 0.2.0 — 2026-10-08

Marketplace packaging, a pass against the live default MCP server, and discovery files for skills.sh / Claude / Codex / the official MCP Registry.

- Add Claude marketplace (`.claude-plugin/marketplace.json`), Codex marketplace (`.agents/plugins/marketplace.json`), and `gemini-extension.json`.
- Add `skills/flowra-onboard`, `/flowra-setup` and `/flowra-status` commands, and `evals/` scenarios (operate confirm, cron, agent widget, paused, initiated, custom toolkit, first win).
- Package as a Cursor plugin: `.cursor-plugin/plugin.json`, `mcp.json`, `assets/logo.svg`, `LICENSE`, and `rules/flowra-safety.mdc`.
- Add `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.mcp.json`, `server.json`, and repo `llms.txt`.
- Move the skill to `skills/flowra/` so Cursor and `npx skills` discover it without a recursive fallback.
- README with logo, skills.sh / Registry badges, install table, comparison blurb, and a Security model section.
- Social preview (`assets/social-preview.png`, 1280×640) and square mark (`assets/logo-400.png`).
- Skill description rewritten around user intent (OAuth, schedule, approval, paused run) without fetching `llms.txt` at runtime.
- Document the six bound tools. Builder slugs (`FLOWRA_CREATE_OR_UPDATE_WORKFLOW`, and so on) run only as `tools[].toolSlug` inside `FLOWRA_MULTI_EXECUTE_TOOL`. A pinned NORMAL server is optional.
- Require an explicit yes in chat before write / send / delete / pay in Operate or the workbench.
- `FLOWRA_EXECUTE_WORKFLOW` runs both static workflows and agents. Agent `testMode: true` is a dry-run; `testMode: false` bills credits.
- Add required live-schema fields to copy-paste examples (`mode`, `reinitiateAll`, `syncResponseToWorkbench`, `allowExecuteWhenInactive`, `includeOutputSchema`).
- Debug with `FLOWRA_GET_WORKFLOW_EXECUTION` and `FLOWRA_GET_TOOL_EXECUTION_LOGS`. Document workbench / bash, inventory DISCOVER, `mode: "status"`, and session placement.
- Fix CLI install (`npm i -g @flowra/cli`) and Python (`pip install flowra-sdk`).
- Stop claiming MCP blocks deletes, inventing a credit-to-dollar ratio, or using guessed action slugs in examples.
