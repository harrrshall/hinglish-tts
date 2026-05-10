#!/usr/bin/env python3
"""Build audit/eval_sentences.tsv per AUDIT_PLAN.md §1.

Anchors (12) are taken VERBATIM from AUDIT_PLAN.md §1.2 and must not be
edited. The remaining 18 lines (§1.3) are casual-register Hinglish / Hindi /
English-with-Indian-NE chosen to (a) cover every phenomenon tag from §1.4,
(b) keep length 5–15 words, (c) include questions, imperatives, and
exclamations within each category where natural.

Self-checks from §1.5 are run inline; the script exits non-zero if any fail.

NOTE on a runbook inconsistency (logged in RUN_NOTES.md): §1.1 dictates
8/8/8/6 totals (= 30) but §1.3 lists 27–30 as the english_with_NE generated
range, which gives 8/8/7/7. We honor the §1.1 contract — ID 27 is therefore
mixed_script (5 generated for that category: 20, 21, 22, 23, 27), and
english_with_NE generated IDs are 28, 29, 30 (3 generated, 3 anchored).

Run:
    python audit/scripts/build_eval_set.py
"""
from __future__ import annotations

import csv
import random
import sys
from collections import Counter
from pathlib import Path


HEADER = ["id", "category", "text", "expected_pronunciation_notes", "tested_phenomenon"]


# ── §1.2 anchors — verbatim, do not edit ──────────────────────────────────
ANCHORS: list[tuple[str, str, str, str, str]] = [
    ("01", "pure_devanagari",
     "कल मुझे दिल्ली जाना है।",
     "Standard Hindi declarative.",
     "baseline_devanagari"),
    ("02", "pure_devanagari",
     "क्या आप मुझे पानी दे सकते हैं?",
     "Polite Hindi question.",
     "question_devanagari"),
    ("03", "pure_devanagari",
     "मेरा भाई आज स्कूल नहीं गया क्योंकि उसकी तबीयत खराब है।",
     "Long Hindi sentence with English loanword \"स्कूल\" written in Devanagari.",
     "loanword_in_devanagari"),

    ("09", "pure_roman",
     "kal mujhe office jaana hai",
     "Should sound Hindi, NOT English. \"office\" is the only English word.",
     "roman_hindi_with_english_loan"),
    ("10", "pure_roman",
     "mera naam Arjun hai aur mai Bengaluru se hu",
     "\"hai\" is Hindi \"is\", NOT \"hi\" greeting. \"Bengaluru\" must be pronounced Indian, not anglicized.",
     "homograph_hai_hi"),
    ("11", "pure_roman",
     "yaar tu kal kya kar raha tha",
     "Casual Hinglish, common words yaar/tu/kya.",
     "casual_roman_hindi"),

    ("17", "mixed_script",
     "Kal mujhe ऑफिस जाना hai, but ट्राफिक will be an issue.",
     "The hardest case — script switches mid-sentence.",
     "mixed_script_hard"),
    ("18", "mixed_script",
     "Mera presentation tomorrow है, और मैं nervous हूं।",
     "Hindi grammar around English content words.",
     "mixed_script_grammar"),
    ("19", "mixed_script",
     "Bhai please मेरा homework कर दे, मैं तुझे ₹100 दूंगा।",
     "Currency symbol + Devanagari numerals/script switch.",
     "mixed_script_currency"),

    ("24", "english_with_NE",
     "My friend Aishwarya from Chennai is visiting Bengaluru next week.",
     "Three Indian named entities in pure-English sentence.",
     "english_with_indian_NE"),
    ("25", "english_with_NE",
     "Mr. Khanna will join the meeting after he finishes lunch with Priya.",
     "Indian surname + first name in English context.",
     "english_with_indian_names"),
    ("26", "english_with_NE",
     "I love butter chicken from Karim's in Old Delhi.",
     "Restaurant + locality, Indian food name.",
     "english_with_food_locality"),
]


