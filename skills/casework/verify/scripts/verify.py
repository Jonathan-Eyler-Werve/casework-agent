#!/usr/bin/env python3
import argparse, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
import casework_io as cio

REQUIRED_HOURS = 20  # H.R. 1 ABAWD weekly threshold (synthetic)

def verify_work_requirement(a):
    app = cio.load_record("applicants", a.applicant_id)
    if not app:
        cio.append_log({"endpoint": "verify", "op": "verify_work_requirement", "applicant_id": a.applicant_id, "status": "error"})
        return cio.emit("error", {"message": "applicant not found"})
    hours = app.get("work", {}).get("hours_per_week", 0)
    meets = hours >= REQUIRED_HOURS
    gap = "" if meets else f"Reported {hours}h/wk is below the {REQUIRED_HOURS}h ABAWD threshold and is unverified; needs hours proof or an exemption."
    data = {"meets_req": meets, "hours_counted": hours, "required_hours": REQUIRED_HOURS,
            "exemptions": [], "abawd": app.get("work", {}).get("abawd_status") == "subject", "gap": gap}
    cio.append_log({"endpoint": "verify", "op": "verify_work_requirement", "applicant_id": a.applicant_id, "status": "ok", "meets_req": meets})
    return cio.emit("ok", data)

def verify_income(a):
    app = cio.load_record("applicants", a.applicant_id)
    if not app:
        cio.append_log({"endpoint": "verify", "op": "verify_income", "applicant_id": a.applicant_id, "status": "error"})
        return cio.emit("error", {"message": "applicant not found"})
    data = {"verified": False, "discrepancies": ["proof_of_income on file is expired"], "source": "state wage match (stub)"}
    cio.append_log({"endpoint": "verify", "op": "verify_income", "applicant_id": a.applicant_id, "status": "ok"})
    return cio.emit("ok", data)

def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="op", required=True)
    s = sub.add_parser("verify_work_requirement"); s.add_argument("--applicant-id", required=True); s.set_defaults(fn=verify_work_requirement)
    s = sub.add_parser("verify_income"); s.add_argument("--applicant-id", required=True); s.set_defaults(fn=verify_income)
    a = p.parse_args(); a.fn(a)

if __name__ == "__main__":
    main()
