#!/usr/bin/env python3
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
import casework_io as cio

SRC = "assist/sources/hr1-snap-work-req.md"

# Canned, citation-backed answers keyed by topic (deterministic for the demo).
KB = [
    {"keywords": ["exempt", "exemption", "exemptions", "child", "children", "dependent", "dependents",
                  "work", "requirement", "requirements", "abawd", "able-bodied", "hours", "snap",
                  "recert", "recertification", "eligible", "eligibility", "qualify", "qualifies",
                  "caretaker", "caring", "care", "waive", "waiver", "comply", "compliance",
                  "h.r. 1", "hr1", "deadline", "benefit", "verify", "verification", "income"],
     "answer": ("A SNAP applicant is exempt from the H.R. 1 ABAWD work requirement if they are responsible "
                "for a dependent child under 18 in the household. Caring for an incapacitated household member, "
                "or being unable to work, also qualifies. Unverified hours don't count — request documentation "
                "before any adverse action."),
     "citations": [
         {"quote": "An individual is exempt from the SNAP work requirement if they are responsible for a dependent child under age 18 in their household.", "source": SRC},
         {"quote": "Hours that cannot be verified do not count toward the requirement; the agency should request documentation before any adverse action.", "source": SRC},
     ]},
]

def ask(args):
    question = args.question.lower()
    best = max(KB, key=lambda entry: sum(k in question for k in entry["keywords"]))
    if sum(k in question for k in best["keywords"]) == 0:
        cio.append_log({"endpoint": "assist", "op": "ask", "status": "ok", "matched": False})
        return cio.emit("ok", {"answer": "I don't have a vetted source for that question.", "confidence": "low"}, citations=[])
    cio.append_log({"endpoint": "assist", "op": "ask", "status": "ok", "matched": True})
    return cio.emit("ok", {"answer": best["answer"], "confidence": "high"}, citations=best["citations"])

def main():
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="op", required=True)
    cmd = sub.add_parser("ask"); cmd.add_argument("--question", required=True); cmd.set_defaults(fn=ask)
    args = parser.parse_args(); args.fn(args)

if __name__ == "__main__":
    main()
