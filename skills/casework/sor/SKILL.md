---
name: casework-sor
description: Stubbed case/eligibility system of record. Use to look up a case, an applicant, or a caseworker's caseload during casework orchestration.
---

# System of Record (stub)

Read-only lookups against the case system of record. Call via:

- `python sor/scripts/sor.py get_applicant --applicant-id A-1002`
- `python sor/scripts/sor.py get_case --case-id C-1002`
- `python sor/scripts/sor.py get_caseload --caseworker-id CW-7`  → today's caseload + planned meetings

Returns the JSON envelope `{status,data}`. Every call is logged to the activity log. Records live under `~/.hermes/wiki/system-of-record/`.
