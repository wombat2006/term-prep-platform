# Service Contract Canon (Plan B)

Status:
Draft v1 (2026-06-29) — contract-first baseline before remote service implementation.

> **Consumer entry point:** [`meta/CONSUMER_HANDOFF.md`](../CONSUMER_HANDOFF.md)  
> This directory contains the **Plan B (remote service) contract** only.
> The current production path is the **1.x package CLI contract** — see quickstart below.

---

## Purpose

This directory is the canonical contract for the future **Plan B** runtime boundary
(Remote MCP / HTTP service).

It defines:

1. Domain and error models
2. Surface contracts (HTTP, SSE, MCP, CLI)
3. Versioning and compatibility rules
4. Connector SPI requirements to lower implementation cost for new adapters
5. LLM provider policy — consumer isolation from Anthropic/Google/Ollama changes

Implementation can change, but this contract must remain stable within major version.

---

## Current production quickstart (1.x package contract)

> **This quickstart is for the current `1.x` package CLI contract.**
> No remote service migration is needed at this stage.
> Plan B remote service specs are in the files listed in the Read order below.

```bash
# 1. Install the platform package (use your private index or local editable install)
pip install term-prep-platform==1.0.0

# 2. Copy and adapt the config template
cp /path/to/term-prep-platform/meta/glossary-pipeline/glossary-config.template.json \
   meta/glossary-config.json
# edit meta/glossary-config.json: set project_root, corpus.files, scoring, output

# 3. Verify config + morphology
term-prep-contract-check --config meta/glossary-config.json --expect-major 1
term-prep-extract --check --config meta/glossary-config.json

# 4. Run extraction
term-prep-extract --config meta/glossary-config.json
# outputs: meta/glossary-adopt.json, meta/glossary-hold.json

# 5. Wire npm scripts (optional convenience)
```

```json
{
  "scripts": {
    "glossary:extract:check": "term-prep-extract --check --config meta/glossary-config.json",
    "glossary:extract": "term-prep-extract --config meta/glossary-config.json",
    "glossary:sync:check": "term-prep-sync --check --config meta/glossary-config.json",
    "glossary:sync": "term-prep-sync --config meta/glossary-config.json"
  }
}
```

For CI: copy [`meta/consumer-handoff/templates/consumer-contract-ci.yml`](../consumer-handoff/templates/consumer-contract-ci.yml)
into your `.github/workflows/` and adapt the `pip install` step.

For a detailed migration guide: [`meta/consumer-handoff/04-consumer-pr-guide-techdev-cursor.md`](../consumer-handoff/04-consumer-pr-guide-techdev-cursor.md)

For a per-consumer checklist template: [`meta/consumer-handoff/consumers/_TEMPLATE.md`](../consumer-handoff/consumers/_TEMPLATE.md)

---

## Read order

1. [domain-model.md](./domain-model.md)
2. [versioning-policy.md](./versioning-policy.md)
3. [http/openapi.yaml](./http/openapi.yaml)
4. [sse/event-envelope.schema.json](./sse/event-envelope.schema.json)
5. [mcp-tool-contract.md](./mcp-tool-contract.md)
6. [cli-contract.md](./cli-contract.md)
7. [connector-spi.md](./connector-spi.md)
8. [llm-provider-policy.md](./llm-provider-policy.md)

---

## Contract scope

This canon covers:

- request/response payload structure
- async job lifecycle and event stream
- error envelope and retry semantics
- compatibility gates for consumers

This canon does not cover:

- deployment topology
- vendor-specific connector internals
- provider-specific ranking heuristics

---

## Governance

- Source of truth: this directory + decision logs in `meta/glossary-pipeline/DECISIONS.md`
- Breaking changes require:
  1. Semver major increment
  2. consumer-handoff changelog update
  3. compatibility matrix update in consumer CI guidance
