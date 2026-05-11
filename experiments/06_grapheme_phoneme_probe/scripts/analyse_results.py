"""Phase 4 analysis — per-test MFCC similarity + clustering.

Run from repo root after extract_acoustics.py:
    ./venv-scoring/bin/python experiments/06_grapheme_phoneme_probe/scripts/analyse_results.py

Writes:
    experiments/06_grapheme_phoneme_probe/scores/analysis_results.json
    (human-readable summary also printed to stdout)
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

REPO = Path(__file__).resolve().parents[3]
DATA_PATH = REPO / "experiments/06_grapheme_phoneme_probe/acoustic_analysis.json"
OUT_PATH  = REPO / "experiments/06_grapheme_phoneme_probe/scores/analysis_results.json"
OUT_PATH.parent.mkdir(exist_ok=True)


def cosine(a: list, b: list) -> float:
    av, bv = np.array(a, dtype=float), np.array(b, dtype=float)
    denom = np.linalg.norm(av) * np.linalg.norm(bv)
    return float(av @ bv / denom) if denom > 1e-10 else 0.0


def safe_vec(data: dict, key: str, feature: str) -> list | None:
    entry = data.get(key)
    if entry is None or "error" in entry:
        return None
    return entry.get(feature)


def analysis_A(data: dict) -> dict:
    pairs = [("A1_devanagari","A1_roman"),("A2_devanagari","A2_roman"),
             ("A3_devanagari","A3_roman"),("A4_devanagari","A4_roman"),
             ("A5_devanagari","A5_roman"),("A6_devanagari","A6_roman"),
             ("A7_devanagari","A7_roman"),("A8_devanagari","A8_roman")]

    pair_sims_full, pair_sims_200ms = [], []
    pair_rows = []
    for dev_id, rom_id in pairs:
        vd_full  = safe_vec(data, dev_id, "mfcc_full_mean")
        vr_full  = safe_vec(data, rom_id, "mfcc_full_mean")
        vd_200   = safe_vec(data, dev_id, "mfcc_200ms_mean")
        vr_200   = safe_vec(data, rom_id, "mfcc_200ms_mean")
        sim_full = cosine(vd_full, vr_full) if vd_full and vr_full else None
        sim_200  = cosine(vd_200, vr_200)   if vd_200 and vr_200   else None
        if sim_full is not None: pair_sims_full.append(sim_full)
        if sim_200  is not None: pair_sims_200ms.append(sim_200)
        pair_rows.append({"pair": dev_id.replace("_devanagari",""),
                          "sim_full": round(sim_full, 4) if sim_full is not None else None,
                          "sim_200ms": round(sim_200, 4) if sim_200 is not None else None})

    # Baseline: unrelated Devanagari pairs
    deva_ids = [p[0] for p in pairs]
    baseline_sims = []
    for a, b in list(combinations(deva_ids, 2))[:8]:
        va = safe_vec(data, a, "mfcc_full_mean")
        vb = safe_vec(data, b, "mfcc_full_mean")
        if va and vb:
            baseline_sims.append(cosine(va, vb))

    mean_matched  = float(np.mean(pair_sims_full))  if pair_sims_full  else None
    mean_baseline = float(np.mean(baseline_sims))    if baseline_sims   else None
    delta = round(mean_matched - mean_baseline, 4) if (mean_matched is not None
                                                        and mean_baseline is not None) else None

    interpretation = "INCONCLUSIVE"
    if delta is not None:
        if delta >= 0.15:
            interpretation = "PHONEME_MEDIATED — matched pairs above baseline by ≥0.15"
        elif delta >= 0.05:
            interpretation = "WEAK_SIGNAL — matched pairs above baseline 0.05–0.15"
        else:
            interpretation = "GRAPHEME_BOUND — matched pairs not above baseline"

    return {"pairs": pair_rows,
            "mean_matched_sim_full":  round(mean_matched, 4) if mean_matched is not None else None,
            "mean_baseline_sim_full": round(mean_baseline, 4) if mean_baseline is not None else None,
            "delta":                  delta,
            "interpretation":         interpretation}


def analysis_B(data: dict) -> dict:
    ids = [f"B{i}" for i in range(1, 9)]
    vecs = {k: safe_vec(data, k, "mfcc_50ms_mean") for k in ids}
    available = [k for k, v in vecs.items() if v is not None]

    sims = []
    rows = []
    for a, b in combinations(available, 2):
        s = cosine(vecs[a], vecs[b])
        sims.append(s)
        rows.append({"pair": f"{a}_{b}", "sim_50ms": round(s, 4)})

    mean_sim = float(np.mean(sims)) if sims else None
    std_sim  = float(np.std(sims))  if sims else None

    interpretation = "INCONCLUSIVE"
    if mean_sim is not None:
        if mean_sim > 0.70:
            interpretation = "CONSISTENT_K_PHONEME — mean >0.70, strong phoneme representation"
        elif mean_sim > 0.40:
            interpretation = "PARTIAL_K_CONSISTENCY — 0.40–0.70, coarticulation dominates"
        else:
            interpretation = "NO_K_ABSTRACTION — mean <0.40, grapheme-bound"

    return {"pairs": rows,
            "mean_sim_50ms": round(mean_sim, 4) if mean_sim is not None else None,
            "std_sim_50ms":  round(std_sim, 4)  if std_sim  is not None else None,
            "n_available":   len(available),
            "interpretation": interpretation}


def analysis_C(data: dict) -> dict:
    ids = [f"C{i}" for i in range(1, 9)]
    vecs_raw = {k: safe_vec(data, k, "mfcc_50ms_mean") for k in ids}
    available = [k for k, v in vecs_raw.items() if v is not None]
    vecs = {k: vecs_raw[k] for k in available}

    pairwise_sims = {}
    for a, b in combinations(available, 2):
        pairwise_sims[f"{a}_{b}"] = round(cosine(vecs[a], vecs[b]), 4)

    cluster_result = {}
    if len(available) >= 3:
        mat = np.array([vecs[k] for k in available], dtype=float)
        dist = pdist(mat, metric="cosine")
        Z = linkage(dist, method="average")
        c2 = fcluster(Z, t=2, criterion="maxclust").tolist()
        c3 = fcluster(Z, t=3, criterion="maxclust").tolist()
        cluster_result = {
            "ids": available,
            "2_clusters": dict(zip(available, c2)),
            "3_clusters": dict(zip(available, c3)),
        }
        # Check if Hindi-context (C1,C5) vs English-context (C2,C4,C6) vs Roman (C3,C7) cluster
        hindi_deva = [k for k in available if k in ("C1","C5")]
        english    = [k for k in available if k in ("C2","C4","C6")]
        roman      = [k for k in available if k in ("C3","C7")]

        def mean_within(group):
            if len(group) < 2: return None
            s = [cosine(vecs[a], vecs[b]) for a, b in combinations(group, 2)]
            return round(float(np.mean(s)), 4)

        def mean_between(g1, g2):
            if not g1 or not g2: return None
            s = [cosine(vecs[a], vecs[b]) for a in g1 for b in g2]
            return round(float(np.mean(s)), 4)

        cluster_result["within_hindi_deva"]  = mean_within(hindi_deva)
        cluster_result["within_english"]     = mean_within(english)
        cluster_result["within_roman"]       = mean_within(roman)
        cluster_result["between_hindi_english"] = mean_between(hindi_deva, english)
        cluster_result["between_hindi_roman"]   = mean_between(hindi_deva, roman)

    interpretation = "INCONCLUSIVE"
    if cluster_result:
        wh = cluster_result.get("within_hindi_deva")
        we = cluster_result.get("within_english")
        bhe = cluster_result.get("between_hindi_english")
        two_c = cluster_result.get("2_clusters", {})
        unique_clusters = set(two_c.values())
        if len(unique_clusters) == 1:
            interpretation = "LANGUAGE_AGNOSTIC — all in one cluster"
        elif (wh is not None and bhe is not None and
              we is not None and wh > bhe and we > bhe):
            interpretation = "LANGUAGE_SPECIFIC — within-group sim > between-group sim"
        else:
            interpretation = "MIXED_OR_UNCLEAR"

    return {"pairwise_sims": pairwise_sims,
            "clustering":     cluster_result,
            "interpretation": interpretation}


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Run extract_acoustics.py first: {DATA_PATH}")

    data = json.loads(DATA_PATH.read_text())
    print(f"Loaded {len(data)} entries from {DATA_PATH}\n")

    results = {}

    print("=" * 60)
    print("TEST A — Cross-script homophone similarity")
    print("=" * 60)
    results["test_A"] = analysis_A(data)
    A = results["test_A"]
    for r in A["pairs"]:
        print(f"  {r['pair']}: full={r['sim_full']}  200ms={r['sim_200ms']}")
    print(f"\n  Mean matched sim (full MFCC): {A['mean_matched_sim_full']}")
    print(f"  Mean baseline sim (full MFCC): {A['mean_baseline_sim_full']}")
    print(f"  Delta: {A['delta']}")
    print(f"  >> {A['interpretation']}")

    print("\n" + "=" * 60)
    print("TEST B — /k/ onset consistency within Hindi")
    print("=" * 60)
    results["test_B"] = analysis_B(data)
    B = results["test_B"]
    for r in B["pairs"]:
        print(f"  {r['pair']}: {r['sim_50ms']}")
    print(f"\n  Mean /k/-onset sim (50ms MFCC): {B['mean_sim_50ms']} ± {B['std_sim_50ms']}")
    print(f"  >> {B['interpretation']}")

    print("\n" + "=" * 60)
    print("TEST C — Cross-language /k/ phoneme transfer")
    print("=" * 60)
    results["test_C"] = analysis_C(data)
    C = results["test_C"]
    print("  Pairwise sims:")
    for pair, s in C["pairwise_sims"].items():
        print(f"    {pair}: {s}")
    if C["clustering"]:
        cl = C["clustering"]
        print(f"\n  2-cluster assignment: {cl.get('2_clusters')}")
        print(f"  Within Hindi-Deva: {cl.get('within_hindi_deva')}")
        print(f"  Within English:    {cl.get('within_english')}")
        print(f"  Between Hindi/Eng: {cl.get('between_hindi_english')}")
    print(f"  >> {C['interpretation']}")

    OUT_PATH.write_text(json.dumps(results, indent=2))
    print(f"\nWrote analysis → {OUT_PATH}")


if __name__ == "__main__":
    main()
