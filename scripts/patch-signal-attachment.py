#!/usr/bin/env python3
"""Patch the Hermes Signal gateway to surface inbound attachment file paths in
the message text the agent receives.

The gateway downloads attachments to ~/.local/share/signal-cli/attachments/ and
passes them as `media_urls`, but non-image documents (e.g. a .md transcript)
aren't rendered into the model's view — so the agent can't tell a file arrived
or where it is. This appends a `[Attachment saved locally: <path>]` marker to the
inbound text, giving the agent the exact path to read. Deterministic; no `ls`
guessing.

Usage:
  python3 patch-signal-attachment.py [path-to-signal.py]   # apply (idempotent)
  python3 patch-signal-attachment.py --revert [path]        # remove

Default path: ~/.hermes/hermes-agent/gateway/platforms/signal.py
NOTE: edits the Hermes install — re-run after a `hermes update`. Requires a
gateway restart to take effect.
"""
import pathlib
import sys

DEFAULT = pathlib.Path.home() / ".hermes/hermes-agent/gateway/platforms/signal.py"
MARK = "[casework-demo attachment patch]"

ANCHOR = "        # Skip envelopes with no meaningful content (no text, no attachments).\n"
INJECT = (
    "        # " + MARK + " surface attachment local path(s) in the message text\n"
    "        if media_urls:\n"
    '            _att_note = "[Attachment saved locally: " + ", ".join(media_urls) + "]"\n'
    "            text = (text + \"\\n\\n\" + _att_note) if (text and text.strip()) else _att_note\n"
    "\n"
    + ANCHOR
)


def main() -> None:
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    positional = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = pathlib.Path(positional[0]) if positional else DEFAULT
    source = path.read_text(encoding="utf-8")

    if "--revert" in flags:
        if MARK not in source:
            print("Patch not present; nothing to revert.")
            return
        path.write_text(source.replace(INJECT, ANCHOR), encoding="utf-8")
        print(f"Reverted attachment patch in {path}")
        return

    if MARK in source:
        print("Attachment patch already applied; no change.")
        return
    if ANCHOR not in source:
        print("ERROR: anchor not found — signal.py may have changed. Aborting.", file=sys.stderr)
        sys.exit(1)
    path.write_text(source.replace(ANCHOR, INJECT, 1), encoding="utf-8")
    print(f"Applied attachment-path patch to {path}")


if __name__ == "__main__":
    main()
