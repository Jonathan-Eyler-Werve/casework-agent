#!/usr/bin/env python3
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
import casework_io as cio

def get_applicant(args):
    rec = cio.load_record("applicants", args.applicant_id)
    status = "ok" if rec else "error"
    cio.append_log({"endpoint": "sor", "op": "get_applicant", "applicant_id": args.applicant_id, "status": status})
    return cio.emit(status, rec or {"message": f"applicant {args.applicant_id} not found"})

def get_case(args):
    rec = cio.load_record("cases", args.case_id)
    status = "ok" if rec else "error"
    cio.append_log({"endpoint": "sor", "op": "get_case", "case_id": args.case_id, "status": status})
    return cio.emit(status, rec or {"message": f"case {args.case_id} not found"})

def get_caseload(args):
    cases_dir = cio.sor_dir() / "cases"
    rows = []
    for case_path in sorted(cases_dir.glob("*.json")):
        case = json.loads(case_path.read_text())
        if case.get("caseworker_id") == args.caseworker_id:
            rows.append({k: case.get(k) for k in ("case_id", "status", "recert_due", "planned_meeting")})
    cio.append_log({"endpoint": "sor", "op": "get_caseload", "caseworker_id": args.caseworker_id, "status": "ok", "count": len(rows)})
    return cio.emit("ok", {"caseload": rows})

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="op", required=True)
    cmd = sub.add_parser("get_applicant"); cmd.add_argument("--applicant-id", required=True); cmd.set_defaults(fn=get_applicant)
    cmd = sub.add_parser("get_case"); cmd.add_argument("--case-id", required=True); cmd.set_defaults(fn=get_case)
    cmd = sub.add_parser("get_caseload"); cmd.add_argument("--caseworker-id", required=True); cmd.set_defaults(fn=get_caseload)
    args = parser.parse_args(); args.fn(args)

if __name__ == "__main__":
    main()
