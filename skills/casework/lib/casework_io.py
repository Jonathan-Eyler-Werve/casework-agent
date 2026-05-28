import json, os, pathlib, time

def sor_dir() -> pathlib.Path:
    base = os.environ.get("WIKI_PATH") or os.path.expanduser("~/.hermes/wiki")
    return pathlib.Path(base) / "system-of-record"

def load_record(kind: str, rid: str):
    p = sor_dir() / kind / f"{rid}.json"
    return json.loads(p.read_text()) if p.exists() else None

def append_log(entry: dict) -> dict:
    log = sor_dir() / "activity-log.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **entry}
    with log.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

def emit(status: str, data=None, citations=None, log_ref=None) -> dict:
    out = {"status": status, "data": data if data is not None else {}}
    if citations is not None:
        out["citations"] = citations
    if log_ref is not None:
        out["log_ref"] = log_ref
    print(json.dumps(out, indent=2))
    return out
