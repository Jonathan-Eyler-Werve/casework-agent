---
name: casework-assist
description: Stubbed RAG policy assistant (NAVA assistive-chatbot pattern). Use to answer benefits-policy questions with direct-quote citations from vetted sources.
---

# Policy Assistant (stub)

- `python assist/scripts/assist.py ask --question "Which H.R. 1 SNAP work-requirement exemptions apply?"`

Returns `{answer, confidence}` plus `citations:[{quote, source}]` pointing into `assist/sources/`. Sticks to vetted sources; says so when it has none.
