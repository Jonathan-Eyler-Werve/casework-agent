#!/usr/bin/env bash
# reset-demo.sh — reset the casework demo on the Hermes host to a clean state.
#
# Each demo run leaves artifacts that pollute the next run's orientation:
# the agent files the transcript + a case briefing into the wiki, appends a
# "recert submitted" entry to wiki/log.md, and the Signal session retains the
# conversation. This script clears all of that so the next run starts fresh.
#
# Run ON the Hermes host, e.g.:  bash ~/.hermes/reset-demo.sh
# Or from a workstation:         ssh home-box 'bash ~/.hermes/reset-demo.sh'
#
# Session handling is OPT-IN and explicit: pass the demo session id to clear its
# chat history (reset-demo.sh <session-id>). With no arg the script ONLY cleans
# the wiki + SoR state (always safe) and lists recent Signal sessions for you to
# pick from — it never guesses which session to delete.

set -euo pipefail

WIKI="${WIKI_PATH:-$HOME/.hermes/wiki}"
SOR="$WIKI/system-of-record"
HERMES="$HOME/.local/bin/hermes"

# 1. Restore pristine wiki log + index (strip the agent's run entries).
cat > "$WIKI/log.md" <<'EOF'
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-05-28] create | Wiki initialized
- Domain: generic / placeholder (not yet specialized — see SCHEMA.md TODO)
- Structure created with PATTERN.md (verbatim llm-wiki skill), SCHEMA.md, index.md, log.md, and raw/entities/concepts/comparisons/queries dirs
- Wired as a startup orientation target via SOUL.md
EOF

cat > "$WIKI/index.md" <<'EOF'
# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-05-28 | Total pages: 0

## Entities
<!-- Alphabetical within section -->

## Concepts

## Comparisons

## Queries
EOF

# 2. Clear agent-written pages/transcripts (keep the dir tree + .gitkeep files).
for d in raw/articles raw/papers raw/transcripts raw/assets raw/cases entities concepts comparisons queries; do
  [ -d "$WIKI/$d" ] && find "$WIKI/$d" -type f ! -name '.gitkeep' -delete
done

# 3. Reset the system-of-record volatile state.
: > "$SOR/activity-log.jsonl"
rm -f "$SOR"/notices/N-*.json

echo "Wiki + SoR reset: log/index pristine, raw/case artifacts cleared, activity log + notices empty."

# 4. Clear the demo conversation — only when an explicit session id is given.
#    SAFETY: never auto-deletes. "Most recent Signal session" could be a real
#    conversation, so the caller must name the session to drop.
if [ -n "${1:-}" ]; then
  "$HERMES" sessions delete --yes "$1" 2>&1 | tail -1
  echo "Deleted demo session $1."
else
  echo
  echo "To also clear the demo conversation, re-run with the demo session id:"
  echo "  bash ~/.hermes/reset-demo.sh <session-id>"
  echo "Recent Signal sessions (pick the demo one):"
  "$HERMES" sessions list --source signal --limit 5 2>/dev/null || true
fi
