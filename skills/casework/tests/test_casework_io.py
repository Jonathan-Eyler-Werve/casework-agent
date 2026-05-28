import json, casework_io as cio

def test_append_log_writes_one_line_with_ts(sor):
    cio.append_log({"endpoint": "sor", "op": "get_case", "status": "ok"})
    lines = (sor / "activity-log.jsonl").read_text().strip().splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["endpoint"] == "sor" and entry["status"] == "ok"
    assert "ts" in entry

def test_load_record_returns_none_when_missing(sor):
    assert cio.load_record("applicants", "NOPE") is None
