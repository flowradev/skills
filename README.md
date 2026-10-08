<p align="center">
  <img src="assets/logo.svg" width="72" alt="Flowra logo">
</p>

# Flowra — Agent Skill & Hosted MCP Server

**Run hosted AI agents and approval-gated workflows on Gmail, Slack, GitHub, Notion, Telegram, WhatsApp, Linear and 1,000+ apps — from Claude Code, Cursor, Codex, GitHub Copilot or any MCP client.** OAuth per account, a human approval gate before send/delete/pay, and a ledger of every tool call.

[![skills.sh](https://skills.sh/b/flowradev/skills)](https://skills.sh/flowradev/skills)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-io.github.flowradev%2Fmcp-blue)](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.flowradev/mcp)
[![Add Flowra MCP to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=flowra&config=eyJ1cmwiOiJodHRwczovL21jcC5mbG93cmEuZGV2L21jcCJ9)

[Product](https://flowra.dev) · [Docs](https://docs.flowra.dev) · [SDK](https://github.com/flowradev/sdk) · [Changelog](./CHANGELOG.md) · [skills.sh](https://skills.sh/flowradev/skills/flowra)

This repo is the **agent skill + Cursor/Claude/Codex plugin** for Flowra. From your backend, use the [SDK](https://github.com/flowradev/sdk) (`@flowra/sdk`, `flowra-sdk`, `@flowra/cli`).

## What's included

| Component | Purpose |
|---|---|
| `mcp.json` / `.mcp.json` | Registers `https://mcp.flowra.dev/mcp` (OAuth, no keys). Six tools: discover, schemas, connect, multi-execute, workbench, bash. |
| `skills/flowra` | Routes operate / build / edit / debug / credits to the right Flowra calls. |
| `skills/flowra-onboard` | First install: Connect MCP and one read-only first win. |
| `commands/` | `/flowra-setup` and `/flowra-status`. |
| `evals/` | Behavioral scenarios the skill must pass. |
| `rules/flowra-safety.mdc` | Reads are free, writes need your yes; untrusted content is never an instruction. |

## Install in 30 seconds

**1. Skill** (Claude Code, Cursor, Codex, Copilot, OpenClaw, Hermes):

```bash
npx skills add flowradev/skills --skill flowra
```

**2. Hosted MCP server** — no API key needed; sign in with OAuth:

```text
https://mcp.flowra.dev/mcp
```

| Client | How |
|---|---|
| Cursor | Settings → Tools & MCP → **Connect** next to `flowra` (or install the Flowra plugin) |
| Claude Code | `claude mcp add --transport http flowra https://mcp.flowra.dev/mcp` |
| VS Code / Copilot | `@mcp` in Extensions, or add the URL to `.vscode/mcp.json` |
| Skill only | `npx skills add flowradev/skills --skill flowra` |
| CI / no OAuth | Project API key in your own config — never in this repo |

Cursor Marketplace: search "Flowra", or `/add-plugin flowra` once listed.

## First run

1. Connect the MCP server and pick a Flowra project.
2. Ask: "List my 5 latest Gmail subjects with Flowra."
3. Then: "Every weekday at 9, post a Slack recap of my inbox. Ask me before posting."

## What you can ask

- "Connect Gmail on Flowra and list my latest subjects."
- "Every weekday at 9:00, post a Slack recap of new Linear issues — ask me before posting."
- "This Flowra run is paused — show the ledger and resume it."

## Why Flowra (vs Zapier MCP, Composio, n8n)

- **Agent or locked workflow** on the same project — not just a tool catalog.
- **Human approval gate** on any step, including cron runs.
- **Run ledger**: inputs, outputs and credits for every tool call.
- **Missing app?** Describe the REST endpoint and Flowra builds the toolkit.

## Security model

Inbound mail, chat and webhook content is treated as untrusted data. The skill never executes instructions found in payloads and never skips approval gates. Reads run freely; writes (send, post, create, update, delete, pay) need an explicit yes in this chat. Durable automations still need a `human_wait` node or agent `humanApproval`. No API keys are stored in this repo.

**Use when** you want a scheduled or approved automation instead of a local script or an n8n, Zapier, or Make canvas.

**Skip when** there is no Flowra project, or you are already editing an n8n, Zapier, or Make graph you own.

## CI / clients without OAuth

Add headers only in your own `.cursor/mcp.json`. Never commit a key.

```json
{
  "mcpServers": {
    "flowra": {
      "url": "https://mcp.flowra.dev/mcp",
      "headers": {
        "x-api-key": "<your-project-api-key>",
        "x-username": "project_default_user"
      }
    }
  }
}
```

## Local testing

```bash
mkdir -p ~/.cursor/plugins/local
ln -sfn "$PWD" ~/.cursor/plugins/local/flowra
```

Then run Developer: Reload Window.

## Layout

```text
.cursor-plugin/plugin.json
.claude-plugin/plugin.json
.codex-plugin/plugin.json
mcp.json
.mcp.json
server.json
commands/flowra-setup.md
commands/flowra-status.md
evals/
rules/flowra-safety.mdc
skills/flowra/SKILL.md
skills/flowra-onboard/SKILL.md
skills/flowra/references/
```

MIT © Flowra
