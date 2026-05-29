import json, os, subprocess, sys, pathlib

ASSIST_PY = pathlib.Path(__file__).resolve().parents[1] / "assist" / "scripts" / "assist.py"

def _run(args):
    out = subprocess.run([sys.executable, str(ASSIST_PY), *args], capture_output=True, text=True, env={**os.environ})
    return json.loads(out.stdout)

def test_ask_exemption_returns_cited_answer(sor):
    res = _run(["ask", "--question", "Which H.R. 1 SNAP work-requirement exemptions apply to a parent of a child?"])
    assert res["status"] == "ok"
    assert "exempt" in res["data"]["answer"].lower()
    assert res["citations"] and res["citations"][0]["source"].endswith("hr1-snap-work-req.md")
