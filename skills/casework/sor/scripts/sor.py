#!/usr/bin/env python3
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
import casework_io as cio

def get_applicant(a):
    rec = cio.load_record("applicants", a.applicant_id)
    status = "ok" if rec else "error"
    cio.append_log({"endpoint": "sor", "op": "get_applicant", "applicant_id": a.applicant_id, "status": status})
    return cio.emit(status, rec or {"message": f"applicant {a.applicant_id} not found"})

def get_case(a):
    rec = cio.load_record("cases", a.case_id)
    status = "ok" if rec else "error"
    cio.append_log({"endpoint": "sor", "op": "get_case", "case_id": a.case_id, "status": status})
    return cio.emit(status, rec or {"message": f"case {a.case_id} not found"})

def get_caseload(a):
    cases_dir = cio.sor_dir() / "cases"
    rows = []
    for p in sorted(cases_dir.glob("*.json")):
        c = json.loads(p.read_text())
        if c.get("caseworker_id") == a.caseworker_id:
            rows.append({k: c.get(k) for k in ("case_id", "status", "recert_due", "planned_meeting")})
    cio.append_log({"endpoint": "sor", "op": "get_caseload", "caseworker_id": a.caseworker_id, "status": "ok", "count": len(rows)})
    return cio.emit("ok", {"caseload": rows})

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="op", required=True)
    s = sub.add_parser("get_applicant"); s.add_argument("--applicant-id", required=True); s.set_defaults(fn=get_applicant)
    s = sub.add_parser("get_case"); s.add_argument("--case-id", required=True); s.set_defaults(fn=get_case)
    s = sub.add_parser("get_caseload"); s.add_argument("--caseworker-id", required=True); s.set_defaults(fn=get_caseload)
    a = p.parse_args(); a.fn(a)

if __name__ == "__main__":
    main()
