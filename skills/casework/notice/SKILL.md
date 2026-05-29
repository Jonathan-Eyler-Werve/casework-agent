---
name: casework-notice
description: Stubbed document/notice service. Use to request a missing document from an applicant or queue a notice on a case.
---

# Notice / Document Request (stub)

- `python notice/scripts/notice.py request_document --case-id C-1002 --doc-type proof_of_work_hours --reason "verify H.R. 1 hours"`

Creates a notice record under `system-of-record/notices/` and returns `{notice_id, sent_to, status:"queued"}`.
