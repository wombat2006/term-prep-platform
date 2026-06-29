# Versioning And Compatibility Policy

Status:
Draft v1 (2026-06-29)

---

## Contract version source

Contract version is the package version in `pyproject.toml` (`term-prep-platform`).

Semver policy:

- `MAJOR`: breaking contract changes
- `MINOR`: backward-compatible features
- `PATCH`: bug fixes and clarifications without surface changes

---

## What counts as breaking

Any of the following requires a major increment:

1. Removing or renaming a field in canonical models
2. Changing type/enum semantics of existing fields
3. Changing command behavior or exit-code semantics in CLI contract
4. Renaming/removing HTTP endpoint, SSE event, or MCP tool
5. Tightening validation in a way that rejects previously valid consumer configs

---

## Deprecation window

Default:

- At least one `MINOR` release with deprecation notice before removal
- Deprecations must be documented in `meta/consumer-handoff/CHANGELOG.md`
- Consumers must receive migration guidance before next major cut

---

## Compatibility matrix baseline

For each release, maintain this matrix:

| Platform major | Consumer expectation | Status |
|---|---|---|
| 1.x | `term-prep-contract-check --expect-major 1` | supported |
| 2.x | `term-prep-contract-check --expect-major 2` | future |

---

## CI gate (minimum)

Consumer CI must run:

```bash
term-prep-contract-check --config meta/glossary-config.json --expect-major 1
term-prep-extract --check --config meta/glossary-config.json
```

Contract changes are not complete until CI guidance and changelog are updated.

---

## Retry policy (consumer-side guidance)

When the platform returns `ErrorEnvelope` with `retryable: true`, consumers
should apply the following strategy. This is a recommendation, not a contract
requirement enforced by the platform.

| Retry | Wait before retry |
|---|---|
| 1st | 1 second |
| 2nd | 2 seconds |
| 3rd | 4 seconds |
| After 3rd | Treat as failed, do not retry |

Additional rules:

- Apply exponential backoff: wait = `2^(n-1)` seconds for retry `n`
- For HTTP `429` (Too Many Requests) or `503` (Service Unavailable): honour
  the `Retry-After` header value if present, ignoring the table above
- `retryable: false` — do **not** retry; the error is deterministic

If `retryable` is absent (e.g. network-level failure before reaching the
service), treat the request as potentially retryable with the same table.

---

## Error code stability

`error.code` values are stable across all patch and minor versions within a
major. Consumers may build switch/case logic on error codes without risk of
breakage within `1.x`. `error.message` is for humans only and may change in
any release.
