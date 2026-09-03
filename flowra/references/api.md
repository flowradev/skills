# Auth and API

Docs: [authentication](https://docs.flowra.dev/authentication) · [projects and keys](https://docs.flowra.dev/product/projects-and-keys) · [external users](https://docs.flowra.dev/product/external-users)

## Headers

| Header | Role |
|---|---|
| `x-api-key` | Project API key. Required for the public API and MCP. |
| `x-username` | External user to act as. Created if missing. Shows up under External users. |

Get a key from **Dashboard → Project settings → API Keys**. Store it as `FLOWRA_API_KEY`. Same headers on MCP.

JWT Bearer is for the dashboard session, not app backends.

## Base URL

Default SDK origin: `https://flowra.dev`.  
HTTP paths are under `/api/v1/...`.

```http
GET /api/v1/users/profile
x-api-key: <project-key>
```

Override origin only for self-hosted / staging:

```ts
new Flowra({ apiKey, baseUrl: 'https://your-origin.example' })
```

## External users (`asUser`)

Use this when the caller is an end-customer of *your* product, not the Flowra project owner.

```ts
const user = flowra.asUser('customer_42');
await user.connections.createLink({ authConfigId: '...' });
await user.workflows.run(id, { input: { message: 'hi' } });
```

```python
user = flowra.as_user("customer_42")
```

Rules:

- Username is an opaque string you choose (`customer_42`, email, etc.).
- **Never** put the project UUID in `x-username`.
- Project default: `project_default_user`.
- Agents, connections, files, and tables stay **separate per username**.
- The MCP server is shared for the project; identity is still `x-username`.

Manage users: `flowra.users.list` / `.create` / `.getByUsername`.

## OpenAPI

Full HTTP surface: [docs.flowra.dev/api-reference](https://docs.flowra.dev/api-reference).

TypeScript escape hatch: `flowra.raw` (generated operations).  
Python escape hatch: `flowra.request("GET", "/api/v1/toolkits", query={"limit": 5})`.
