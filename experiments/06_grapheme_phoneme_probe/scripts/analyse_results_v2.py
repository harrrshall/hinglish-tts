"""Phase 4 analysis v2 — speech-onset-aligned, voiced-frames only, C0 excluded.

Fixes vs v1:
  - All cosine comparisons use C1–C12 (index 1:), never C0
  - Test A: mfcc_voiced_mean instead of mfcc_full_mean
  - Test B: mfcc_onset50ms_mean (first 50ms after silence removal)
  - Test C: mfcc_onset100ms_mean (first 100ms after silence removal)
  - A4/A5 sanity section with F0 + onset diagnostics

Run from repo root:
    ./venv-scoring/bin/python experiments/06_grapheme_phoneme_probe/scripts/analyse_results_v2.py
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

REPO = Path(__file__).resolve().parents[3]
DATA_PATH = REPO / "experiments/06_grapheme_phoneme_probe/acoustic_analysis_v2.json"
OUT_PATH  = REPO / "experiments/06_grapheme_phoneme_probe/scores/analysis_results_v2.json"
OUT_PATH.parent.mkdir(exist_ok=True)


def cosine(a: list, b: list) -> float:
    av, bv = np.array(a, dtype=float), np.array(b, dtype=float)
    denom = np.linalg.norm(av) * np.linalg.norm(bv)
    return float(av @ bv / denom) if denom > 1e-10 else 0.0


def vec(data: dict, key: str, feature: str, c0_excluded: bool = True) -> list | None:
    entry = data.get(key)
    if entry is None or "error" in entry:
        return None
    v = entry.get(feature)
    if v is None:
        return None
    return v[1:] if c0_excluded else v  # skip C0 (index 0)


# ── Test A ────────────────────────────────────────────────────────────────────

def analysis_A(data: dict) -> dict:
    pairs = [("A1_devanagari","A1_roman"), ("A2_devanagari","A2_roman"),
             ("A3_devanagari","A3_roman"), ("A4_devanagari","A4_roman"),
             ("A5_devanagari","A5_roman"), ("A6_devanagari","A6_roman"),
             ("A7_devanagari","A7_roman"), ("A8_devanagari","A8_roman")]

    pair_sims, pair_rows = [], []
    for dev_id, rom_id in pairs:
        vd = vec(data, dev_id, "mfcc_voiced_mean")
        vr = vec(data, rom_id, "mfcc_voiced_mean")
        s  = cosine(vd, vr) if (vd and vr) else None
        if s is not None:
            pair_sims.append(s)
        onset_dev = data[dev_id].get("speech_onset_ms", "?")
        onset_rom = data[rom_id].get("speech_onset_ms", "?")
        f0_dev    = data[dev_id].get("f0_mean", "?")
        f0_rom    = data[rom_id].get("f0_mean", "?")
        pair_rows.append({
            "pair":      dev_id.replace("_devanagari", ""),
            "sim_voiced":round(s, 4) if s is not None else None,
            "f0_dev":    round(f0_dev, 1) if isinstance(f0_dev, float) else f0_dev,
            "f0_rom":    round(f0_rom, 1) if isinstance(f0_rom, float) else f0_rom,
            "onset_dev_ms": onset_dev,
            "onset_rom_ms": onset_rom,
        })

    # Baseline: unrelated Devanagari pairs (voiced MFCC, C1-C12)
    deva_ids = [p[0] for p in pairs]
    baseline_sims = []
    for a, b in list(combinations(deva_ids, 2))[:8]:
        va = vec(data, a, "mfcc_voiced_mean")
        vb = vec(data, b, "mfcc_voiced_mean")
        if va and vb:
            baseline_sims.append(cosine(va, vb))

    mean_matched  = float(np.mean(pair_sims)) if pair_sims else None
    mean_baseline = float(np.mean(baseline_sims)) if baseline_sims else None
    delta = round(mean_matched - mean_baseline, 4) if (mean_matched and mean_baseline) else None

    if delta is None:
        interp = "INCONCLUSIVE"
    elif delta >= 0.15:
        interp = "PHONEME_MEDIATED — matched pairs exceed baseline by ≥0.15"
    elif delta >= 0.05:
        interp = "WEAK_SIGNAL — matched pairs exceed baseline by 0.05–0.15"
    else:
        interp = "GRAPHEME_BOUND — matched pairs not above baseline"

    return {"feature": "mfcc_voiced_mean C1-C12",
            "pairs": pair_rows,
            "mean_matched":  round(mean_matched, 4) if mean_matched else None,
            "mean_baseline": round(mean_baseline, 4) if mean_baseline else None,
            "delta":         delta,
            "interpretation": interp}


# ── Test B ────────────────────────────────────────────────────────────────────

def analysis_B(data: dict) -> dict:
    ids = [f"B{i}" for i in range(1, 9)]

    # Primary: mfcc_onset50ms_mean (first 50ms of speech, C1-C12)
    vecs50 = {k: vec(data, k, "mfcc_onset50ms_mean") for k in ids}
    avail50 = [k for k, v in vecs50.items() if v is not None]

    sims50, rows50 = [], []
    for a, b in combinations(avail50, 2):
        s = cosine(vecs50[a], vecs50[b])
        sims50.append(s)
        rows50.append({"pair": f"{a}_{b}", "sim_onset50ms": round(s, 4)})

    mean50 = float(np.mean(sims50)) if sims50 else None
    std50  = float(np.std(sims50))  if sims50 else None

    # Distribution check: report bimodal vs unimodal
    bimodal_check = None
    if sims50:
        high = sum(1 for s in sims50 if s > 0.5)
        low  = sum(1 for s in sims50 if s < 0.0)
        bimodal_check = {"n_high_gt05": high, "n_low_lt0": low,
                         "n_total": len(sims50), "is_bimodal": (high > 2 and low > 2)}

    # Per-clip onset diagnostics
    onset_rows = []
    for k in ids:
        e = data.get(k, {})
        onset_rows.append({
            "clip": k,
            "speech_onset_ms": e.get("speech_onset_ms"),
            "f0_mean": round(e.get("f0_mean", 0), 1),
            "onset50ms_available": vecs50.get(k) is not None,
        })

    if mean50 is None:
        interp = "INCONCLUSIVE — no valid onset vectors"
    elif bimodal_check and bimodal_check["is_bimodal"]:
        interp = "BIMODAL — onset feature still contaminated; distribution not unimodal"
    elif mean50 > 0.70:
        interp = "CONSISTENT_K — mean >0.70 (phoneme-consistent onset)"
    elif mean50 > 0.40:
        interp = "PARTIAL_CONSISTENCY — 0.40–0.70"
    else:
        interp = "NO_K_ABSTRACTION — mean <0.40 (grapheme-bound)"

    return {"feature": "mfcc_onset50ms_mean C1-C12 (after silence strip)",
            "pairs":        rows50,
            "mean_sim":     round(mean50, 4) if mean50 is not None else None,
            "std_sim":      round(std50, 4)  if std50  is not None else None,
            "n_available":  len(avail50),
            "bimodal_check": bimodal_check,
            "onset_diagnostics": onset_rows,
            "interpretation": interp}


# ── Test C ────────────────────────────────────────────────────────────────────

def analysis_C(data: dict) -> dict:
    ids = [f"C{i}" for i in range(1, 9)]

    # Primary: mfcc_onset100ms_mean (first 100ms of speech, C1-C12)
    vecs = {k: vec(data, k, "mfcc_onset100ms_mean") for k in ids}
    avail = [k for k, v in vecs.items() if v is not None]

    # Sanity: print first 4 coefficients for C1 and C4
    c1v = vecs.get("C1")
    c4v = vecs.get("C4")
    identity_check = None
    if c1v and c4v:
        diff = float(np.linalg.norm(np.array(c1v) - np.array(c4v)))
        identity_check = {
            "C1_C1_C12_first4": [round(x, 3) for x in c1v[:4]],
            "C4_C1_C12_first4": [round(x, 3) for x in c4v[:4]],
            "L2_distance":       round(diff, 4),
            "are_identical":     diff < 0.001,
        }

    pairwise_sims = {}
    for a, b in combinations(avail, 2):
        pairwise_sims[f"{a}_{b}"] = round(cosine(vecs[a], vecs[b]), 4)

    # Clustering
    cluster_result = {}
    if len(avail) >= 3:
        mat  = np.array([vecs[k] for k in avail], dtype=float)
        dist = pdist(mat, metric="cosine")
        Z    = linkage(dist, method="average")
        c2   = fcluster(Z, t=2, criterion="maxclust").tolist()
        c3   = fcluster(Z, t=3, criterion="maxclust").tolist()
        cluster_result = {
            "ids": avail,
            "2_clusters": dict(zip(avail, c2)),
            "3_clusters": dict(zip(avail, c3)),
        }
        hindi_deva = [k for k in avail if k in ("C1", "C5")]
        english    = [k for k in avail if k in ("C2", "C4", "C6")]
        roman      = [k for k in avail if k in ("C3", "C7")]

        def mean_within(g):
            if len(g) < 2: return None
            s = [cosine(vecs[a], vecs[b]) for a, b in combinations(g, 2)]
            return round(float(np.mean(s)), 4)

        def mean_between(g1, g2):
            if not g1 or not g2: return None
            s = [cosine(vecs[a], vecs[b]) for a in g1 for b in g2]
            return round(float(np.mean(s)), 4)

        cluster_result.update({
            "within_hindi_deva":     mean_within(hindi_deva),
            "within_english":        mean_within(english),
            "within_roman":          mean_within(roman),
            "between_hindi_english": mean_between(hindi_deva, english),
            "between_hindi_roman":   mean_between(hindi_deva, roman),
        })

    # Check if all sims are still 1.0 (degenerate)
    all_one = all(abs(v - 1.0) < 0.001 for v in pairwise_sims.values()) if pairwise_sims else False

    if all_one:
        interp = "DEGENERATE — all similarities still 1.0; onset100ms feature insufficient"
    elif cluster_result:
        wh  = cluster_result.get("within_hindi_deva")
        we  = cluster_result.get("within_english")
        bhe = cluster_result.get("between_hindi_english")
        two_c = cluster_result.get("2_clusters", {})
        if len(set(two_c.values())) == 1:
            interp = "LANGUAGE_AGNOSTIC — all clips in one cluster"
        elif (wh and bhe and we and wh > bhe and we > bhe):
            interp = "LANGUAGE_SPECIFIC — within-group > between-group similarity"
        else:
            interp = "MIXED_OR_UNCLEAR"
    else:
        interp = "INCONCLUSIVE"

    return {"feature": "mfcc_onset100ms_mean C1-C12 (after silence strip)",
            "identity_check":  identity_check,
            "pairwise_sims":   pairwise_sims,
            "clustering":      cluster_result,
            "all_sims_degenerate": all_one,
            "interpretation":  interp}


# ── A4/A5 sanity ──────────────────────────────────────────────────────────────

def sanity_A4_A5(data: dict) -> dict:
    rows = []
    for pair_id in ["A4", "A5"]:
        dev_id = f"{pair_id}_devanagari"
        rom_id = f"{pair_id}_roman"
        de = data.get(dev_id, {})
        ro = data.get(rom_id, {})
        vd = vec(data, dev_id, "mfcc_voiced_mean")
        vr = vec(data, rom_id, "mfcc_voiced_mean")
        rows.append({
            "pair":             pair_id,
            "sim_voiced_C1_12": round(cosine(vd, vr), 4) if (vd and vr) else None,
            "f0_dev":           round(de.get("f0_mean", 0), 1),
            "f0_rom":           round(ro.get("f0_mean", 0), 1),
            "onset_dev_ms":     de.get("speech_onset_ms"),
            "onset_rom_ms":     ro.get("speech_onset_ms"),
            "dur_dev_s":        de.get("duration_s"),
            "dur_rom_s":        ro.get("duration_s"),
            "voiced_dev":       de.get("voiced_frame_count"),
            "voiced_rom":       ro.get("voiced_frame_count"),
            "diagnosis": (
                "MODE_C_CONFIRMED: Roman f0≈93Hz (garbage attractor) "
                "vs Devanagari f0>150Hz (normal output). "
                "Low similarity is real, not artifact."
                if ro.get("f0_mean", 0) < 100 and de.get("f0_mean", 0) > 150
                else "AMBIGUOUS — check manually"
            ),
        })
    # Compare against A7/A8 which showed near-Devanagari F0 for Roman
    for pair_id in ["A7", "A8"]:
        dev_id = f"{pair_id}_devanagari"
        rom_id = f"{pair_id}_roman"
        de = data.get(dev_id, {})
        ro = data.get(rom_id, {})
        vd = vec(data, dev_id, "mfcc_voiced_mean")
        vr = vec(data, rom_id, "mfcc_voiced_mean")
        rows.append({
            "pair":             pair_id,
            "sim_voiced_C1_12": round(cosine(vd, vr), 4) if (vd and vr) else None,
            "f0_dev":           round(de.get("f0_mean", 0), 1),
            "f0_rom":           round(ro.get("f0_mean", 0), 1),
            "onset_dev_ms":     de.get("speech_onset_ms"),
            "onset_rom_ms":     ro.get("speech_onset_ms"),
            "dur_dev_s":        de.get("duration_s"),
            "dur_rom_s":        ro.get("duration_s"),
            "voiced_dev":       de.get("voiced_frame_count"),
            "voiced_rom":       ro.get("voiced_frame_count"),
            "diagnosis": "CONTROL: high-frequency Roman word; should show higher similarity",
        })
    return {"pairs": rows,
            "note": "A4/A5 are low-similarity because Roman inputs hit Mode-C (f0≈93Hz). "
                    "A7/A8 shown as controls (common romanized words, partial phoneme access)."}


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Run extract_acoustics_v2.py first: {DATA_PATH}")

    data = json.loads(DATA_PATH.read_text())
    print(f"Loaded {len(data)} entries from {DATA_PATH}\n")

    results = {}

    # ── Test A ────────────────────────────────────────────────────────────────
    print("=" * 65)
    print("TEST A — Cross-script homophone similarity (voiced MFCC, C1-C12)")
    print("=" * 65)
    results["test_A"] = analysis_A(data)
    A = results["test_A"]
    print(f"  Feature: {A['feature']}")
    for r in A["pairs"]:
        flag = ""
        if r["sim_voiced"] is not None:
            if r["sim_voiced"] < 0.6:
                flag = "  ← LOW"
            elif r["sim_voiced"] > 0.95:
                flag = "  ← HIGH"
        print(f"  {r['pair']}: sim={r['sim_voiced']}  "
              f"f0 dev={r['f0_dev']} rom={r['f0_rom']} Hz  "
              f"onset dev={r['onset_dev_ms']}ms rom={r['onset_rom_ms']}ms{flag}")
    print(f"\n  Mean matched:  {A['mean_matched']}")
    print(f"  Mean baseline: {A['mean_baseline']}")
    print(f"  Delta:         {A['delta']}")
    print(f"  >> {A['interpretation']}")

    # ── Test B ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("TEST B — /k/ onset consistency (onset-50ms MFCC, C1-C12)")
    print("=" * 65)
    results["test_B"] = analysis_B(data)
    B = results["test_B"]
    print(f"  Feature: {B['feature']}")
    print(f"  n_available: {B['n_available']}")
    print("\n  Onset diagnostics:")
    for r in B["onset_diagnostics"]:
        print(f"    {r['clip']}: onset={r['speech_onset_ms']}ms  "
              f"f0={r['f0_mean']}Hz  onset50ms_ok={r['onset50ms_available']}")
    print("\n  Pairwise sims (onset 50ms, C1-C12):")
    for r in B["pairs"]:
        flag = "  ← BETWEEN-GROUP" if r["sim_onset50ms"] < 0.0 else ""
        print(f"    {r['pair']}: {r['sim_onset50ms']}{flag}")
    bc = B["bimodal_check"]
    print(f"\n  Bimodal check: {bc}")
    print(f"  Mean: {B['mean_sim']}  Std: {B['std_sim']}")
    print(f"  >> {B['interpretation']}")

    # ── Test C ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("TEST C — Cross-language /k/ phoneme transfer (onset-100ms, C1-C12)")
    print("=" * 65)
    results["test_C"] = analysis_C(data)
    C = results["test_C"]
    print(f"  Feature: {C['feature']}")
    if C.get("identity_check"):
        ic = C["identity_check"]
        print(f"\n  Identity check C1 vs C4 (after silence strip, C1-C12):")
        print(f"    C1 first-4 coeffs: {ic['C1_C1_C12_first4']}")
        print(f"    C4 first-4 coeffs: {ic['C4_C1_C12_first4']}")
        print(f"    L2 distance: {ic['L2_distance']}  identical: {ic['are_identical']}")
    print(f"\n  All sims degenerate (=1.0): {C['all_sims_degenerate']}")
    print("\n  Pairwise sims:")
    for k, v in C["pairwise_sims"].items():
        print(f"    {k}: {v}")
    cl = C.get("clustering", {})
    if cl:
        print(f"\n  2-cluster assignment: {cl.get('2_clusters')}")
        print(f"  Within Hindi-Deva: {cl.get('within_hindi_deva')}")
        print(f"  Within English:    {cl.get('within_english')}")
        print(f"  Between Hindi/Eng: {cl.get('between_hindi_english')}")
    print(f"  >> {C['interpretation']}")

    # ── A4/A5 sanity ──────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("SANITY — A4/A5 outliers vs A7/A8 controls")
    print("=" * 65)
    results["sanity_A4_A5"] = sanity_A4_A5(data)
    S = results["sanity_A4_A5"]
    print(f"  {S['note']}\n")
    for r in S["pairs"]:
        print(f"  {r['pair']}: sim={r['sim_voiced_C1_12']}  "
              f"f0 dev={r['f0_dev']} rom={r['f0_rom']} Hz")
        print(f"       dur dev={r['dur_dev_s']}s rom={r['dur_rom_s']}s")
        print(f"       voiced dev={r['voiced_dev']} rom={r['voiced_rom']} frames")
        print(f"       {r['diagnosis']}")

    OUT_PATH.write_text(json.dumps(results, indent=2))
    print(f"\nWrote analysis → {OUT_PATH}")


if __name__ == "__main__":
    main()
