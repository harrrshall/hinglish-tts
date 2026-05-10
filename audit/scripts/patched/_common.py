"""Shared monkeypatch: redirect MODELS + OUT before main() runs."""
import sys, os
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = REPO / "audit" / "scripts"
sys.path.insert(0, str(SCRIPTS))  # so 'import lib_audio' etc. work

def install(extract_module, out_filename: str):
    """Patch MODELS and OUT on the imported extract_signals module, then run main()."""
    extract_module.MODELS = ["indicf5_patched"]
    extract_module.OUT = REPO / "audit" / "indicf5_patched" / out_filename
    extract_module.OUT.parent.mkdir(parents=True, exist_ok=True)
    rc = extract_module.main()
    return rc
