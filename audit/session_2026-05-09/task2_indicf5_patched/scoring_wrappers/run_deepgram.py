import _common, sys
sys.path.insert(0, str(_common.SCRIPTS))
import extract_signals_deepgram
sys.exit(_common.install(extract_signals_deepgram, "signal_vectors_deepgram.json"))
