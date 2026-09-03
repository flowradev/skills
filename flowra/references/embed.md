# Site widget

Docs: [widgets and embeds](https://docs.flowra.dev/product/widgets-and-embeds)

Use a widget when the job is “put this agent on my website.” Do not build a custom chat UI unless they ask.

Preferred: `FLOWRA_CREATE_OR_UPDATE_AGENT` with `createEmbedWidget: true`, then paste `embedScript` from the response (see [examples.md](examples.md) job 2).

Dashboard → Workflows → Widgets still works (origin allowlist + throttle). Snippet shape:

```html
<script
  src="https://flowra.dev/embed.js"
  data-widget-id="WIDGET_ID"
  data-base-url="https://flowra.dev"
  data-display-mode="bubble"
  data-position="bottom-right"
  data-size="md"
  data-primary-color="#bb7400"
  data-header-text="Chat with us"
></script>
```

Fullscreen:

```html
<script
  src="https://flowra.dev/embed.js"
  data-widget-id="WIDGET_ID"
  data-base-url="https://flowra.dev"
  data-display-mode="fullscreen"
  data-primary-color="#bb7400"
  data-header-text="Assistant"
></script>
```

`data-widget-id` is public (not a secret). API keys must **not** go in the page.

## Client behaviour

Embed chat uses the widget id (`X-Widget-Id`) plus a per-visitor id (`X-Embed-Visitor-Id`). No dashboard session cookie.

If you build a custom embed client instead of `embed.js`:

- Call the public embed/graphify mirrors with `X-Widget-Id` only.
- Persist a visitor id in `localStorage` keyed by widget id.
- Honor the widget origin allowlist; do not proxy the project API key to the browser.

Self-hosted: point `src` and `data-base-url` at that origin, not `flowra.dev`.
