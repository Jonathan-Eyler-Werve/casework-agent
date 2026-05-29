# Case Overview Agent

A **coordination layer** for benefits caseworkers — one assistant that sits across the tools a caseworker already uses and calls them tool-call style (policy lookup, verification, document requests, form submission, systems of record), instead of shipping yet another point tool. It adapts to local tooling, workflows, and a caseworker's preferences.

**▶ Demo (2 min):** https://p192.p3.n0.cdn.zight.com/items/P8uoBN49/01dd81cd-7021-4744-9d01-6c41c52a652b.mp4?v=35d7dc93082c348630f4ef9f7c7f157f

Take-home prototype for the Code for America Director of Product assessment. Everything here is **synthetic** — no real applicant data, and the integrations are stubbed so the orchestration is what's on display.

## What it does

The caseworker drives it from their normal workplace chat (Signal in the demo) with a small set of command verbs. The demo runs a SNAP recertification under H.R. 1:

`AGENDA` → caseload + today's meetings · `BRIEFING` → brief the case · `INTAKE` → file a meeting transcript and extract structured data · `VERIFY` → work-requirement + income checks · `POLICY` → cited policy answers · `RECORD REQUEST` → request a missing document · `REVIEW` → assemble the recert · `SUBMIT` → file it.

The point is the seams: the agent catches missing/expired data *while the applicant is still in the room*, then hands the assembled recertification to the caseworker for approval before anything is submitted.

## How it's built

The point tools are stubbed behind an imagined API:

- `skills/casework/` — the orchestrator playbook + five endpoint skills (`sor`, `verify`, `notice`, `assist`, `formfiller`), each a small stdlib-only Python CLI sharing `lib/casework_io.py`.
- `system-of-record/` — the stubbed external case system: JSON records + an append-only `activity-log.jsonl`; `API_SPEC.md` documents the imagined API.
- Reads resolve to JSON files; every call appends to the activity log; nothing is destructively overwritten.

## Run the endpoint stubs

The five endpoint scripts are standalone and **stdlib-only Python 3** — call them directly, no install needed:

```bash
WIKI_PATH=$PWD python3 skills/casework/sor/scripts/sor.py get_caseload --caseworker-id CW-7
WIKI_PATH=$PWD python3 skills/casework/verify/scripts/verify.py verify_work_requirement --applicant-id A-1002
WIKI_PATH=$PWD python3 skills/casework/assist/scripts/assist.py ask --question "Which H.R. 1 exemptions apply?"
```

Tests need **pytest**: `cd skills/casework && python3 -m pytest tests/` (8 passing). A full-flow smoke exercises every endpoint end-to-end.

> The scripts above are stdlib-only because they're the stubbed *endpoints* the agent calls. The **full demo** — the agent orchestrating them from chat — runs on the Hermes agent harness (Node-based gateway + signal-cli) on the Pi/Tailscale/Docker setup below; that's the part with real dependencies.

## The demo harness

The live demo runs on deliberately modest, controllable infrastructure — the security/privacy/stability story matters as much as the feature:

- Agent harness on an on-prem **Raspberry Pi 4**, calling Anthropic for inference. Most tasks could run on an open model on agency- or CfA-owned hardware.
- Reachable only over **Tailscale**; runs in a **Docker** container, manageable remotely; data encrypted in transit and at rest; nothing persisted to the cloud.
- UI is whatever workplace chat the caseworker already uses (the gateway supports Signal, Slack, Teams, SMS, email, and others).
- `scripts/` holds idempotent patchers for the two gateway tweaks the demo relies on (a deterministic message header and inbound-attachment path surfacing) plus `reset-demo.sh` to return the demo to a clean state.

---
*Prototype only — stubbed integrations, synthetic data.*
