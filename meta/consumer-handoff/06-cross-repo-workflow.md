# Cross-repo workflow (legacy A + C bot)

Status:
deprecated (2026-06-29)

---

## Context

The previous A+C hybrid flow (platform bot issue + consumer PR) depended on:

- sibling path assumptions
- cross-repo issue bot secrets
- mirror config in platform repo

Decision [D-004](../glossary-pipeline/DECISIONS.md#d-004) replaced this with a
package/Semver contract model.

---

## Replacement workflow

1. platform publishes package release (`X.Y.Z`)
2. consumer updates package pin in its own PR
3. consumer runs contract check in CI
4. release notes replace issue-bot handoff

---

## Legacy assets removed

- `scripts/cross_repo/*`
- `.github/workflows/consumer-handoff-notify.yml`
- consumer `scripts/platform-handoff/*` template flow

---

## Related

- [README.md](./README.md)
- [02-schema-and-cli.md](./02-schema-and-cli.md)
- [04-consumer-pr-guide-techdev-cursor.md](./04-consumer-pr-guide-techdev-cursor.md)