# ── §1.3 generated — casual register, 5–15 words, all 18 phenomena covered ─
GENERATED: list[tuple[str, str, str, str, str]] = [
    # pure_devanagari — fill 04-08 (5 sentences)
    ("04", "pure_devanagari",
     "मेरे पास सिर्फ़ तीन सौ रुपये हैं, बस इतने में चला लो।",
     "Numerals expressed in Devanagari words; casual register.",
     "numbers_devanagari"),
    ("05", "pure_devanagari",
     "जल्दी आओ यार, सब तेरा इंतज़ार कर रहे हैं।",
     "Casual imperative with informal pronoun \"तेरा\".",
     "imperative_devanagari"),
    ("06", "pure_devanagari",
     "आज बहुत थक गया हूँ, बस सीधा सोना चाहता हूँ।",
     "Casual declarative; common contraction \"सीधा\".",
     "baseline_devanagari"),
    ("07", "pure_devanagari",
     "तुझे पता है कल मीटिंग कितने बजे है?",
     "Informal question; \"मीटिंग\" is an English loanword in Devanagari.",
     "question_devanagari"),
    ("08", "pure_devanagari",
     "अरे यार, मेरा फ़ोन कहाँ रखा था?!",
     "Exclamative question; everyday casual reaction.",
     "imperative_devanagari"),

    # pure_roman — fill 12-16 (5 sentences)
    ("12", "pure_roman",
     "kya tu bhi aaj party me aa raha hai?",
     "Roman-script Hindi question with English loan \"party\".",
     "roman_question"),
    ("13", "pure_roman",
     "abe yaar jaldi reply kar, mai wait kar raha hu",
     "Roman-Hindi imperative; \"reply\" and \"wait\" must NOT be re-anglicized in pronunciation.",
     "roman_imperative"),
    ("14", "pure_roman",
     "kal raat ka movie tha bohot bakwaas, paisa bilkul waste",
     "Casual film reaction; multiple English loans inside Roman-Hindi.",
     "casual_roman_hindi"),
    ("15", "pure_roman",
     "tera laptop kab tak deliver hoga bhai?",
     "Roman-Hindi question with English nouns \"laptop\" / \"deliver\".",
     "roman_hindi_with_english_loan"),
    ("16", "pure_roman",
     "yaar tu bohot lucky hai, mujhe nahi mila ticket!",
     "Casual exclamation; \"hai\" must read as Hindi \"is\", not \"hi\".",
     "casual_roman_hindi"),

    # mixed_script — fill 20-23 + 27 (5 sentences, see header for §1.1 vs §1.3 fix)
    ("20", "mixed_script",
     "Tumne वो new restaurant try kiya jo Connaught Place में khula hai?",
     "Mid-sentence script switch with question intonation.",
     "mixed_script_question"),
    ("21", "mixed_script",
     "कल का event cancel हो गया, सबको message कर देना please।",
     "English content nouns inside Hindi grammatical frame.",
     "mixed_script_grammar"),
    ("22", "mixed_script",
     "Boss को बता देना kal मैं leave पर रहूँगा, kuch personal काम है।",
     "Heavy code-switching; office register; double script switches.",
     "mixed_script_hard"),
    ("23", "mixed_script",
     "Ye file को quickly review करो, deadline बहुत close है।",
     "Imperative with English verb embedded in Hindi auxiliary structure.",
     "mixed_script_grammar"),
    ("27", "mixed_script",
     "Office में सब log lunch के लिए बाहर गए, तू भी आ ja yaar.",
     "Office casual register; English content nouns inside Hindi frame.",
     "mixed_script_grammar"),

    # english_with_NE — fill 28-30 (3 sentences)
    ("28", "english_with_NE",
     "Rohan is flying from Mumbai to Bengaluru tomorrow morning for work.",
     "Three Indian named entities (one personal, two cities) in English.",
     "english_with_indian_NE"),
    ("29", "english_with_NE",
     "Let's grab biryani from Paradise in Hyderabad this weekend.",
     "Indian food + restaurant + city in English context.",
     "english_with_food_locality"),
    ("30", "english_with_NE",
     "She just got hired at Tata Consultancy Services in Pune.",
     "Indian company brand in pure-English sentence.",
     "english_with_indian_brand"),
]


