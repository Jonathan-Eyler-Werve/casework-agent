---
name: casework-formfiller
description: Stubbed agentic form-filling submission (NAVA form-filling pattern). Use ONLY after the caseworker approves the assembled payload, to submit a recertification.
---

# Form-Filling Agent (stub)

- `python formfiller/scripts/formfiller.py submit --form snap_recert --case-id C-1002 --payload-file <path-to-payload.json>`

Simulates agentic portal work (progress lines to stderr, a few seconds) and returns `{status:"success", confirmation_id, submitted_at}`. **Caseworker oversight:** confirm the payload with the user before calling this. Logs the submission to the activity log.
