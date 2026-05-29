import json, subprocess, sys, pathlib, shutil

SOR_PY = pathlib.Path(__file__).resolve().parents[1] / "sor" / "scripts" / "sor.py"

def _seed(sor):
    (sor / "applicants" / "A-1002.json").write_text(json.dumps({"applicant_id": "A-1002", "name": "Marcus Reyes"}))
    (sor / "cases" / "C-1002.json").write_text(json.dumps({"case_id": "C-1002", "caseworker_id": "CW-7", "status": "recert_due", "recert_due": "2026-06-15", "planned_meeting": {"goal": "recert"}}))

def _run(args, env):
    out = subprocess.run([sys.executable, str(SOR_PY), *args], capture_output=True, text=True, env=env)
    return json.loads(out.stdout)

def test_get_applicant_returns_record(sor, monkeypatch):
    import os
    _seed(sor)
    env = {**os.environ}
    res = _run(["get_applicant", "--applicant-id", "A-1002"], env)
    assert res["status"] == "ok"
    assert res["data"]["name"] == "Marcus Reyes"

def test_get_caseload_lists_planned_meeting(sor):
    import os
    _seed(sor)
    res = _run(["get_caseload", "--caseworker-id", "CW-7"], {**os.environ})
    assert res["status"] == "ok"
    rows = res["data"]["caseload"]
    assert any(r["case_id"] == "C-1002" and "planned_meeting" in r for r in rows)
