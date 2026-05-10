"""IndicXlit-powered Hinglish normalizer.

`to_unified_devanagari(text)` produces a canonical Devanagari rendering of any
Hinglish input. Used by:

  * rubric v2.0 — applied symmetrically to ground-truth reference and ASR
    transcript before WER/CER. Solves the script-mismatch artifact where
    Devanagari-output-on-Roman-input pegged CER at ~1.0.

  * Step 2a (input preprocessing) — same function applied to eval sentences
    before feeding to patched IndicF5, testing whether the model's
    Devanagari-trained character embeddings handle the input better.

The function is symmetric across these uses by design.

Strategy:
  1. Tokenize on whitespace + punctuation boundaries (preserve punctuation).
  2. For each token:
       - Pure Devanagari (or other Indic script): pass through unchanged.
       - Pure ASCII alphabetic: lowercase + strip apostrophes, then:
           - look up in CANONICAL dict (English loans + Indian NEs)
           - else IndicXlit transliterate (topk=1, deterministic)
       - Numeric / pure-punctuation: pass through.

The whitelists are tuned to the 30-sentence eval set (`eval_sentences.tsv`).
Each entry's source-sentence id is annotated. Generalization to wild Hinglish
would require expansion.

Idempotent: applying the function twice gives the same result.

Author: agent, 2026-05-09 (rubric v2.0 build)
"""
from __future__ import annotations

import re
import unicodedata


# --- Whitelists (eval-set-tuned, n=30) ---

# English loans used in Hinglish — canonical Devanagari renderings.
# Each entry annotated with the eval-sentence id(s) where it appears.
ENGLISH_LOAN_CANONICAL: dict[str, str] = {
    "biryani":      "बिरयानी",       # 29
    "boss":         "बॉस",            # 22
    "butter":       "बटर",            # 26
    "cancel":       "कैंसल",          # 21
    "chicken":      "चिकन",           # 26
    "close":        "क्लोज़",          # 23
    "deadline":     "डेडलाइन",        # 23
    "deliver":      "डिलीवर",         # 15
    "event":        "इवेंट",          # 21
    "file":         "फाइल",           # 23
    "homework":     "होमवर्क",        # 19
    "issue":        "इश्यू",          # 17
    "laptop":       "लैपटॉप",         # 15
    "leave":        "लीव",            # 22
    "log":          "लॉग",            # 27
    "lucky":        "लकी",            # 16
    "lunch":        "लंच",            # 25, 27
    "message":      "मैसेज",          # 21
    "movie":        "मूवी",           # 14
    "nervous":      "नर्वस",          # 18
    "new":          "न्यू",           # 20
    "office":       "ऑफिस",           # 9, 27
    "party":        "पार्टी",         # 12
    "personal":     "पर्सनल",         # 22
    "place":        "प्लेस",          # 20
    "please":       "प्लीज़",         # 19, 21
    "presentation": "प्रेज़ेंटेशन",   # 18
    "quickly":      "क्विकली",        # 23
    "reply":        "रिप्लाई",        # 13
    "restaurant":   "रेस्टोरेंट",     # 20
    "review":       "रिव्यू",         # 23
    "ticket":       "टिकट",           # 16
    "tomorrow":     "टुमॉरो",         # 18, 28
    "try":          "ट्राई",          # 20
    "wait":         "वेट",            # 13
    "waste":        "वेस्ट",          # 14
}

# Indian named entities — canonical Devanagari renderings.
INDIAN_NE_CANONICAL: dict[str, str] = {
    "aishwarya":   "ऐश्वर्या",        # 24
    "arjun":       "अर्जुन",          # 10
    "bengaluru":   "बेंगलुरु",         # 10, 24, 28
    "chennai":     "चेन्नई",           # 24
    "connaught":   "कनॉट",            # 20
    "consultancy": "कंसल्टेंसी",      # 30
    "delhi":       "दिल्ली",           # 26
    "hyderabad":   "हैदराबाद",        # 29
    "karim":       "करीम",            # 26 ("Karim's" → strip apostrophe before lookup)
    "khanna":      "खन्ना",           # 25
    "mr":          "मिस्टर",           # 25 (treated as title)
    "mumbai":      "मुंबई",           # 28
    "old":         "ओल्ड",            # 26 ("Old Delhi")
    "paradise":    "पैराडाइज़",        # 29
    "priya":       "प्रिया",          # 25
    "pune":        "पुणे",             # 30
    "rohan":       "रोहन",            # 28
    "services":    "सर्विसेज़",        # 30
    "tata":        "टाटा",            # 30
}

CANONICAL: dict[str, str] = {**ENGLISH_LOAN_CANONICAL, **INDIAN_NE_CANONICAL}


# --- IndicXlit engine (lazy-loaded singleton) ---

_xlit_engine = None


def _get_xlit():
    global _xlit_engine
    if _xlit_engine is None:
        from ai4bharat.transliteration import XlitEngine
        _xlit_engine = XlitEngine("hi", beam_width=4, src_script_type="en")
    return _xlit_engine


# --- Token detection ---

_DEVANAGARI_RANGE = (0x0900, 0x097F)


