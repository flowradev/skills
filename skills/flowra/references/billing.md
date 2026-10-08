# Credits and usage

Docs and plan limits change. Read the live pricing page / dashboard `usage` payload; do not invent plan prices, quotas, or credit-to-dollar ratios.

Flowra bills in **credits**. Credits spend on model tokens, tool executions, sandbox, browser, media, and workflow overhead. They refresh with the plan. The public site currently lists a free monthly credit grant with no card — confirm the live number on https://flowra.dev before quoting it.

## After a chat turn

SSE `event: usage`:

```json
{
  "runCredits": 142,
  "threadCreditsTotal": 890,
  "balanceRemaining": 48200,
  "executionId": "...",
  "breakdown": { "ai_model": 120, "tool": 22 }
}
```

Breakdown keys you may see: `ai_model`, `tool`, `sandbox`, `browser`, `workflow`, `media`.

## After a workflow run

`FLOWRA_EXECUTE_WORKFLOW` (via MULTI_EXECUTE) returns status / `threadId` / usage when finished. SDK `POST .../workflow/manager/execute/{id}` returns `executionId`; `usage` is null while running.

```ts
const status = await flowra.workflows.status(threadId);
// status.usage.credits when completed
```

## Historical

```ts
const balance = await flowra.usage.balance(); // { balance, currency: 'credits' }
const ledger = await flowra.usage.list({
  threadId,
  from: '2026-08-01T00:00:00.000Z',
});
const run = await flowra.usage.forExecution(executionId);
```

Attribution on rows: `workflowId`, `executionId`, `eUID`, `threadId`.

If balance is too low, stop and tell the user to top up or wait for the monthly refresh. Do not retry failed paid calls in a tight loop.
