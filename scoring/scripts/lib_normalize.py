"""Hinglish normalizer — converts any script-mix Hinglish text to Devanagari.

Public API
----------
to_unified_devanagari(text: str) -> str
    Convert Hinglish text (any script mix) to Devanagari for IndicF5 input.
    Idempotent: applying twice gives the same result.

ROMAN_HINDI_FUNCTION_WORDS : dict[str, str]
    Short Roman-script Hindi function words that IndicXlit misreads as English
    phonetics (e.g. "mai" → "माई" instead of "मैं"). Whitelist intercepts first.

ENGLISH_LOAN_CANONICAL : dict[str, str]
    English loanwords common in Hinglish — canonical Devanagari renderings.

INDIAN_NE_CANONICAL : dict[str, str]
    Indian named entities (cities, people, brands) — canonical Devanagari.

Strategy
--------
1. Tokenize on whitespace + punctuation boundaries (preserve punctuation).
2. Per token:
   - Pure Devanagari (or other Indic script): pass through unchanged.
   - Pure ASCII alphabetic: lowercase + strip apostrophes, then:
       a. look up in whitelist tables (ROMAN_HINDI_FUNCTION_WORDS first,
          then ENGLISH_LOAN_CANONICAL, then INDIAN_NE_CANONICAL)
       b. else transliterate via IndicXlit (topk=1, deterministic)
   - Numeric / pure-punctuation: pass through.
"""
from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# Public whitelist tables (v2.1)
# ---------------------------------------------------------------------------

# Short Hindi function words in Roman script — IndicXlit maps these to English
# phonetics. The correct Hindi forms are listed here; the whitelist intercepts
# before IndicXlit sees the token.
ROMAN_HINDI_FUNCTION_WORDS: dict[str, str] = {
    "aa":  "आ",   # "come" / leading vowel — IndicXlit gives "एए"
    "hu":  "हूं",  # "am" (1st person) — IndicXlit gives "हू" (drops nasal)
    "mai": "मैं",  # "I" — IndicXlit gives "माई" (English "my")
    "tu":  "तू",   # "you" (informal) — IndicXlit gives "टू" (English "to")
}

# English loanwords common in Hinglish — stable canonical Devanagari renderings.
ENGLISH_LOAN_CANONICAL: dict[str, str] = {
    "biryani":      "बिरयानी",
    "boss":         "बॉस",
    "butter":       "बटर",
    "cancel":       "कैंसल",
    "chicken":      "चिकन",
    "close":        "क्लोज़",
    "deadline":     "डेडलाइन",
    "deliver":      "डिलीवर",
    "event":        "इवेंट",
    "file":         "फाइल",
    "homework":     "होमवर्क",
    "issue":        "इश्यू",
    "laptop":       "लैपटॉप",
    "leave":        "लीव",
    "log":          "लॉग",
    "lucky":        "लकी",
    "lunch":        "लंच",
    "message":      "मैसेज",
    "movie":        "मूवी",
    "nervous":      "नर्वस",
    "new":          "न्यू",
    "office":       "ऑफिस",
    "party":        "पार्टी",
    "personal":     "पर्सनल",
    "place":        "प्लेस",
    "please":       "प्लीज़",
    "presentation": "प्रेज़ेंटेशन",
    "quickly":      "क्विकली",
    "reply":        "रिप्लाई",
    "restaurant":   "रेस्टोरेंट",
    "review":       "रिव्यू",
    "ticket":       "टिकट",
    "tomorrow":     "टुमॉरो",
    "try":          "ट्राई",
    "wait":         "वेट",
    "waste":        "वेस्ट",
}

# Indian named entities (cities, people, brands) — canonical Devanagari.
# Apostrophes are stripped before lookup ("Karim's" → "karim").
INDIAN_NE_CANONICAL: dict[str, str] = {
    "aishwarya":   "ऐश्वर्या",
    "arjun":       "अर्जुन",
    "bengaluru":   "बेंगलुरु",
    "chennai":     "चेन्नई",
    "connaught":   "कनॉट",
    "consultancy": "कंसल्टेंसी",
    "delhi":       "दिल्ली",
    "hyderabad":   "हैदराबाद",
    "karim":       "करीम",
    "khanna":      "खन्ना",
    "mr":          "मिस्टर",
    "mumbai":      "मुंबई",
    "old":         "ओल्ड",
    "paradise":    "पैराडाइज़",
    "priya":       "प्रिया",
    "pune":        "पुणे",
    "rohan":       "रोहन",
    "services":    "सर्विसेज़",
    "tata":        "टाटा",
}


# ---------------------------------------------------------------------------
# Internal: merged lookup + IndicXlit engine
# ---------------------------------------------------------------------------

