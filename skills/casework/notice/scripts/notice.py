#!/usr/bin/env python3
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "lib"))
import casework_io as cio

def request_document(args):
    notice_id = "N-" + time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    record = {"notice_id": notice_id, "case_id": args.case_id, "doc_type": args.doc_type,
              "reason": args.reason, "sent_to": "applicant", "status": "queued"}
    out_dir = cio.sor_dir() / "notices"; out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{notice_id}.json").write_text(json.dumps(record, indent=2))
    cio.append_log({"endpoint": "notice", "op": "request_document", "case_id": args.case_id,
                    "doc_type": args.doc_type, "status": "ok", "ref": notice_id})
    return cio.emit("ok", record, log_ref=notice_id)

def main():
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="op", required=True)
    cmd = sub.add_parser("request_document")
    cmd.add_argument("--case-id", required=True); cmd.add_argument("--doc-type", required=True); cmd.add_argument("--reason", required=True)
    cmd.set_defaults(fn=request_document)
    args = parser.parse_args(); args.fn(args)

if __name__ == "__main__":
    main()
