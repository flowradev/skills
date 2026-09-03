# Connections (short)

Full sequence: [registry.md](registry.md).

Use `FLOWRA_MANAGE_CONNECTIONS` with toolkit **base** slugs from DISCOVER (`gmail`, `slack`). Do not invent OAuth URLs.

| status | Do |
|---|---|
| `active` / `no_auth_required` | Continue |
| `initiated` | Show `redirectUrl`; wait; call again |
| `requires_parameters` | Ask listed fields; `specifyCustomAuth` |
| `requires_challenge` | OTP → `challengeResponse` |
| `needs_setup` | Owner adds app credentials in the dashboard |
| `failed` | Read `errorMessage` |

SDK door two: `flowra.connections.createLink({ authConfigId })` / `asUser`. Marketplace templates: [docs](https://docs.flowra.dev/product/marketplace).