_CANONICAL: dict[str, str] = {
    **ROMAN_HINDI_FUNCTION_WORDS,   # checked first — short tokens, high collision risk
    **ENGLISH_LOAN_CANONICAL,
    **INDIAN_NE_CANONICAL,
}

_xlit_engine = None


def _get_xlit():
    global _xlit_engine
    if _xlit_engine is None:
        from ai4bharat.transliteration import XlitEngine
        _xlit_engine = XlitEngine("hi", beam_width=4, src_script_type="en")
    return _xlit_engine


# ---------------------------------------------------------------------------
# Internal: token classification
# ---------------------------------------------------------------------------

_DEVANAGARI_RANGE = (0x0900, 0x097F)

# Captures: ASCII alpha runs | Devanagari runs | digit runs | whitespace |
# any single char (punctuation, apostrophes, etc.)
# Apostrophes are NOT folded into ASCII alpha tokens so "Karim's" →
# ["Karim", "'", "s"] — "karim" then hits the NE whitelist cleanly.
_TOKEN_RE = re.compile(
    r"([A-Za-z]+"
    r"|[ऀ-ॿ]+"
    r"|\d+"
    r"|\s+"
    r"|.)"
)


def _is_devanagari_token(tok: str) -> bool:
    has_deva = any(_DEVANAGARI_RANGE[0] <= ord(c) <= _DEVANAGARI_RANGE[1] for c in tok)
    has_ascii_alpha = any(c.isascii() and c.isalpha() for c in tok)
    return has_deva and not has_ascii_alpha


def _is_ascii_alpha_token(tok: str) -> bool:
    if not tok:
        return False
    return all(c.isascii() and (c.isalpha() or c == "'") for c in tok)


def _normalize_ascii_token(tok: str) -> str:
    key = tok.lower()
    if key in _CANONICAL:
        return _CANONICAL[key]
    xlit = _get_xlit()
    result = xlit.translit_word(key, topk=1)
    if isinstance(result, dict):
        cands = result.get("hi") or next(iter(result.values()), [])
    elif isinstance(result, list):
        cands = result
    else:
        cands = []
    if cands:
        return cands[0]
    return tok


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def to_unified_devanagari(text: str) -> str:
    """Convert Hinglish text (any script mix) to Devanagari for IndicF5 input.

    Idempotent: applying twice gives the same result.
    """
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
            out.append(tok)
    return "".join(out)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    TESTS = [
        ("कल मुझे दिल्ली जाना है।",
            ["कल", "मुझे", "दिल्ली", "जाना", "है"],
            "pure Devanagari — pass-through"),
        ("kal mujhe office jaana hai",
            ["ऑफिस"],
            "Roman Hindi — canonical English loan"),
        ("My friend Aishwarya from Chennai is visiting Bengaluru next week.",
            ["ऐश्वर्या", "चेन्नई", "बेंगलुरु"],
            "English with Indian NEs"),
        ("Mera presentation tomorrow है, और मैं nervous हूं।",
            ["प्रेज़ेंटेशन", "टुमॉरो", "नर्वस", "और", "मैं"],
            "mixed script — loans + Devanagari pass-through"),
        ("Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।",
            ["बॉस", "लीव", "पर्सनल"],
            "mixed script — Roman loans"),
        ("I love butter chicken from Karim's in Old Delhi.",
            ["बटर", "चिकन", "करीम", "ओल्ड", "दिल्ली"],
            "English with NE + apostrophe stripping"),
        ("She just got hired at Tata Consultancy Services in Pune.",
            ["टाटा", "कंसल्टेंसी", "सर्विसेज़", "पुणे"],
            "English with Indian brand NEs"),
        ("mai ghar aa raha hu",
            ["मैं", "आ", "हूं"],
            "Roman Hindi function words whitelist"),
    ]

    print("Loading IndicXlit (first call may take 30–60s)...")
    _ = _get_xlit()
    print("OK\n")

    failed = 0
    for inp, expected, label in TESTS:
        out = to_unified_devanagari(inp)
        missing = [s for s in expected if s not in out]
        status = "OK  " if not missing else "FAIL"
        print(f"  {status} [{label}]")
        if missing:
            print(f"       in:      {inp}")
            print(f"       out:     {out}")
            print(f"       missing: {missing}")
            failed += 1
        else:
            print(f"       out: {out}")

    print("\nIdempotency check:")
    for inp, _, label in TESTS[:4]:
        once = to_unified_devanagari(inp)
        twice = to_unified_devanagari(once)
        if once != twice:
            print(f"  FAIL [{label}] — not idempotent")
            print(f"       once:  {once}")
            print(f"       twice: {twice}")
            failed += 1
        else:
            print(f"  OK   [{label}]")

    print(f"\n{'PASSED' if failed == 0 else f'FAILED ({failed} tests)'}")
    sys.exit(0 if failed == 0 else 1)
