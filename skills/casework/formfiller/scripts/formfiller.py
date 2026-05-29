#!/usr/bin/env python3
import argparse, json, pathlib, random, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
import casework_io as cio

STEPS = ["Authenticating to benefits portal",
         "Locating SNAP recertification form",
         "Populating fields from payload",
         "Reviewing for completeness",
         "Submitting"]

def submit(a):
    payload = json.loads(pathlib.Path(a.payload_file).read_text())
    delay = 0 if a.fast else 0.8
    for step in STEPS:
        print(f"[formfiller] {step}…", file=sys.stderr, flush=True)
        time.sleep(delay)
    confirmation_id = "SNAP-REC-" + str(random.randint(1000, 9999))
    submitted_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data = {"confirmation_id": confirmation_id, "submitted_at": submitted_at, "form": a.form, "case_id": a.case_id}
    cio.append_log({"endpoint": "formfiller", "op": "submit", "case_id": a.case_id,
                    "status": "success", "ref": f"confirmation:{confirmation_id}"})
    print(json.dumps({"status": "success", "data": data, "log_ref": confirmation_id}, indent=2))
    return data

def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="op", required=True)
    s = sub.add_parser("submit")
    s.add_argument("--form", required=True); s.add_argument("--case-id", required=True)
    s.add_argument("--payload-file", required=True); s.add_argument("--fast", action="store_true", help="skip simulated delay (tests)")
    s.set_defaults(fn=submit)
    a = p.parse_args(); a.fn(a)

if __name__ == "__main__":
    main()
