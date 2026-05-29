import json, os, subprocess, sys, pathlib

FF_PY = pathlib.Path(__file__).resolve().parents[1] / "formfiller" / "scripts" / "formfiller.py"

def test_submit_returns_success_with_confirmation(sor, tmp_path):
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps({"applicant_id": "A-1002", "household_size": 2, "monthly_income": 1100}))
    out = subprocess.run(
        [sys.executable, str(FF_PY), "submit", "--form", "snap_recert", "--case-id", "C-1002",
         "--payload-file", str(payload), "--fast"],
        capture_output=True, text=True, env={**os.environ})
    res = json.loads(out.stdout)
    assert res["status"] == "success"
    assert res["data"]["confirmation_id"].startswith("SNAP-REC-")
    assert "submitting" in out.stderr.lower()
