---
title: Unresolved security advisories
labels: security-advisory
---

`pip-audit` reports advisories against the pinned dependencies. Renovate only
proposes version bumps on its own schedule, so these need a deliberate bump in
`requirements_prod.txt` or `requirements_dev.txt`.

## Audit output

```text
{{ env.AUDIT_REPORT }}
```
