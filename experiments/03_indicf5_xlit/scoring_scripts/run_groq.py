import _common, sys
sys.path.insert(0, str(_common.SCRIPTS))
import extract_signals_groq
sys.exit(_common.install(extract_signals_groq, "signal_vectors_groq.json"))
