# Toolkit registry

Docs: [toolkits](https://docs.flowra.dev/product/toolkits-and-tools) · [connections](https://docs.flowra.dev/product/connections)

A toolkit you mint is **project-scoped**. It does not join the global catalog.

## Contents

- [1. Discover](#1-discover-always)
- [2. Connect](#2-connect)
- [3. Register only if DISCOVER has no app](#3-register-only-if-discover-has-no-app)
- [4. After register](#4-after-register)

## 1. Discover (always)

```
FLOWRA_DISCOVER_TOOLS
{
  "userMessage": "<exact user text>",
  "intentSummary": "<one sentence; put schedules here, not in useCase>",
  "includeInputSchemas": true,
  "session": { "generate_id": true },
  "queries": [
    { "useCase": "Gmail list recent inbox messages" },
    { "useCase": "Slack post a message to a channel" }
  ]
}
```

Reuse `data.session.id` on later DISCOVER / GET_TOOL_SCHEMAS / MANAGE_CONNECTIONS / MULTI_EXECUTE_TOOL. Do not attach `session` to CREATE_AGENT / CREATE_WORKFLOW arguments.

- One atomic English `useCase` per query; include the app name.
- Use only slugs in `mainToolSlugs` / `relatedToolSlugs`.
- If `hasActiveConnection` is false → connect before execute.
- `toolkitSlugs` pins an app (`gmail`, `github`). Never pass ACTION slugs there.

**Inventory** — list or search one app's tools (paginated):

```
FLOWRA_DISCOVER_TOOLS
{
  "mode": "inventory",
  "toolkitSlugs": ["github"],
  "query": "issue",
  "userMessage": "List GitHub issue tools",
  "intentSummary": "Inventory of GitHub issue tools",
  "includeInputSchemas": false
}
```

If `inventory.truncated` is true, call again with the same `toolkitSlugs` + `query` and `offset=inventory.nextOffset`.

To load schemas later:

```
FLOWRA_GET_TOOL_SCHEMAS
{
  "toolSlugs": ["<slug from DISCOVER>"],
  "includeOutputSchema": false,
  "session": { "id": "<session.id>" }
}
```

To run a catalog **action** (not as a bound function):

```
FLOWRA_MULTI_EXECUTE_TOOL
{
  "session": { "id": "<session.id>" },
  "syncResponseToWorkbench": false,
  "tools": [
    { "toolSlug": "<exact slug from DISCOVER>", "arguments": { } }
  ]
}
```

Triggers (`type=trigger`) cannot go through MULTI_EXECUTE. Register them with `FLOWRA_MANAGE_TRIGGER`.

## 2. Connect

```
FLOWRA_MANAGE_CONNECTIONS
{
  "toolkits": ["gmail", "slack"],
  "mode": "connect",
  "reinitiateAll": false,
  "session": { "id": "<session.id>" }
}
```

Canonical status table (initiated → one link and stop; verify with `mode: "status"`): [connections.md](connections.md).

Do not loop. One user-facing link, then wait.

## 3. Register only if DISCOVER has no app

### Toolkit — `FLOWRA_CREATE_OR_UPDATE_TOOLKIT`

Create: `slug`, `name`, `description` required.

- `slug`: lowercase `snake_case`, **max 2 segments** (`gmail`, `google_ads`, `httpbin`). Do not append `:publicId`.
- Auth is XOR: `noAuth: true` **or** `authSchemes` + `authConfigDetails` + usually `baseUrl`. Never mix `noAuth: true` with auth schemes.
- `authFlow`: `static_secret` \| `cookie_paste` \| `password` \| `password_otp` \| `oauth` \| `whatsapp_qr` \| `zernio_connect` (Instagram Business Login). Password/OTP needs `authRecipe`.
- Login / OTP / auth paths belong in toolkit `authRecipe` — never save them as tools.

```
FLOWRA_CREATE_OR_UPDATE_TOOLKIT
{
  "slug": "httpbin",
  "name": "HTTP Bin",
  "description": "Probe REST API",
  "baseUrl": "https://httpbin.org",
  "noAuth": true
}
```

Update: prefer `toolkitId` from the create response; omitted fields stay.

### Tool — `FLOWRA_CREATE_OR_UPDATE_TOOL`

Create: `toolkitSlug`, `slug`, `name`, `description`, and **`httpEndpoint` XOR `script`**.

- Tool `slug`: `UPPER_SNAKE_CASE` starting with `TOOLKITPREFIX_` (`httpbin` → `HTTPBIN_GET_JSON`).
- Prefer **`httpEndpoint`** for REST (`method`, `path` with `{param}`, optional `queryParams` / `bodyParams` / `baseUrl`).
- **`script`** only when REST cannot express it. Must be exactly `async function run(state) { ... }` returning `{ data, successful, error }`. Secrets via `state.authConfigCredentials` / `state.accountData.val`. No top-level `await`/`fetch`.
- Sending both → validation error. On update, `httpEndpoint` / `script` / `inputParameters` **replace** the whole field.
- After `FLOWRA_HTTP_REQUEST`, you can pass `requestSample` / `responseSample` so the platform can draft the tool schema. Do not invent field names when a sample exists.

```
FLOWRA_CREATE_OR_UPDATE_TOOL
{
  "toolkitSlug": "httpbin",
  "slug": "HTTPBIN_GET_JSON",
  "name": "Get JSON",
  "description": "GET /json",
  "noAuth": true,
  "httpEndpoint": {
    "method": "GET",
    "path": "/json",
    "baseUrl": "https://httpbin.org"
  }
}
```

Probe unknown APIs first with `FLOWRA_HTTP_REQUEST`, then mint the tool.

## 4. After register

Connect (`MANAGE_CONNECTIONS` with the new slug) if the toolkit needs auth, then execute via `FLOWRA_MULTI_EXECUTE_TOOL` or pin the slug on a workflow/agent.

SDK door two: `flowra.toolkits.create` / `flowra.tools.create`. Public OpenAPI `tools.create` uses **`script`**, not `httpEndpoint`. Prefer MCP builder slugs (via MULTI_EXECUTE) for REST.
