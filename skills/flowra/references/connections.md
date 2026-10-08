# Connections

Use `FLOWRA_MANAGE_CONNECTIONS` with toolkit **base** slugs from DISCOVER (`gmail`, `slack`). Do not invent OAuth URLs. Required fields: `toolkits`, `mode`, `reinitiateAll`.

- `mode: "connect"` (default): may start OAuth and return a `redirectUrl`.
- `mode: "status"`: read-only. Never mints a link or an `initiated` row.
- `reinitiateAll: false` unless the user asked to reconnect every toolkit in the list.

Show connection **labels** (email, username, app name). Never show a connection UUID.

| status | Do |
|---|---|
| `active` / `no_auth_required` | Continue |
| `not_connected` | Only in `mode: "status"`. Call again with `mode: "connect"` when the user wants to connect |
| `initiated` | Show the one `redirectUrl` as a markdown link and **end the turn**. Do not call again until the user says they finished in the browser. Then re-check with `mode: "status"` — a verify call must not mint a second link |
| `requires_parameters` | Ask only the listed fields; `specifyCustomAuth` |
| `requires_challenge` | OTP → `challengeResponse` (`connectionId` plus the listed fields) |
| `needs_setup` | Owner adds app credentials in the dashboard. Never ask an end user for `client_id` / `client_secret` |
| `failed` | Read `errorMessage`; reconnect that toolkit; do not rotate the project API key unless the key itself is invalid |

OAuth in the wrong Google/Slack account: retry in a clean browser profile. Do not paste client secrets into chat.

SDK door two: `flowra.connections.createLink({ authConfigId })` / `asUser`. Marketplace templates: [docs](https://docs.flowra.dev/product/marketplace).
