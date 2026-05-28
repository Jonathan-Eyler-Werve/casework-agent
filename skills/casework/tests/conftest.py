import json, pathlib, sys
import pytest

LIB = pathlib.Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(LIB))

@pytest.fixture
def sor(tmp_path, monkeypatch):
    """Temp SoR dir wired via WIKI_PATH; returns the system-of-record path."""
    wiki = tmp_path / "wiki"
    sor = wiki / "system-of-record"
    (sor / "applicants").mkdir(parents=True)
    (sor / "cases").mkdir(parents=True)
    (sor / "notices").mkdir(parents=True)
    monkeypatch.setenv("WIKI_PATH", str(wiki))
    return sor
