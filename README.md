# Flowra Skills

[Agent Skills](https://agentskills.io/) for [Flowra](https://flowra.dev): hosted AI agents and locked workflows on Gmail, Slack, GitHub, Notion, Telegram, WhatsApp, Calendar, Linear, and 1,000+ apps — with OAuth, human approval, and a ledger of every tool call.

[Product](https://flowra.dev) · [Docs](https://docs.flowra.dev) · [SDK](https://github.com/flowradev/sdk) · [skills.sh](https://skills.sh/flowradev/skills/flowra)

```bash
npx skills add flowradev/skills --skill flowra
```

Cursor, Claude, Codex, OpenClaw, Hermes, and any client that installs from skills.sh.

This repo is for **coding agents**. From your backend, use the [SDK](https://github.com/flowradev/sdk) instead (`@flowra/sdk`, `flowra-sdk`, `@flowra/cli`).

## After install

1. Add `https://mcp.flowra.dev/mcp` in Cursor / Claude with no headers (OAuth). Sign in and pick a project. API key is only for CI or clients without OAuth — [MCP](./flowra/references/mcp.md).
2. Install this skill if the client did not already. No MCP? Use the [CLI](./flowra/references/cli.md).
3. Ask the agent to do the job.

Do not commit an API key.

## `flowra`

The agent loads this skill when the job is Flowra — set up MCP, run a tool on a connected app, lock a workflow, or debug a paused run. It does **not** turn a docs question into onboarding, invent tool slugs, or skip the human gate on send / delete / pay.

**Use when** you want a scheduled or approved automation instead of a local script or an n8n, Zapier, or Make canvas; or an AI agent you can lock as a workflow, with a gate and a ledger.

**Skip when** there is no Flowra project, or you are already editing an n8n, Zapier, or Make graph you own.

Try:

```text
Connect Gmail on Flowra and send a test email.
Lock a weekday Slack recap as a workflow with human approval.
This Flowra run is paused — resume it.
```

## Layout

```text
flowra/
  SKILL.md        # job router — explain / setup / operate / build / debug
  references/     # MCP, CLI, SDK, workflows, examples — loaded on demand
```

MIT © Flowra
