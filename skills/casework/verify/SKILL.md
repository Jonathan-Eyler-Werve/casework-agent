---
name: casework-verify
description: Stubbed income / work-requirement verification service. Use to check whether an applicant meets H.R. 1 SNAP work requirements or has income discrepancies.
---

# Verification (stub)

- `python verify/scripts/verify.py verify_work_requirement --applicant-id A-1002`
- `python verify/scripts/verify.py verify_income --applicant-id A-1002`

`verify_work_requirement` returns `{meets_req, hours_counted, required_hours, exemptions, abawd, gap}`. A non-empty `gap` means follow up — request a document (notice) and/or check exemptions (assist).
