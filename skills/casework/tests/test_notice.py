import json, os, subprocess, sys, pathlib

NOTICE_PY = pathlib.Path(__file__).resolve().parents[1] / "notice" / "scripts" / "notice.py"

def _run(args):
    out = subprocess.run([sys.executable, str(NOTICE_PY), *args], capture_output=True, text=True, env={**os.environ})
    return json.loads(out.stdout)

def test_request_document_creates_notice_record(sor):
    res = _run(["request_document", "--case-id", "C-1002", "--doc-type", "proof_of_work_hours", "--reason", "verify hours"])
    assert res["status"] == "ok"
    nid = res["data"]["notice_id"]
    assert (sor / "notices" / f"{nid}.json").exists()
    assert res["data"]["status"] == "queued"
