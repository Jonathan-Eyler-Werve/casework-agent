import json, os, subprocess, sys, pathlib

VERIFY_PY = pathlib.Path(__file__).resolve().parents[1] / "verify" / "scripts" / "verify.py"

def _seed(sor):
    (sor / "applicants" / "A-1002.json").write_text(json.dumps({
        "applicant_id": "A-1002",
        "work": {"hours_per_week": 18, "abawd_status": "subject"},
        "income": [{"source": "retail", "amount": 1100, "freq": "monthly"}]
    }))

def _run(args):
    out = subprocess.run([sys.executable, str(VERIFY_PY), *args], capture_output=True, text=True, env={**os.environ})
    return json.loads(out.stdout)

def test_work_requirement_flags_gap_below_threshold(sor):
    _seed(sor)
    res = _run(["verify_work_requirement", "--applicant-id", "A-1002"])
    assert res["status"] == "ok"
    d = res["data"]
    assert d["meets_req"] is False
    assert d["hours_counted"] == 18
    assert d["gap"]  # non-empty gap description
