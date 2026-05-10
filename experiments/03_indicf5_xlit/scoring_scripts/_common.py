"""Shared monkeypatch for indicf5_patched_xlit: redirect MODELS + OUT before main()."""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = REPO / "audit" / "scripts"
sys.path.insert(0, str(SCRIPTS))


def install(extract_module, out_filename: str):
    extract_module.MODELS = ["indicf5_patched_xlit"]
    extract_module.OUT = REPO / "audit" / "indicf5_patched_xlit" / out_filename
    extract_module.OUT.parent.mkdir(parents=True, exist_ok=True)
    return extract_module.main()
