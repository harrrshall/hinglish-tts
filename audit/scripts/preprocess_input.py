"""Preprocess Hinglish input text to Devanagari before feeding to IndicF5.

Phase 2 Step 2a — embedding-undertraining mitigation experiment.

EXECUTION PATH (2026-05-10): the actual production run for Step 2a happens
inside the Kaggle kernel rather than here. The local IndicXlit install path
(via venv-scoring-py311 / venv-scoring) hits a fairseq+hydra+omegaconf
dataclass-mutable-default cascade on Python 3.11+ that wasn't resolvable in
a reasonable time on a slow network, so the equivalent code is inlined into
audit/indicf5_patched_xlit/KAGGLE_CELLS.md (PREPROCESS_CELL). This file is
kept as the canonical local-equivalent reference: identical logic, same
to_unified_devanagari call, same TSV schema. If you ever get a working
local IndicXlit, running this should produce the same output Kaggle does.

Hypothesis: IndicF5's ASCII character embeddings are undertrained
(see audit/indicf5_patched/COMPARISON.md §4 "RIGHT_LEN_GARBLED" — 15/22
residual failures show Devanagari surviving and Roman tokens turning into
acoustic noise after the duration patch).

Mitigation: transliterate any Roman-script tokens in the input to Devanagari
using IndicXlit (the same tool the rubric v2.0 uses for transcript
normalization), producing a unified-Devanagari input the model has seen at
training time.

Symmetry note: rubric v2.0 applies `to_unified_devanagari` to the *output*
(ASR transcripts) for scoring; here we apply it to the *input* (eval
sentences) before feeding to IndicF5. Same function, different application
point — see lib_normalize.py docstring.

Per-category behavior:
- pure_devanagari   : pass through unchanged (no ASCII alphabetic tokens).
- pure_roman        : Roman tokens → Devanagari; whitelisted English loans kept.
- mixed_script      : Roman tokens → Devanagari; existing Devanagari unchanged;
                      English loans whitelisted.
- english_with_NE   : Option A (default) — fully Devanagari; proper nouns
                      get canonical Indian-NE Devanagari forms from the
                      whitelist; surrounding English words are transliterated.

Run from project root:
    PYTHONPATH=audit/scripts venv-scoring-py311/bin/python audit/scripts/preprocess_input.py

Outputs:
    audit/indicf5_patched_xlit/preprocessed_sentences.tsv  (30 rows, side-by-side)
"""

import csv
import sys
from pathlib import Path

# Make lib_normalize importable when this script is run from project root
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from lib_normalize import to_unified_devanagari  # noqa: E402

EVAL_TSV = Path("audit/eval_sentences.tsv")
OUT_TSV = Path("audit/indicf5_patched_xlit/preprocessed_sentences.tsv")


def main() -> int:
    if not EVAL_TSV.exists():
        print(f"ERROR: {EVAL_TSV} not found. Run from project root.", file=sys.stderr)
        return 1

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)

    with open(EVAL_TSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    print(f"Loaded {len(rows)} eval sentences from {EVAL_TSV}")

    out_rows = []
    for r in rows:
        original = r["text"]
        preprocessed = to_unified_devanagari(original)
        out_rows.append({
            "id": r["id"],
            "category": r["category"],
            "text_original": original,
            "text_preprocessed": preprocessed,
            "preprocessing_applied": "yes" if preprocessed != original else "no",
        })

    with open(OUT_TSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"Wrote {OUT_TSV} ({len(out_rows)} rows)")

    # Idempotency spot-check on 3 sentences (one per non-Devanagari category)
    print("\nIdempotency spot-check:")
    sample_ids = {"09": "pure_roman", "17": "mixed_script", "24": "english_with_NE"}
    for r in out_rows:
        if r["id"] in sample_ids:
            once = r["text_preprocessed"]
            twice = to_unified_devanagari(once)
            ok = "OK" if once == twice else "FAIL"
            print(f"  [{ok}] id={r['id']} ({sample_ids[r['id']]})")
            if once != twice:
                print(f"        once:  {once!r}")
                print(f"        twice: {twice!r}")

    print("\nPreview by category (showing 2 of each):")
    for cat in ["pure_devanagari", "pure_roman", "mixed_script", "english_with_NE"]:
        cat_rows = [r for r in out_rows if r["category"] == cat]
        print(f"\n  --- {cat} ({len(cat_rows)} rows) ---")
        for r in cat_rows[:2]:
            tag = "changed" if r["preprocessing_applied"] == "yes" else "unchanged"
            print(f"    id={r['id']} [{tag}]")
            print(f"      original:    {r['text_original']}")
            print(f"      preprocessed: {r['text_preprocessed']}")

    n_changed = sum(1 for r in out_rows if r["preprocessing_applied"] == "yes")
    print(f"\nSummary: {n_changed}/{len(out_rows)} sentences changed by preprocessing")
    print("(pure_devanagari rows should be in the unchanged group; "
          "everything else should be in the changed group.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
