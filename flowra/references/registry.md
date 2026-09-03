# Toolkit registry

Docs: [toolkits](https://docs.flowra.dev/product/toolkits-and-tools) · [connections](https://docs.flowra.dev/product/connections)

A toolkit you mint is **project-scoped**. It does not join the global catalog.

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

Reuse `data.session.id` on later DISCOVER / GET_TOOL_SCHEMAS / MANAGE_CONNECTIONS / MULTI_EXECUTE_TOOL.

- One atomic English `useCase` per query; include the app name.
- Use only slugs in `mainToolSlugs` / `relatedToolSlugs`.
- If `hasActiveConnection` is false → connect before execute.

To run a catalog **action** (not as a bound function):

```
FLOWRA_MULTI_EXECUTE_TOOL
{
  "session": { "id": "<session.id>" },
  "tools": [
    { "toolSlug": "<exact slug from DISCOVER>", "arguments": { } }
  ]
}
```

Triggers (`type=trigger`) cannot go through MULTI_EXECUTE. Register them with `FLOWRA_MANAGE_TRIGGER`.

Optional: `FLOWRA_GET_TOOL_SCHEMAS` with the same `session.id` if you skipped `includeInputSchemas`.

## 2. Connect

```
FLOWRA_MANAGE_CONNECTIONS
{
  "toolkits": ["gmail", "slack"],
  "session": { "id": "<session.id>" }
}
```

| status | Agent must |
|---|---|
| `active` / `no_auth_required` | Proceed |
| `initiated` | Show `redirectUrl` as a markdown link. Wait. Call again with the same `toolkits` |
| `requires_parameters` | Ask only `requiredParameters` fields, then recall with `specifyCustomAuth` |
| `requires_challenge` | Collect OTP; recall `{ challengeResponse: { connectionId, otp } }` |
| `needs_setup` | Owner must add app credentials in the dashboard. Never ask the end user for `client_id` / `client_secret` |
| `failed` | Read `errorMessage` before retry |

Do not loop. One user-facing link, then wait.

## 3. Register only if DISCOVER has no app

### Toolkit — `FLOWRA_CREATE_OR_UPDATE_TOOLKIT`

Create: `slug`, `name`, `description` required.

- `slug`: lowercase `snake_case`, **max 2 segments** (`gmail`, `google_ads`, `httpbin`). Do not append `:publicId`.
- Auth is XOR: `noAuth: true` **or** `authSchemes` + `authConfigDetails` + usually `baseUrl`. Never mix `noAuth: true` with auth schemes.
- `authFlow`: `static_secret` \| `cookie_paste` \| `password` \| `password_otp` \| `oauth` \| `whatsapp_qr`. Password/OTP needs `authRecipe`.

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

SDK door two: `flowra.toolkits.create` / `flowra.tools.create`. Public OpenAPI `tools.create` uses **`script`**, not `httpEndpoint`. Prefer MCP builder tools for REST.
