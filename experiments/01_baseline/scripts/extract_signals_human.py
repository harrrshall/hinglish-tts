"""Stage 1 (human ground truth): per-clip signal vectors for the 8 human wavs.

Same schema as audit/signal_vectors*.json so the existing judge.py family can
ingest the output as-is. Runs DSP + MOS once, then all three ASR backends
(AssemblyAI, Deepgram, Groq) so we get one signal_vectors_<backend>.json per
ASR. The model tag in each entry is "human_groundtruth".

Reads:
  audit/human_groundtruth/wavs/human_NN.wav  (8 files)
  audit/human_groundtruth/wav_to_sentence.csv
  .env  (ASSEMBLYAI_API_KEY, DEEPGRAM_API_KEY, GROQ_API_KEY)

Writes:
  audit/human_groundtruth/signal_vectors_aai.json
  audit/human_groundtruth/signal_vectors_deepgram.json
  audit/human_groundtruth/signal_vectors_groq.json

Note: keys are loaded from .env into os.environ before importing the lib_asr_*
modules, since those modules read the env at first call.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
GT_DIR = REPO / "audit" / "human_groundtruth"
WAVS_DIR = GT_DIR / "wavs"
MAPPING_CSV = GT_DIR / "wav_to_sentence.csv"
ENV_FILE = REPO / ".env"


def load_env():
    if not ENV_FILE.exists():
        print(f"[fatal] {ENV_FILE} missing", file=sys.stderr)
        sys.exit(2)
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()


load_env()

SCRIPTS_DIR = REPO / "audit" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import lib_audio  # noqa: E402
import lib_mos    # noqa: E402
import lib_asr as lib_aai  # noqa: E402
import lib_asr_deepgram as lib_dg  # noqa: E402
import lib_asr_groq as lib_gq  # noqa: E402

BACKENDS = [
    ("aai", lib_aai),
    ("deepgram", lib_dg),
    ("groq", lib_gq),
]


def load_mapping() -> list[dict]:
    rows = []
    with MAPPING_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def signals_for_clip(wav_path: Path, gt: dict) -> dict:
    """Returns {dsp_block, mos_block, per_backend: {name: asr_block}}.

    DSP and MOS computed once. ASR via all three backends.
    """
    audio, sr = lib_audio.load_wav(str(wav_path))

    dsp = {
        "duration_s": float(len(audio) / sr) if sr > 0 else 0.0,
        "sample_rate_hz": int(sr),
        "silence_mid_clip_s": round(lib_audio.longest_silence_s(audio, sr), 3),
        "end_pop_db": round(lib_audio.end_pop_db(audio, sr), 2),
        "terminal_sample_abs": round(lib_audio.terminal_sample_abs(audio), 4),
    }

    print(f"  [{wav_path.name}] computing MOS...", flush=True)
    t0 = time.time()
    mos = lib_mos.all_mos_signals(audio, sr)
    print(f"    MOS: UTMOS={mos['utmos']:.2f} SQUIM_MOS={mos['squim_mos']:.2f} "
          f"PESQ={mos['squim_pesq']:.2f}  ({time.time()-t0:.1f}s)", flush=True)

    text = (gt.get("reference_text") or "").strip()
    asr_blocks = {}
    for name, mod in BACKENDS:
        print(f"  [{wav_path.name}] {name} ASR (3 calls)...", flush=True)
        t0 = time.time()
        try:
            tr = mod.transcribe_all(str(wav_path))
        except Exception as e:
            print(f"    [ERR] {name} failed: {type(e).__name__}: {e}", flush=True)
            raise
        block = {
            "transcript_hi":         tr["transcript_hi"],
            "transcript_en_forced":  tr["transcript_en_forced"],
            "transcript_roman":      tr["transcript_roman"],
            "detected_lang":         tr.get("detected_lang", ""),
            "cer_devanagari":  round(mod.cer(text, tr["transcript_hi"]), 4),
            "wer_roman":       round(mod.wer(text, tr["transcript_roman"]), 4),
            "wer_en_forced":   round(mod.wer(text, tr["transcript_en_forced"]), 4),
        }
        print(f"    {name}: CER={block['cer_devanagari']:.3f} "
              f"WER_rom={block['wer_roman']:.3f} WER_en={block['wer_en_forced']:.3f}  "
              f"({time.time()-t0:.1f}s)", flush=True)
        asr_blocks[name] = block

    return {
        "id": wav_path.stem,                # e.g. "human_01"
        "model": "human_groundtruth",
        "category": gt.get("category"),
        "text": text,
        "expected_pronunciation_notes": "",
        "tested_phenomenon": gt.get("tested_phenomenon", ""),
        "_dsp": dsp,
        "_mos": mos,
        "_asr": asr_blocks,
    }


def main() -> int:
    mapping = load_mapping()
    print(f"=== Stage 1 (human GT): {len(mapping)} clips × 3 ASR backends ===\n")
    t_total = time.time()

    enriched = []
    for r in mapping:
        wav = WAVS_DIR / r["filename"]
        if not wav.exists():
            print(f"[fatal] missing {wav}", file=sys.stderr)
            return 1
        print(f"[clip] {r['filename']}  id={r['sentence_id']}  cat={r['category']}", flush=True)
        rec = signals_for_clip(wav, r)
        enriched.append(rec)
        print()

    for backend, _mod in BACKENDS:
        out = []
        for rec in enriched:
            entry = {
                "model": rec["model"],
                "id": rec["id"],
                "category": rec["category"],
                "text": rec["text"],
                "expected_pronunciation_notes": rec["expected_pronunciation_notes"],
                "tested_phenomenon": rec["tested_phenomenon"],
                **rec["_dsp"],
                **rec["_asr"][backend],
                **rec["_mos"],
            }
            out.append(entry)
        path = GT_DIR / f"signal_vectors_{backend}.json"
        path.write_text(json.dumps(out, ensure_ascii=False, indent=1))
        print(f"  wrote {path.relative_to(REPO)} ({len(out)} entries)")

    print(f"\nTotal time: {(time.time()-t_total)/60:.1f} min")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
