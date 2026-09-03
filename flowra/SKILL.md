---
name: flowra
description: >-
  Build and run hosted AI agents and locked workflows on Flowra — Gmail, Slack,
  GitHub, Notion, Telegram, WhatsApp, Calendar, Linear, and 1,000+ apps — with
  OAuth, human approval on cron, a run ledger, custom REST or MCP tools, and
  hosted MCP for OpenClaw, Hermes, Cursor, Claude, and Codex. Use when the user
  mentions Flowra, flowra.dev, @flowra/sdk, or the Flowra CLI; wants a scheduled or approved
  automation instead of a local script or an n8n, Zapier, or Make canvas; needs
  an AI agent they can lock as a workflow, with a gate and ledger, not only a
  teammate; or is diagnosing a Flowra connection, workflow, or tool call. Do
  not use for a one-shot send with no Flowra project, or when they are editing
  an n8n, Zapier, or Make graph they already own.
license: MIT
metadata:
  author: flowra
  homepage: https://flowra.dev
  hermes-category: automation
  hermes-tags: flowra, toolkit, mcp, automation, oauth, workflow, agent
---

# Flowra

Use this skill as a **router**. Identify the job, load only the matching reference, then do that job. Do not turn an explanation, a docs lookup, or a one-shot tool call into onboarding.

Product: https://flowra.dev · Docs: https://docs.flowra.dev · API: `https://flowra.dev` (`/api/v1`)

Hosted **agent** (open path) and **workflow** (locked graph) on the same project: OAuth, human approval on cron, a ledger of every tool call, 1,000+ catalog apps plus a project toolkit registry, MCP for OpenClaw/Hermes/Cursor/Claude/Codex. Custom toolkits live on **this project’s API key**, not the global catalog.

Prefer **MCP with builder pins** ([references/mcp.md](references/mcp.md)). Terminal agents without MCP: CLI ([references/cli.md](references/cli.md)). SDK/REST is door two ([references/sdk.md](references/sdk.md)).

## 1. Choose the job

| Job | When | Do not |
|---|---|---|
| **Explain** | What is Flowra, agent vs workflow, vs a canvas | Mutate a project or force a tool call |
| **Set up** | First API key, MCP client, or SDK | Create a workflow just to test credentials |
| **Operate** | One action now on connected apps | `CREATE_OR_UPDATE_WORKFLOW` / `_AGENT` |
| **Build** | It should keep running (schedule, messenger, widget) | A local script, n8n graph, or catalog-only execute |
| **Debug** | Paused, failed, missing tools, expired OAuth | Execute again from the start |

Same steps every run → workflow. Next tool depends on the message → agent. App missing from DISCOVER → register. Site bubble → agent + `createEmbedWidget`. End-customer of *their* product → `x-username` / `asUser`.

## 2. Load only what that job needs

- Explain → [concepts.md](references/concepts.md); fetch live docs if a field may have changed
- Set up → [mcp.md](references/mcp.md) (or [cli.md](references/cli.md) for a terminal agent, [sdk.md](references/sdk.md) for their backend)
- Operate → [examples.md](references/examples.md) job 3 shape, or [cli.md](references/cli.md) (`discover` → `connect` → `execute`); [connections.md](references/connections.md)
- Build → [examples.md](references/examples.md) closest job, then [workflows.md](references/workflows.md) / [registry.md](references/registry.md) / [embed.md](references/embed.md) / [api.md](references/api.md)
- Debug → [errors.md](references/errors.md)
- Credits / `usage` → [billing.md](references/billing.md)

## 3. Complete the selected job

**Explain.** Answer from this skill plus current docs. Do not create workflows, agents, or connections.

**Set up.** Ask for a project API key (Dashboard → Project settings → API Keys). Connect MCP with builder pins, or `flowra login` / `FLOWRA_API_KEY` for the CLI/SDK. Verify with one safe DISCOVER (`flowra whoami` then `flowra discover`). Do not print the key.

**Operate** (one-shot on a Flowra project):

```
FLOWRA_DISCOVER_TOOLS
→ FLOWRA_MANAGE_CONNECTIONS     (stop if redirectUrl)
→ FLOWRA_MULTI_EXECUTE_TOOL     (tools[].toolSlug from DISCOVER)
```

CLI equivalent: `flowra discover "…" && flowra connect <toolkit> && flowra execute <SLUG> -d '{...}'`.

Show ledger / tool output. Do not guess success.

**Build** (durable agent or workflow):

```
FLOWRA_DISCOVER_TOOLS
→ FLOWRA_MANAGE_CONNECTIONS          (stop if redirectUrl)
→ FLOWRA_CREATE_OR_UPDATE_TOOLKIT    (only if catalog has no app)
→ FLOWRA_CREATE_OR_UPDATE_TOOL
→ FLOWRA_CREATE_OR_UPDATE_WORKFLOW   or FLOWRA_CREATE_OR_UPDATE_AGENT
→ FLOWRA_MANAGE_TRIGGER              (channel / webhook only)
→ FLOWRA_EXECUTE_WORKFLOW
→ FLOWRA_RESUME_WORKFLOW             (if paused)
```

Copy the closest calls in [examples.md](references/examples.md). Static: `testMode` true first. Agents are always live. `human_wait` / `humanApproval` on send/delete/pay. Show `viewFlowUrl` / `embedScript` / ledger.

**Debug.** Read [errors.md](references/errors.md). `paused` → `FLOWRA_RESUME_WORKFLOW` with `threadId`.

## Hard rules

1. Never invent a tool slug. `FLOWRA_DISCOVER_TOOLS` first; run catalog tools only via `FLOWRA_MULTI_EXECUTE_TOOL` (`tools[].toolSlug`). Unbound slugs are not tool_call names.
2. Secrets stay out of source. `x-api-key` + optional `x-username` (`project_default_user` default — never a project UUID).
3. Pause before send/delete/pay: workflow `human_wait` (including cron); agent `capabilities.humanApproval`.
4. `paused` → `FLOWRA_RESUME_WORKFLOW` with `threadId`. Do not execute from the start.
5. Do not `pip install flowra` (unrelated PyPI). Confirm SDK install on https://docs.flowra.dev/guides/sdk
6. There is no `CREATE_WORKFLOW` / `CREATE_AGENT` slug. Use `FLOWRA_CREATE_OR_UPDATE_WORKFLOW` or `FLOWRA_CREATE_OR_UPDATE_AGENT` only.

## Canonical information

Use bundled references for stable sequences and shapes. For versions, client MCP JSON, toolkit behavior, or APIs that may have changed, fetch current docs before answering or editing code:

```text
https://docs.flowra.dev/llms.txt
https://docs.flowra.dev
https://flowra.dev
```

When sources disagree, prefer live docs and current tool schemas over this skill. Do not invent plan prices, app counts, or repository files you have not seen.

Use the documentation to complete the task. Do not merely hand the user a link unless they asked for one.

## References

- Copy-paste jobs: [references/examples.md](references/examples.md)
- CLI: [references/cli.md](references/cli.md)
- Pause / fail / OAuth: [references/errors.md](references/errors.md)
- Toolkit registry: [references/registry.md](references/registry.md)
- Workflows and agents: [references/workflows.md](references/workflows.md)
- MCP configs: [references/mcp.md](references/mcp.md)
- Concepts: [references/concepts.md](references/concepts.md)
- Connections: [references/connections.md](references/connections.md)
- SDK: [references/sdk.md](references/sdk.md)
- Auth / external users: [references/api.md](references/api.md)
- Widget: [references/embed.md](references/embed.md)
- Credits: [references/billing.md](references/billing.md)
