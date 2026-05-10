import _common, sys
sys.path.insert(0, str(_common.SCRIPTS))
import extract_signals
sys.exit(_common.install(extract_signals, "signal_vectors_aai.json"))
