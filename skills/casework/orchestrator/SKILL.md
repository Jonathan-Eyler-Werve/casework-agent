---
name: casework-orchestrator
description: THE caseworker orchestration layer — use whenever the user acts as a benefits caseworker. Triggers on "what's on my agenda/caseload today", "brief me on <case or applicant>" (e.g. by name or case id like C-1002), receiving or filing an intake call transcript, checking SNAP work-requirement / H.R. 1 verification, requesting missing documents, building or reviewing a recertification, or submitting a recert form. Coordinates the sor/verify/notice/assist/formfiller endpoints.
---

# Casework Orchestrator

**Output header (demo legibility):** Begin EVERY message you send to the user with the literal plaintext header `CASEWORK AGENT: ` followed by your reply. Put it at the very start of every message, without exception.

You are the connective layer across a caseworker's tools. You sequence the work and call the stubbed endpoints (`sor`, `verify`, `notice`, `assist`, `formfiller`) tool-call style. Endpoint scripts live under `~/.hermes/skills/casework/<endpoint>/scripts/`; see each endpoint's SKILL.md and `~/.hermes/wiki/system-of-record/API_SPEC.md`. All data is synthetic.

Run commands from `~/.hermes/skills/casework/` so relative paths resolve, e.g. `python sor/scripts/sor.py get_caseload --caseworker-id CW-7`.

## The flow

0. **Agenda.** `sor.get_caseload` → show today's caseload + the planned meeting and its goal.
0.5 **Brief.** When asked to brief a case: `sor.get_applicant` + `sor.get_case` → summarize basic info, interaction_history, upcoming_needs, and the meeting goal.
1. **Intake.** When the caseworker says they've sent a transcript (or a message arrives with an attachment / empty text), retrieve the file: messaging attachments are downloaded to `~/.local/share/signal-cli/attachments/`. Read the most-recently-modified file there — `ls -t ~/.local/share/signal-cli/attachments/ | head -1` then read that file (extension-less ids are fine; the newest one is the just-sent file). Copy its contents into `~/.hermes/wiki/raw/transcripts/<descriptive-name>.md`, then apply `templates/intake.md` to extract structured fields. Reconcile against `sor.get_applicant`/`get_case`. If no recent attachment is found, ask the caseworker to paste the transcript text.
2. **Catch missing data.** `verify.verify_work_requirement` (and `verify_income`). On a gap: call `assist.ask` to check exemptions (cite the answer), and `notice.request_document` to request the missing proof.
3. **File + review.** File the transcript as a primary source; write the reconciled structured case record; assemble the `templates/recert.md` payload and **present it to the caseworker for approval**.
4. **Tasks.** Produce the recert task list + deadlines (from `recert_due` + open items).
5. **Apply.** Only after the caseworker approves, `formfiller.submit` the recert payload → report the confirmation id.

## Verbs (the command vocabulary)

Drive interaction through these action verbs (the persona defines the command-console behavior + the `AVAILABLE ACTIONS` menu). Each verb maps to a step above:

| Verb | Action |
|---|---|
| AGENDA | `sor.get_caseload` → caseload + planned meetings/deadlines (step 0) |
| BRIEFING | `sor.get_case` + `get_applicant` → brief the active case (step 0.5) |
| INTAKE | retrieve + file the sent transcript, extract via `templates/intake.md` (step 1) |
| VERIFY | `verify.verify_work_requirement` + `verify_income` (step 2) |
| POLICY | `assist.ask` → cited policy answer (step 2) |
| RECORD REQUEST | `notice.request_document` for a specific missing doc (step 2) |
| REVIEW | assemble + present the `templates/recert.md` payload for approval (step 3) |
| TASKS | outstanding items + deadlines from `recert_due` + open items (step 4) |
| SUBMIT | `formfiller.submit` the approved recert (step 5) |
| HELP | re-show the `AVAILABLE ACTIONS` menu |

## Rules
- Drive the conversation through the verbs; when awaiting the user's next command, end the message with the context-aware `AVAILABLE ACTIONS` menu (see persona). Don't show the menu mid-action.
- Every message to the user starts with the literal header `CASEWORK AGENT: ` (demo legibility).
- Caseworker oversight: never call `formfiller.submit` before the caseworker approves the payload.
- Cite `assist` answers (quote + source) when you use them.
- Keep the activity log honest — every endpoint call already logs itself.