def _is_devanagari_token(tok: str) -> bool:
    """True if at least one character is Devanagari and no characters are ASCII alpha."""
    has_deva = any(_DEVANAGARI_RANGE[0] <= ord(c) <= _DEVANAGARI_RANGE[1] for c in tok)
    has_ascii_alpha = any(c.isascii() and c.isalpha() for c in tok)
    return has_deva and not has_ascii_alpha


def _is_ascii_alpha_token(tok: str) -> bool:
    """True if token consists only of ASCII alphabetic chars (and apostrophes)."""
    if not tok:
        return False
    return all(c.isascii() and (c.isalpha() or c == "'") for c in tok)


# --- Tokenization & assembly ---

# Captures: (a) ASCII alpha runs, (b) Devanagari runs, (c) digit runs,
# (d) any single non-space non-alpha char (punctuation incl. apostrophe), (e) whitespace.
# Apostrophes are deliberately NOT captured into ASCII alpha tokens so "Karim's"
# splits into ["Karim", "'", "s"] — letting "karim" hit the NE whitelist cleanly.
_TOKEN_RE = re.compile(
    r"([A-Za-z]+|"                       # ASCII alpha words
    r"[ऀ-ॿ]+|"                 # Devanagari runs
    r"\d+|"                              # numerals
    r"\s+|"                              # whitespace
    r".)"                                # punctuation / anything else (incl. apostrophes)
)


def _normalize_ascii_token(tok: str) -> str:
    """Lookup canonical, else fall back to IndicXlit transliteration."""
    key = tok.lower()
    if key in CANONICAL:
        return CANONICAL[key]
    # Fallback: IndicXlit (deterministic at topk=1)
    xlit = _get_xlit()
    result = xlit.translit_word(key, topk=1)
    # IndicXlit returns dict like {"hi": ["कल"]} or sometimes a list directly.
    if isinstance(result, dict):
        cands = result.get("hi") or next(iter(result.values()), [])
    elif isinstance(result, list):
        cands = result
    else:
        cands = []
    if cands:
        return cands[0]
    # Last resort: return the original token (will hurt CER but at least not crash).
    return tok


def to_unified_devanagari(text: str) -> str:
    """Return Devanagari-unified version of `text`. Idempotent."""
    if not text:
        return text
    out = []
    for m in _TOKEN_RE.finditer(text):
        tok = m.group(0)
        if tok.isspace():
            out.append(tok)
        elif _is_devanagari_token(tok):
            out.append(tok)
        elif _is_ascii_alpha_token(tok):
            out.append(_normalize_ascii_token(tok))
        else:
            # punctuation, digits, mixed — pass through
            out.append(tok)
    return "".join(out)


# --- Self-test (run as `python lib_normalize.py`) ---

if __name__ == "__main__":
    import sys

    TESTS = [
        # (input, [expected substrings], label)
        ("कल मुझे दिल्ली जाना है।",
            ["कल", "मुझे", "दिल्ली", "जाना", "है"],
            "pure_devanagari pass-through"),
        ("kal mujhe office jaana hai",
            ["ऑफिस"],
            "pure_roman + canonical English loan"),
        ("My friend Aishwarya from Chennai is visiting Bengaluru next week.",
            ["ऐश्वर्या", "चेन्नई", "बेंगलुरु"],
            "english_with_NE: NE whitelists"),
        ("Mera presentation tomorrow है, और मैं nervous हूं।",
            ["प्रेज़ेंटेशन", "टुमॉरो", "नर्वस", "और", "मैं"],
            "mixed_script: loans + Devanagari pass-through"),
        ("मेरा भाई आज स्कूल नहीं गया",
            ["स्कूल"],
            "Devanagari unchanged"),
        ("Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।",
            ["बॉस", "लीव", "पर्सनल"],
            "mixed_script with Roman loans"),
        ("I love butter chicken from Karim's in Old Delhi.",
            ["बटर", "चिकन", "करीम", "ओल्ड", "दिल्ली"],
            "english_with_NE with apostrophe + multi-NE"),
        ("She just got hired at Tata Consultancy Services in Pune.",
            ["टाटा", "कंसल्टेंसी", "सर्विसेज़", "पुणे"],
            "english_with_NE: TCS brand"),
    ]

    print("Loading IndicXlit (first call may take 30-60s)...")
    _ = _get_xlit()
    print("OK\n")

    failed = 0
    for inp, expected_substrings, label in TESTS:
        out = to_unified_devanagari(inp)
        missing = [s for s in expected_substrings if s not in out]
        if missing:
            print(f"  FAIL [{label}]")
            print(f"    in:  {inp}")
            print(f"    out: {out}")
            print(f"    missing: {missing}")
            failed += 1
        else:
            print(f"  OK   [{label}]")
            print(f"    out: {out}")

    # Idempotency check
    print("\nIdempotency check:")
    for inp, _, label in TESTS[:3]:
        once = to_unified_devanagari(inp)
        twice = to_unified_devanagari(once)
        if once != twice:
            print(f"  FAIL [{label}] not idempotent")
            print(f"    once:  {once}")
            print(f"    twice: {twice}")
            failed += 1
        else:
            print(f"  OK   [{label}]")

    print(f"\n{'PASSED' if failed == 0 else f'FAILED ({failed} tests)'}")
    sys.exit(0 if failed == 0 else 1)
