#!/usr/bin/env python3
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
import casework_io as cio

REQUIRED_HOURS = 20  # H.R. 1 ABAWD weekly threshold (synthetic)

def verify_work_requirement(args):
    app = cio.load_record("applicants", args.applicant_id)
    if not app:
        cio.append_log({"endpoint": "verify", "op": "verify_work_requirement", "applicant_id": args.applicant_id, "status": "error"})
        return cio.emit("error", {"message": "applicant not found"})
    hours = app.get("work", {}).get("hours_per_week", 0)
    meets = hours >= REQUIRED_HOURS
    gap = "" if meets else f"Reported {hours}h/wk is below the {REQUIRED_HOURS}h ABAWD threshold and is unverified; needs hours proof or an exemption."
    data = {"meets_req": meets, "hours_counted": hours, "required_hours": REQUIRED_HOURS,
            "exemptions": [], "abawd": app.get("work", {}).get("abawd_status") == "subject", "gap": gap}
    cio.append_log({"endpoint": "verify", "op": "verify_work_requirement", "applicant_id": args.applicant_id, "status": "ok", "meets_req": meets})
    return cio.emit("ok", data)

def verify_income(args):
    app = cio.load_record("applicants", args.applicant_id)
    if not app:
        cio.append_log({"endpoint": "verify", "op": "verify_income", "applicant_id": args.applicant_id, "status": "error"})
        return cio.emit("error", {"message": "applicant not found"})
    data = {"verified": False, "discrepancies": ["proof_of_income on file is expired"], "source": "state wage match (stub)"}
    cio.append_log({"endpoint": "verify", "op": "verify_income", "applicant_id": args.applicant_id, "status": "ok"})
    return cio.emit("ok", data)

def main():
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="op", required=True)
    cmd = sub.add_parser("verify_work_requirement"); cmd.add_argument("--applicant-id", required=True); cmd.set_defaults(fn=verify_work_requirement)
    cmd = sub.add_parser("verify_income"); cmd.add_argument("--applicant-id", required=True); cmd.set_defaults(fn=verify_income)
    args = parser.parse_args(); args.fn(args)

if __name__ == "__main__":
    main()