REQUIRED_TAGS = {
    "baseline_devanagari", "question_devanagari", "loanword_in_devanagari",
    "numbers_devanagari", "imperative_devanagari",
    "roman_hindi_with_english_loan", "homograph_hai_hi", "casual_roman_hindi",
    "roman_question", "roman_imperative",
    "mixed_script_hard", "mixed_script_grammar", "mixed_script_currency",
    "mixed_script_question",
    "english_with_indian_NE", "english_with_indian_names",
    "english_with_food_locality", "english_with_indian_brand",
}

REQUIRED_CATEGORY_COUNTS = {
    "pure_devanagari": 8,
    "pure_roman": 8,
    "mixed_script": 8,
    "english_with_NE": 6,
}


def _word_count(s: str) -> int:
    return len(s.split())


def main() -> int:
    rows = sorted(ANCHORS + GENERATED, key=lambda r: r[0])
    out = Path(__file__).resolve().parents[1] / "eval_sentences.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_NONE,
                       escapechar="\\", lineterminator="\n")
        w.writerow(HEADER)
        for r in rows:
            w.writerow(r)

    # ── §1.5 self-checks ─────────────────────────────────────────────
    problems: list[str] = []

    # 1. exactly 31 lines
    n_lines = sum(1 for _ in out.open(encoding="utf-8"))
    if n_lines != 31:
        problems.append(f"file has {n_lines} lines, expected 31")

    # 2. ids 01..30 unique
    ids = [r[0] for r in rows]
    expected_ids = [f"{i:02d}" for i in range(1, 31)]
    if ids != expected_ids:
        problems.append(f"id sequence wrong: got {ids}")

    # 3. category counts 8/8/8/6
    cat_counts = Counter(r[1] for r in rows)
    for cat, want in REQUIRED_CATEGORY_COUNTS.items():
        if cat_counts.get(cat, 0) != want:
            problems.append(f"category {cat}: have {cat_counts.get(cat,0)}, want {want}")
    extra = set(cat_counts) - set(REQUIRED_CATEGORY_COUNTS)
    if extra:
        problems.append(f"unknown categories: {extra}")

    # 4. every required phenomenon tag present
    seen_tags = {r[4] for r in rows}
    missing = REQUIRED_TAGS - seen_tags
    if missing:
        problems.append(f"missing phenomenon tags: {sorted(missing)}")
    unknown = seen_tags - REQUIRED_TAGS
    if unknown:
        problems.append(f"unknown phenomenon tags: {sorted(unknown)}")

    # length sanity (5–15 words)
    for r in rows:
        wc = _word_count(r[2])
        if not 5 <= wc <= 16:                 # +1 leniency for trailing punctuation
            problems.append(f"id {r[0]} word count {wc} outside 5–15: {r[2]!r}")

    # 5. print 5 random sentences for human sanity check
    rng = random.Random(20260507)
    sample = rng.sample(rows, 5)
    print("=== 5 random sentences (sanity-check the register) ===")
    for r in sample:
        print(f"  [{r[0]}] {r[1]:<16} {r[2]}")
    print()

    # category coverage of each phenomenon (informational)
    tag_counts = Counter(r[4] for r in rows)
    print("=== Phenomenon coverage ===")
    for tag in sorted(REQUIRED_TAGS):
        print(f"  {tag:<32} {tag_counts.get(tag, 0)}")
    print()

    print(f"=== Category counts ===  {dict(cat_counts)}")
    print(f"Wrote {out} ({n_lines} lines)")

    if problems:
        print("\nSELF-CHECK FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  • {p}", file=sys.stderr)
        return 1
    print("\nSELF-CHECK OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
