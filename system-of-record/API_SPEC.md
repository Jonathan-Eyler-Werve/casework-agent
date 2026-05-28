# System of Record — imagined API (stub)

This directory stubs an external case/eligibility system + point-tool endpoints. Reads resolve to JSON files here; writes append to `activity-log.jsonl` and create records under `notices/`. Each endpoint is a CLI under `~/.hermes/skills/casework/<endpoint>/scripts/`.

**Response envelope (stdout):** `{"status":"ok"|"error","data":{...},"citations"?:[...],"log_ref"?:"..."}`
**Activity log line:** `{"ts","endpoint","op","status",...context}` appended to `activity-log.jsonl`.

## sor — system of record
- `get_case --case-id C-1002` → case record
- `get_applicant --applicant-id A-1002` → applicant record
- `get_caseload --caseworker-id CW-7` → `[{case_id,status,recert_due,planned_meeting}]`

## verify — income / work-requirement verification
- `verify_income --applicant-id A-1002` → `{verified,discrepancies[],source}`
- `verify_work_requirement --applicant-id A-1002` → `{meets_req,hours_counted,required_hours,exemptions[],abawd,gap}`

## notice — document / notice service
- `request_document --case-id C-1002 --doc-type proof_of_work_hours --reason "..."` → `{notice_id,sent_to,status}`

## assist — RAG policy assistant (cited answers; NAVA assistive-chatbot pattern)
- `ask --question "..."` → `{answer,confidence}` + `citations:[{quote,source}]`

## formfiller — agentic form submission (NAVA form-filling pattern)
- `submit --form snap_recert --case-id C-1002 --payload-file <path>` → simulated work → `{status:"success",confirmation_id,submitted_at}`

## Record schemas
See `applicants/*.json` and `cases/*.json` for the canonical shapes (household, income, work, interaction_history, upcoming_needs, planned_meeting, recert_due, documents, flags).
