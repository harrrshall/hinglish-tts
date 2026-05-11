"""Stage-2: v2.1 enrichment + 3-ASR consensus judge.

Reads:
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_aai.json
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_deepgram.json
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_groq.json

Writes:
  experiments/04_indicf5_xlit_v2/scores/signal_vectors_v2.json   (all 90 enriched entries)
  experiments/04_indicf5_xlit_v2/scores/auto_scores_v2.1.csv     (30 consensus rows)

Run with py311 venv (needs fairseq for IndicXlit):
  cd ~/Desktop/hienglish
  ./venv-scoring-py311/bin/python experiments/04_indicf5_xlit_v2/scoring_scripts/enrich_and_judge.py
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import string
import sys
from pathlib import Path

import jiwer
import numpy as np

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = REPO / "scoring" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from lib_normalize import to_unified_devanagari

SCORES   = REPO / "experiments" / "04_indicf5_xlit_v2" / "scores"
V2_OUT   = SCORES / "signal_vectors_v2.json"
CSV_OUT  = SCORES / "auto_scores_v2.1.csv"
MODEL    = "indicf5_patched_xlit_v2"

_PUNCT = string.punctuation + "।॥,।'\"‍‌"


def _strip_punct(text: str) -> str:
    out = "".join(" " if ch in _PUNCT else ch for ch in text)
    return re.sub(r"\s+", " ", out).strip()


def _cer(ref: str, hyp: str) -> float:
    ref, hyp = _strip_punct(ref), _strip_punct(hyp)
    return 1.0 if not ref else float(jiwer.cer(ref, hyp))


def _wer(ref: str, hyp: str) -> float:
    ref, hyp = _strip_punct(ref), _strip_punct(hyp)
    return 1.0 if not ref else float(jiwer.wer(ref, hyp))


def _token_overlap(ref_norm: str, hyp_norm: str) -> float:
    ref_toks = {t for t in _strip_punct(ref_norm).split() if len(t) > 1}
    hyp_toks = {t for t in _strip_punct(hyp_norm).split() if len(t) > 1}
    return 1.0 if not ref_toks else len(ref_toks & hyp_toks) / len(ref_toks)


# Cache normalizations so we don't call IndicXlit 3× for the same string
_norm_cache: dict[str, str] = {}


def _norm(text: str) -> str:
    if text not in _norm_cache:
        _norm_cache[text] = to_unified_devanagari(text)
    return _norm_cache[text]


def enrich(entry: dict, asr_backend: str) -> dict:
    text = entry.get("text", "") or ""
    th   = entry.get("transcript_hi", "") or ""
    tr   = entry.get("transcript_roman", "") or ""

    text_norm = _norm(text)
    th_norm   = _norm(th)
    tr_norm   = _norm(tr)

    silence_mid = float(entry.get("silence_mid_clip_s", 0.0))

    out = dict(entry)
    out.update({
        "text_normalized":             text_norm,
        "transcript_hi_normalized":    th_norm,
        "transcript_roman_normalized": tr_norm,
        "cer_devanagari_norm":         round(_cer(text_norm, th_norm), 4),
        "wer_roman_norm":              round(_wer(text_norm, tr_norm), 4),
        "asr_backend":                 asr_backend,
        "silence_or_skip_norm":        silence_mid > 0.5,
        "_token_overlap_norm":         round(_token_overlap(text_norm, th_norm), 4),
    })
    return out


def intel_score(cer_norm: float) -> int:
    if cer_norm <= 0.05: return 5
    if cer_norm <= 0.15: return 4
    if cer_norm <= 0.30: return 3
    if cer_norm <= 0.50: return 2
    return 1


def speaker_score(pesq: float, terminal_abs: float) -> int:
    if pesq >= 4.0:   s = 5
    elif pesq >= 3.5: s = 4
    elif pesq >= 3.0: s = 3
    elif pesq >= 2.5: s = 2
    else:             s = 1
    return max(1, s - 1) if terminal_abs > 0.05 else s


def end_pop(end_pop_db: float, terminal_abs: float) -> str:
    return "TRUE" if end_pop_db > 6.0 and terminal_abs > 0.005 else "FALSE"


def code_switch(intel: int, cat: str, pure_mean: float) -> int:
    if cat in ("pure_devanagari", "pure_roman"):
        return intel
    gap = pure_mean - intel
    if gap <= 0.05: return 5
    if gap <= 0.15: return 4
    if gap <= 0.30: return 3
    if gap <= 0.50: return 2
    return 1


def consensus_intel(scores: list[int]) -> int:
    """Median of the three backend scores (rounds to nearest int)."""
    return round(statistics.median(scores))


def main() -> int:
    # ── Load all three backends ──────────────────────────────────────────────
    backends = {
        "aai":      SCORES / "signal_vectors_aai.json",
        "deepgram": SCORES / "signal_vectors_deepgram.json",
        "groq":     SCORES / "signal_vectors_groq.json",
    }
    raw: dict[str, list[dict]] = {}
    for name, path in backends.items():
        data = json.loads(path.read_text())
        print(f"Loaded {name}: {len(data)} entries")
        raw[name] = {e["id"]: e for e in data}

    # ── Enrich with v2.1 normalized CER/WER (IndicXlit lazy-loads on first call)
    print("\n=== v2.1 enrichment (IndicXlit normalizer) ===")
    enriched_by_backend: dict[str, dict[str, dict]] = {}
    all_ids = sorted(raw["aai"].keys(), key=lambda x: int(x) if x.isdigit() else 99)

    for name in ("aai", "deepgram", "groq"):
        enriched_by_backend[name] = {}
        for id_ in all_ids:
            e = raw[name].get(id_)
            if e is None:
                print(f"  [{name}] id={id_} missing — skipping")
                continue
            print(f"  [{name}] id={id_} ...", end=" ", flush=True)
            enriched_by_backend[name][id_] = enrich(e, name)
            print(f"cer_norm={enriched_by_backend[name][id_]['cer_devanagari_norm']:.3f}")

    # ── Write all 90 enriched entries ────────────────────────────────────────
    all_enriched = []
    for name in ("aai", "deepgram", "groq"):
        all_enriched.extend(enriched_by_backend[name].values())
    all_enriched.sort(key=lambda r: (int(r["id"]) if r["id"].isdigit() else 99,
                                     r["asr_backend"]))
    V2_OUT.write_text(json.dumps(all_enriched, ensure_ascii=False, indent=1))
    print(f"\nWrote {V2_OUT} ({len(all_enriched)} entries)")

    # ── 3-ASR consensus scoring ───────────────────────────────────────────────
    print("\n=== 3-ASR consensus judging ===")

    # Pure-category mean: median of each backend's pure mean, then average
    pure_intels_per_backend = []
    for name in ("aai", "deepgram", "groq"):
        pure = [enriched_by_backend[name][id_]
                for id_ in all_ids
                if enriched_by_backend[name].get(id_, {}).get("category")
                in ("pure_devanagari", "pure_roman")]
        if pure:
            mean = np.mean([intel_score(e["cer_devanagari_norm"]) for e in pure])
            pure_intels_per_backend.append(mean)
    pure_mean = float(np.mean(pure_intels_per_backend)) if pure_intels_per_backend else 4.0
    print(f"pure-category intel mean (across 3 backends): {pure_mean:.3f}")

    scored_rows = []
    for id_ in all_ids:
        # Gather intel score from each backend
        backend_intels = []
        for name in ("aai", "deepgram", "groq"):
            e = enriched_by_backend[name].get(id_)
            if e:
                backend_intels.append(intel_score(e["cer_devanagari_norm"]))

        if not backend_intels:
            print(f"  id={id_}: no backends — skipping")
            continue

        cons_intel = consensus_intel(backend_intels)

        # Use AAI entry for DSP fields (PESQ, end_pop, silence — audio-based, same for all)
        aai_e = enriched_by_backend["aai"].get(id_, {})
        pesq  = float(aai_e.get("squim_pesq", 0.0) or 0.0)
        term  = float(aai_e.get("terminal_sample_abs", 0.0) or 0.0)
        epdb  = float(aai_e.get("end_pop_db", 0.0) or 0.0)
        sil   = aai_e.get("silence_or_skip_norm", False)
        cat   = aai_e.get("category", "")
        text  = aai_e.get("text", "")
        text_norm = aai_e.get("text_normalized", "")

        intels_str = "/".join(str(x) for x in backend_intels)
        print(f"  id={id_:>2} cat={cat[:12]:12s}  "
              f"aai={backend_intels[0] if len(backend_intels)>0 else '?'} "
              f"dg={backend_intels[1] if len(backend_intels)>1 else '?'} "
              f"groq={backend_intels[2] if len(backend_intels)>2 else '?'} "
              f"→ consensus={cons_intel}")

        scored_rows.append({
            "model":                    MODEL,
            "id":                       id_,
            "category":                 cat,
            "text":                     text,
            "text_normalized":          text_norm,
            "intelligibility_1to5":     cons_intel,
            "naturalness_1to5":         "EAR_ONLY",
            "code_switch_handling_1to5": code_switch(cons_intel, cat, pure_mean),
            "speaker_quality_1to5":     speaker_score(pesq, term),
            "silence_or_skip":          "TRUE" if sil else "FALSE",
            "end_of_clip_pop":          end_pop(epdb, term),
            "rubric_version":           "2.1",
            "asr_backends":             "aai+deepgram+groq",
            "intel_per_backend":        intels_str,
            "cer_norm_aai":             enriched_by_backend["aai"].get(id_, {}).get("cer_devanagari_norm", ""),
            "cer_norm_deepgram":        enriched_by_backend["deepgram"].get(id_, {}).get("cer_devanagari_norm", ""),
            "cer_norm_groq":            enriched_by_backend["groq"].get(id_, {}).get("cer_devanagari_norm", ""),
            "squim_pesq":               round(pesq, 3),
            "notes": (
                f"3-ASR consensus ({intels_str}); "
                f"cer_norm_aai={enriched_by_backend['aai'].get(id_,{}).get('cer_devanagari_norm','?'):.3f}; "
                f"squim_pesq={pesq:.3f}"
            ),
        })

    # Sort by id
    scored_rows.sort(key=lambda r: int(r["id"]) if str(r["id"]).isdigit() else 99)

    fieldnames = [
        "model", "id", "category", "text", "text_normalized",
        "intelligibility_1to5", "naturalness_1to5", "code_switch_handling_1to5",
        "speaker_quality_1to5", "silence_or_skip", "end_of_clip_pop",
        "rubric_version", "asr_backends", "intel_per_backend",
        "cer_norm_aai", "cer_norm_deepgram", "cer_norm_groq", "squim_pesq", "notes",
    ]
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(scored_rows)
    print(f"\nWrote {CSV_OUT} — {len(scored_rows)} rows")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n=== Score summary (3-ASR consensus, rubric v2.1) ===")
    for cat in ("pure_devanagari", "pure_roman", "mixed_script", "english_with_NE", None):
        rows = [r for r in scored_rows if cat is None or r["category"] == cat]
        label = cat or "overall"
        if rows:
            mean_i = np.mean([r["intelligibility_1to5"] for r in rows])
            silence = sum(1 for r in rows if r["silence_or_skip"] == "TRUE")
            print(f"  {label:22s}: {mean_i:.2f}  silence_or_skip={silence}/{len(rows)}")

    mean_pesq = np.mean([r["squim_pesq"] for r in scored_rows])
    print(f"\n  mean PESQ: {mean_pesq:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
