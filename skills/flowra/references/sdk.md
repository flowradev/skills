# SDK (door two)

Prefer MCP ([mcp.md](mcp.md)) when OpenClaw/Hermes/Cursor is talking to Flowra. Use the CLI ([cli.md](cli.md)) when the agent can only run shell commands. Use the SDK inside **your** backend.

Docs: [guides/sdk](https://docs.flowra.dev/guides/sdk)

| Package | Install | Import |
|---|---|---|
| TypeScript | `npm install @flowra/sdk` | `import { Flowra } from '@flowra/sdk'` |
| Python | `pip install flowra-sdk` | `from flowra import Flowra` |
| CLI | `npm i -g @flowra/cli` | `flowra` |

Never `pip install flowra` — that PyPI name is an unrelated package.

## TypeScript

```ts
import { Flowra, extractStreamUsage, parseSseChunk } from '@flowra/sdk';

const flowra = new Flowra({
  apiKey: process.env.FLOWRA_API_KEY!,
  // baseUrl: 'https://flowra.dev',
  // username: 'customer_42',
});

await flowra.getProfile();
await flowra.tools.list({ limit: 10 });
const run = await flowra.workflows.run('WORKFLOW_ID', {
  input: { message: 'hello' },
});
```

Act as an end user: `flowra.asUser('customer_42')`.

Every public API-key operation is on the `Flowra` facade. Generated names remain on `flowra.raw`.

## Python

```python
import os
from flowra import Flowra, extract_stream_usage

flowra = Flowra(api_key=os.environ["FLOWRA_API_KEY"])
flowra.tools.list(limit=10)
flowra.workflows.run("WORKFLOW_ID", {"input": {"message": "hello"}})
user = flowra.as_user("customer_42")
```

HTTP errors raise `FlowraAPIError` (`status_code`, `body`).

If the Python package is not installed in the environment, use REST with `x-api-key`.

## Namespaces

`tools` · `toolkits` · `skills` · `workflows` · `connections` · `authConfigs` / `auth_configs` · `users` · `triggers` · `chat` · `files` · `knowledge` · `database` · `sandbox` · `mcp` · `llm` · `browser` · `usage`

## Chat stream + usage

`POST /api/v1/graphify/threads/{thread_id}/runs/stream` ends with:

```
event: usage
data: { "runCredits": 142, "threadCreditsTotal": 890, "balanceRemaining": 48200, "executionId": "...", "breakdown": { "ai_model": 120, "tool": 22 } }
```

```ts
const usage = extractStreamUsage(events);
```

```python
for event in flowra.chat.stream(thread_id, body, as_events=True):
    if event["event"] == "usage":
        print(event["data"]["runCredits"])
```

## Files

Python: `flowra.files.upload("document", "/path/to/file.pdf")` then `flowra.files.download(file_id)` → bytes.  
TypeScript: `flowra.files.upload(fileType, body)` (multipart).
