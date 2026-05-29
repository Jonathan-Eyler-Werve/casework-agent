#!/usr/bin/env python3
"""Patch the Hermes Signal gateway to prepend a deterministic
`CASEWORK AGENT: ` header to every outbound message (demo legibility).

A prompt instruction (in SOUL.md / the orchestrator skill) is non-deterministic
— the model drops the header when other instructions compete. This injects it in
code, in the single Signal send path, so it appears on every outbound message.

Usage:
  python3 patch-signal-header.py [path-to-signal.py]   # apply (idempotent)
  python3 patch-signal-header.py --revert [path]        # remove

Default path: ~/.hermes/hermes-agent/gateway/platforms/signal.py
NOTE: edits the Hermes install — re-run after a `hermes update`. Requires a
gateway restart to take effect. Reverting restores the original send().
"""
import pathlib
import sys

DEFAULT = pathlib.Path.home() / ".hermes/hermes-agent/gateway/platforms/signal.py"
MARK = "[casework-demo patch]"

ANCHOR = (
    '        """Send a text message with native Signal formatting."""\n'
    "        await self._stop_typing_indicator(chat_id)\n"
)
INJECT = (
    ANCHOR
    + "\n"
    + "        # " + MARK + " deterministic CASEWORK AGENT: header on every outbound message\n"
    + '        if content and not content.lstrip().startswith("CASEWORK AGENT:"):\n'
    + '            content = "CASEWORK AGENT: " + content\n'
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
        print(f"Reverted header patch in {path}")
        return

    if MARK in source:
        print("Header patch already applied; no change.")
        return
    if ANCHOR not in source:
        print("ERROR: anchor not found — signal.py send() may have changed. Aborting.", file=sys.stderr)
        sys.exit(1)
    path.write_text(source.replace(ANCHOR, INJECT, 1), encoding="utf-8")
    print(f"Applied CASEWORK AGENT header patch to {path}")


if __name__ == "__main__":
    main()
