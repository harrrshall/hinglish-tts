# Phase 1 Audit — Session Report (2026-05-07)

## Status snapshot at session end

| Model | Wavs | State | Notes |
|---|:---:|---|---|
| Kokoro v1.0 | 30/30 ✅ | DONE locally (CPU) | `audit/results/kokoro/` |
| Indic Parler-TTS | 30/30 ✅ | DONE on Kaggle T4 x2 (v9) | `audit/results/indic_parler/` |
| IndicF5 | 0/30 ❌ | Blocked on Kaggle Secrets bug | UserSecretsClient `Connection error` x3; fix is one UI edit (hardcode token + Save & Run All — no CLI push after) |
| SPRINGLab F5-Hindi | 0/30 ❌ | BLOCKED — Phase 2 | State_dict mismatch (18 vs 22 transformer blocks); rumourscape fork needs investigation |
| Orpheus-Hindi | 0/30 ❌ | BLOCKED — Phase 2 | HF gating pending `Sachin@Telecmi.com` |

**Phase 1 actual outcome (2026-05-08):** 2 of 5 models = 60 of 150 wavs. Best-case after IndicF5 unblocks: 3 of 5 = 90 wavs.

## What got built

- `/tmp/build_kaggle_kernels.py` — generates 4 Kaggle kernel directories at `/tmp/kaggle-kernels/` (02_indicf5, 03_parler, 04_springlab, 05_orpheus). Re-runnable. Embeds `SETUP_CELL` (rglob-based file finder) and `HF_LOGIN_CELL` (UserSecretsClient + env-var fallback).
- Kaggle dataset `harshalsinghcn/hinglish-tts-audit-eval` (eval_sentences.tsv + hindi_ref.{wav,txt}). Files mount at `/kaggle/input/datasets/harshalsinghcn/hinglish-tts-audit-eval/`.
- 4 Kaggle kernels created: `hinglish-tts-audit-indicf5`, `hinglish-tts-audit-parler`, `hin-springlab-f5-hindi-tts`, `hin-orpheus-hindi-tts`.
- `/home/cybernovas/kaggle-env/` venv with `kaggle` CLI 2.1.2.

## What's still TODO

1. ✅ Parler v9 → 30/30, copied to `audit/results/indic_parler/`.
2. ✅ Kokoro confirmed 30/30 in `audit/results/kokoro/`.
3. ✅ `audit/METADATA.json` filled (success counts, ref source, Parler DESCRIPTION prompt).
4. ✅ `audit/scripts/verify.py` ran — exits 1 by design (3 model dirs empty).
5. ✅ `audit/RUN_NOTES.md` updated with per-model deviations + errors + sanity-check.
6. ✅ `audit/scripts/build_handoff.py` ran → `audit/HANDOFF.md` written.
7. ✅ Zip artifact: `audit_phase1_20260508.zip` (12 MB at repo root).
8. ⏸️ IndicF5 — needs user UI edit: open kernel, add `os.environ["HF_TOKEN"] = "<token>"` near top, Save Version → Save & Run All. Do NOT CLI-push afterward.
9. ⏳ **Phase 2:** SPRINGLab F5-Hindi (rumourscape fork investigation), Orpheus-Hindi (gating wait).

## Iteration count by model (versions burned)

- IndicF5: v1 (slug mismatch) → v2 (dataset path) → v3 (numpy>=2.0) → v4 (HF_TOKEN attempt) → v5 (numpy<2.2) → v6 (numpy<2.1) → v7 (UserSecrets worked, P100 GPU error) → **v8 (T4 x2, running)**
- Parler: v1-v6 same iterations → v7 (HF token user-saved) → v8 (P100 fail) → **v9 (T4 x2, running)**
- SPRINGLab: v1 (rumourscape fork, no f5_tts) → v2 (SWivid upstream, state_dict mismatch). Blocked.
- Orpheus: v1 (gating). Blocked.
