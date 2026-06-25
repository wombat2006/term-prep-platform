# Custom subagents (multi-model opinions)

Read-only opinion subagents for parallel second-opinion workflows on **term-prep-platform** work (glossary prep, connectors, MCP, consumer handoff).

| Subagent | Model | Invoke |
|----------|-------|--------|
| `gpt-opinion` | GPT-5.5 | `/gpt-opinion <question>` |
| `codex-opinion` | Codex 5.3 | `/codex-opinion <question>` |
| `gemini-opinion` | Gemini 3.1 Pro | `/gemini-opinion <question>` |

## Parallel comparison (example)

```text
Run /gpt-opinion, /codex-opinion, and /gemini-opinion in parallel on this design question:

Should Phase 0.5 Drive mirror stay TypeScript subprocess vs pure Python connector?

Context: meta/consumer-handoff/05-platform-implementation.md · connectors/googledrive/

Then compare the three opinions in a table: agreements, disagreements, and a merged recommendation.
```

## Platform-specific uses

| Topic | Suggested subagent |
|-------|-------------------|
| Schema / consumer contract | `gpt-opinion` |
| Connector implementation | `codex-opinion` |
| Genspark / aidrive boundary · scope | `gemini-opinion` |
| Cross-repo handoff workflow | `gpt-opinion` + `gemini-opinion` |

## Requirements

- Enable **GPT-5.5**, **Codex 5.3**, and **Gemini 3.1 Pro** in Cursor **Settings → Models**.
- All three agents use `readonly: true` — opinions only, no file edits.

## Related

- Consumer boundary (read-only): sibling `../techdev-cursor/meta/platform-integration/`
- Platform → consumer handoff: `meta/consumer-handoff/` · skill `consumer-handoff`
