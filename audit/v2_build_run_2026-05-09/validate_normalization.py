"""Phase 2 gate: validate IndicXlit normalization on the 8 human GT clips.

Threshold: post-normalization CER must fall under per-clip thresholds derived
from the v1.0 ceiling-report observations. If 3+ clips fail (>1.5x threshold),
stop and report — the normalization or whitelist needs work before integrating
into the v2.0 pipeline.

Reads:
  audit/human_groundtruth/signal_vectors_aai.json   (use AAI as canonical
    backend for this validation; AAI's transcript_hi is consistently the closest
    to the reference script across the 8 clips per the ceiling report)

Writes:
  audit/v2_validation/normalization_validation.json (per-clip detail)
  Also prints a summary table to stdout.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "audit" / "scripts"))

from lib_normalize import to_unified_devanagari, compute_cer, compute_wer

GT_SIGNALS = REPO / "audit" / "human_groundtruth" / "signal_vectors_aai.json"
OUT_PATH = REPO / "audit" / "v2_validation" / "normalization_validation.json"

# Per-clip thresholds, set per the spec. Derived from the v1.0 ceiling report
# observations (script-mismatch artifact corrupted pure_roman; Devanagari
# pass-through clean). Pass criterion: post-normalization CER < threshold * 1.5.
EXPECTED_THRESHOLDS = {
    "human_01": 0.05,  # pure_devanagari Devanagari→Devanagari, should stay clean
    "human_02": 0.10,  # pure_devanagari, slight ASR variation expected
    "human_03": 0.15,  # pure_roman → Devanagari pivot via canonical "office"
    "human_04": 0.15,  # pure_roman, no English loans, pure transliteration
    "human_05": 0.30,  # mixed_script, hardest case
    "human_06": 0.20,  # mixed_script with English loans
    "human_07": 0.15,  # english_with_NE, mostly canonical NEs
    "human_08": 0.20,  # english_with_NE, includes "Karim's" apostrophe quirk
}


def main() -> int:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    gt = json.loads(GT_SIGNALS.read_text())

    results = []
    print(f"\n{'id':<10} {'cat':<18} {'CER_v1':>7} {'CER_v2':>7} {'thresh':>7} {'×':>5} {'flag':<6}")
    print("-" * 80)

    for entry in gt:
        rid = entry["id"]
        ref_text = entry["text"]
        # Use transcript_hi as primary (per the v1.0 rubric's mapping for
        # pure_devanagari + mixed_script). Fall back to transcript_roman if hi
        # is empty (which happens occasionally on some backends).
        transcript = entry.get("transcript_hi") or entry.get("transcript_roman", "")

        ref_norm = to_unified_devanagari(ref_text)
        hyp_norm = to_unified_devanagari(transcript)

        cer_v1 = entry.get("cer_devanagari", 1.0)
        cer_v2 = compute_cer(ref_norm, hyp_norm)
        wer_v2 = compute_wer(ref_norm, hyp_norm)

        threshold = EXPECTED_THRESHOLDS.get(rid, 0.30)
        ratio = cer_v2 / threshold if threshold > 0 else float("inf")
        status = "OK" if ratio < 1.5 else "FAIL"

        results.append({
            "id": rid,
            "category": entry["category"],
            "ref_original": ref_text,
            "ref_normalized": ref_norm,
            "hyp_original": transcript,
            "hyp_normalized": hyp_norm,
            "cer_v1": round(cer_v1, 4),
            "cer_v2_unified": round(cer_v2, 4),
            "wer_v2_unified": round(wer_v2, 4),
            "threshold": threshold,
            "ratio_to_threshold": round(ratio, 2),
            "status": status,
        })
        print(f"{rid:<10} {entry['category']:<18} "
              f"{cer_v1:>7.3f} {cer_v2:>7.3f} {threshold:>7.2f} "
              f"{ratio:>5.2f} {status:<6}")

    n_fail = sum(1 for r in results if r["status"] == "FAIL")
    print(f"\n{n_fail}/{len(results)} clips FAILED the threshold gate (criterion: <1.5× expected).\n")

    if n_fail > 0:
        print("Per-clip detail for failing clips:\n")
        for r in results:
            if r["status"] != "FAIL":
                continue
            print(f"  {r['id']} ({r['category']})")
            print(f"    ref orig:  {r['ref_original']}")
            print(f"    ref norm:  {r['ref_normalized']}")
            print(f"    hyp orig:  {r['hyp_original']}")
            print(f"    hyp norm:  {r['hyp_normalized']}")
            print(f"    CER v2={r['cer_v2_unified']:.3f}, threshold={r['threshold']:.2f}, ratio={r['ratio_to_threshold']:.2f}\n")

    OUT_PATH.write_text(json.dumps({
        "n_clips": len(results),
        "n_fail": n_fail,
        "gate_passed": n_fail <= 2,  # spec: stop if >2 fail
        "per_clip": results,
    }, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT_PATH.relative_to(REPO)}")

    if n_fail > 2:
        print("\nGATE FAILED — more than 2 clips exceeded their threshold by 1.5×.")
        print("Will NOT proceed to Phase 3 without user input on whitelist or threshold adjustments.")
        return 1
    print("\nGATE PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
