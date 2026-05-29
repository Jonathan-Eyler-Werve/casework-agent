#!/usr/bin/env python3
import argparse, json, pathlib, random, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
import casework_io as cio

STEPS = ["Authenticating to benefits portal",
         "Locating SNAP recertification form",
         "Populating fields from payload",
         "Reviewing for completeness",
         "Submitting"]

def submit(args):
    payload = json.loads(pathlib.Path(args.payload_file).read_text())
    delay = 0 if args.fast else 0.8
    for step in STEPS:
        print(f"[formfiller] {step}…", file=sys.stderr, flush=True)
        time.sleep(delay)
    confirmation_id = "SNAP-REC-" + str(random.randint(1000, 9999))
    submitted_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data = {"confirmation_id": confirmation_id, "submitted_at": submitted_at, "form": args.form, "case_id": args.case_id}
    cio.append_log({"endpoint": "formfiller", "op": "submit", "case_id": args.case_id,
                    "status": "success", "ref": f"confirmation:{confirmation_id}"})
    cio.emit("success", data, log_ref=confirmation_id)
    return data

def main():
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="op", required=True)
    cmd = sub.add_parser("submit")
    cmd.add_argument("--form", required=True); cmd.add_argument("--case-id", required=True)
    cmd.add_argument("--payload-file", required=True); cmd.add_argument("--fast", action="store_true", help="skip simulated delay (tests)")
    cmd.set_defaults(fn=submit)
    args = parser.parse_args(); args.fn(args)

if __name__ == "__main__":
    main()
