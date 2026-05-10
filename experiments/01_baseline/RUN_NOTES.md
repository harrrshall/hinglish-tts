# Run Notes

> Append as you go. Do not overwrite previous entries.
> The agent that runs the audit is responsible for keeping this honest.

## Install gotchas

- **2026-05-07, local laptop dry-run** — `pip install kokoro` died twice with
  `urllib3 ProtocolError: Connection broken: IncompleteRead(...)` while
  pulling the default torch wheel (~700 MB). On flaky networks: install
  CPU-only torch first via the pytorch.org CPU index, then kokoro:
    pip install --index-url https://download.pytorch.org/whl/cpu \
      --retries 20 --timeout 300 --no-cache-dir torch
    pip install "kokoro>=0.9.4" soundfile numpy
  On Colab T4 you'll want a CUDA wheel — this gotcha is local-only, but
  the `--retries 20 --timeout 300` survival flags help anywhere.
- **`prep_reference_audio.py` requires `datasets`** for the Rasa path
  and `soundfile` for the WAV verify. Both must be installed BEFORE the
  prep script runs:
    pip install datasets soundfile
- **IndicF5 GitHub `prompts/` directory has NO Hindi clips** (only KAN /
  MAR / PAN / TAM). My first prep script glob fell through and copied
  `KAN_F_HAPPY_00001.wav` as the "Hindi reference" — silently wrong.
  Fixed: prep script now tries Rasa Hindi → SPRINGLab/IndicTTS-Hindi →
  IndicF5 bundled (Hindi-only glob). If all three fail, exit 1 with a
  manual-fix recipe (record your own 3–8 s Hindi clip, ffmpeg-resample
  to 24 kHz mono, write the Devanagari transcript).
- **Rasa Hindi is HF-gated.** Without `HF_TOKEN` set + access accepted
  on the Hub page, `_rasa()` will always fail. SPRINGLab/IndicTTS-Hindi
  is the open fallback that consistently works (2026-05-07: pulled
  `सर=48000` 7-s clip about Kabir, transcript intact).
- **`SPRINGLab/IndicTTS-Hindi` decoder needs `torchcodec`** in current
  `datasets`. Install: `pip install torchcodec` (2.3 MB; no system deps
  beyond ffmpeg which is already on Colab).
- **Reference clip arrived at 48 kHz** from SPRINGLab/IndicTTS-Hindi but
  AUDIT_PLAN §2.2 wants 24 kHz. Prep script now auto-resamples to 24 kHz
  mono via librosa (auto-installs librosa if missing).
- **Cosmetic Python finalization warning** (`PyGILState_Release: thread
  state ... must be current when releasing`) prints AFTER `[prep] OK` —
  known torch+torchcodec finalizer race; the script's actual exit code
  is correct. Ignore the warning.

## Local CPU dry-run (2026-05-07, no GPU)

Ran `audit/scripts/debug_kokoro_cpu.py --limit 30` on this laptop's CPU
(Intel i3-1125G4, 15 GB RAM, no CUDA) to surface real failures before
the executing agent burns Colab time. **30/30 succeeded** in ~70 seconds
total wall clock. Diagnostic phoneme outputs written to
`audit/results/kokoro_cpufull/log.json`.

Notable phoneme-level findings (these are the audit's actual signal):

- **Hindi pipeline + Roman input → English-style fallback.** Anchor 10
  ("mera naam Arjun hai aur mai Bengaluru se hu") phonemizes "hai" as
  `hˈI` (English "high") — exactly the homograph failure the runbook
  warns about. Bengaluru becomes `bˈɛŋɡɐlˌʊəɹuː`, anglicized.
- **Mixed_script handling is partial.** Anchor 17 produces
  `kˈal mˈʌʤh ˈɔpʰɪs ɟˈaːnaː hˈI, bˌʌt ʈɾˈaːpʰɪk wɪl biː ɐn ˈɪʃuː.` —
  the script-switch mid-sentence renders, but "hai"→`hI` again.
- **English pipeline + Indian NEs → predictable mispronunciations.**
  "Khanna" → `kˈɑnə`, "Hyderabad" → `hˈIdəɹəbˌæd` (wrong stress),
  "Aishwarya" → `ˈAʃwɛɹiə`. These are the exact failure modes anchor
  24/25/26 are designed to expose.

These are the audit working as designed — Kokoro is reproducing every
predicted Hinglish failure mode. The actual scoring will happen when the
human listens to the wavs (the phonemes are diagnostic only).

## Per-model deviations from runbook

- **Kokoro:** Ran on local CPU (no GPU available locally). 30/30 OK in ~70s wall clock. `lang_code='h'` Hindi pipeline phonemized Roman input as English ("hai"→`hI`), exactly as predicted by the runbook.
- **IndicF5:** Required `transformers==4.49.0` + `accelerate==0.33.0` + `safetensors==0.4.3` to bypass meta-tensor error in Vocos init (verified via [HF discussion #16](https://huggingface.co/ai4bharat/IndicF5/discussions/16)). Final blocker on Kaggle was `UserSecretsClient` returning "Connection error trying to communicate with service" on all 3 retry attempts — token never reached the kernel and gated repo 401'd. Fix path: hardcode token via UI in a top cell, then Save & Run All (do NOT CLI-push afterward — that wipes the edit).
- **Indic Parler-TTS:** 30/30 OK on Kaggle T4 x2. Pinned `transformers==4.46.1` (newer breaks parler-tts). DESCRIPTION held constant: _"A female speaker delivers a clear, moderately-paced Hindi speech with neutral expression. The recording is high quality with no background noise."_
- **SPRINGLab F5:** State_dict architecture mismatch — checkpoint has 18 transformer blocks, SWivid upstream `f5-tts` defaults to 22. The rumourscape fork is the canonical match but `pip install -e <fork>` did not expose the `f5_tts` module. Deferred to Phase 2 pending fork's setup.py investigation.
- **Orpheus-Hindi:** HF gating still pending manual review by `Sachin@Telecmi.com` as of 2026-05-08. Deferred to Phase 2.

## Phase 1 outcome (2026-05-08, final)

Final score: **4 of 5 models complete (120 of 150 wavs)**.

| Model | Wavs | State |
|---|:---:|---|
| Kokoro v1.0 | 30/30 ✅ | DONE locally (CPU) |
| Indic Parler-TTS | 30/30 ✅ | DONE on Kaggle T4 x2 (v9) |
| IndicF5 | 30/30 ✅ | DONE on Kaggle T4 x2 (v12) — required hardcoded HF token fallback + GPU pre-flight check |
| SPRINGLab F5-Hindi | 30/30 ✅ | DONE on Kaggle T4 x2 (v3) — rumourscape fork + matplotlib + F5TTS_small_cfg + indic=True |
| Orpheus-Hindi | 0/30 ❌ | Gating pending external approval — Phase 2 |

### SPRINGLab fix (2026-05-08)

Earlier diagnosis ("rumourscape fork doesn't expose f5_tts") was wrong. Root cause was a missing `matplotlib` transitive dep — `f5_tts.infer.utils_infer` imports it at top level, so any submodule import fails until matplotlib is installed. The package itself was always installable (setuptools 61+ auto-discovers `src/<package>/` layouts).

Working v3 install + recipe:
```bash
pip install -q matplotlib tomli soundfile pydub
pip install -q git+https://github.com/rumourscape/F5-TTS.git
pip install -q 'numpy>=2.0,<2.1'
```
```python
from f5_tts.infer.utils_infer import load_model, load_vocoder, infer_process, preprocess_ref_audio_text
from f5_tts.model import DiT
F5TTS_small_model_cfg = dict(dim=768, depth=18, heads=12, ff_mult=2, text_dim=512, conv_layers=4)
ema_model = load_model(DiT, F5TTS_small_model_cfg, ckpt_path, vocab_file=vocab_path, device=device)
vocoder   = load_vocoder(vocoder_name="vocos", is_local=False, device=device)
ref_p, txt_p = preprocess_ref_audio_text(ref_audio, ref_text)
wave, sr, _ = infer_process(ref_p, txt_p, gen_text, ema_model, vocoder, indic=True)
```
~2.1 sec per sentence on T4 x2, 30/30 OK, 0 errors. SPRINGLab is CC-BY-4.0 (not gated), so no HF token required.

Bonus learning: `kernel-metadata.json` `machine_shape: "NvidiaTeslaT4"` IS settable via CLI push. No UI Settings → Accelerator step needed (corrects an earlier learning in this audit).

### IndicF5 retry timeline (2026-05-08)

- v8/v9/v10: Kaggle `UserSecretsClient` returned `Connection error trying to communicate with service` on all 3 retries → no HF_TOKEN → 401 GatedRepo. Known Kaggle bug.
- v11: User hardcoded HF token in cell; ran on default GPU **P100 (sm_60)** — Kaggle's pre-installed PyTorch lacks sm_60 kernels → all 30 sentences errored with `cudaErrorNoKernelImageForDevice`. Lesson: pre-flight check the kernel-level `machine_shape` via CLI metadata pull before Save Version.
- v12: GPU explicitly set to T4 x2 via Settings → Accelerator before Save Version. **30/30 OK.** Token injected via `os.environ.get("HF_TOKEN", "<token>")` default-arg fallback (one-character edit, no logic change).

## Eval-set decisions

- **Runbook §1.1 vs §1.3 inconsistency, resolved 2026-05-07.**
  §1.1 mandates 8/8/8/6 totals (= 30) but §1.3 lists 27–30 as the
  english_with_NE generated range, which would give 8/8/7/7. We honored the
  §1.1 contract: ID 27 is **mixed_script** (5 generated for that category:
  20, 21, 22, 23, 27) and english_with_NE generated IDs are 28, 29, 30
  (3 generated, 3 anchored). All 18 phenomenon tags from §1.4 are still
  covered ≥1×; see `audit/scripts/build_eval_set.py` self-check.

## Errors encountered (and resolution, if any)

- **Kaggle default GPU is P100 (sm_60), pre-installed PyTorch needs sm_70+.** Signal: `cudaErrorNoKernelImageForDevice`. Fix: switch each kernel to GPU T4 x2 in Settings → Accelerator (cannot be set via `kernel-metadata.json`). Cost: ~5–10 min per doomed P100 run before erroring.
- **`numpy._core.umath._center` ImportError** after TTS installs. Cause: parler-tts/IndicF5 pin numpy 1.26.4 during install, but pre-installed scipy expects 2.x. numpy 2.1+ removes `_center`. Fix: pin `numpy>=2.0,<2.1` in every install cell.
- **Kaggle `kernel-metadata.json` does not support secrets.** Open feature request Kaggle/kaggle-api#582. Secrets must be attached via the Kaggle UI (`Add-ons → Secrets`).
- **`UserSecretsClient` transient connection failure.** Known Kaggle bug (product feedback #467871, #467883). Built 3-retry logic into `HF_LOGIN_CELL`; still failed for IndicF5 v10. Fallback: hardcode token via UI cell, do NOT CLI-push afterward.
- **HF gating beyond token.** Token alone is insufficient; each gated repo requires a manual "Agree and access" click on `huggingface.co/<owner>/<model>`. ai4bharat auto-approves; Sachin@Telecmi requires manual review (Orpheus still pending).
- **CLI title-derived slug overrides metadata `id` mismatch.** First push warns and creates `<user>/<title-slug>`; subsequent pushes 409 Conflict unless metadata `id` is updated to the actual deployed slug.
- **Don't CLI push after user UI edits.** A CLI push overwrites the entire notebook including any hardcoded tokens. Once a kernel is in UI mode for a fix, switch off CLI for that kernel.
- **IndicF5 `RuntimeError: Tensor.item() cannot be called on meta tensors`** during Vocos init. Cause: newer `transformers` defaults to meta-init for `trust_remote_code=True` models. Fix (verified): pin `transformers==4.49.0`, `accelerate==0.33.0`, `safetensors==0.4.3`. Source: HF discussion #16. Wrong fix attempted earlier: `with torch.device("cpu"):` does not help — bug is in custom code path, not device init.
- **SPRINGLab F5-Hindi state_dict mismatch.** SWivid upstream has 22 transformer blocks; SPRINGLab checkpoint has 18. Need rumourscape fork; pip install of the fork did not expose `f5_tts` module — root cause needs Phase 2 investigation.
- **`torchaudio==2.6.0 --index-url cu121` wheel missing.** Removed pin; Kaggle's pre-installed torchaudio works fine.

## Times

- Eval-set generation: ~5 min (already locked in `eval_sentences.tsv`)
- Reference-audio prep: ~3 min (auto-resampled 48 kHz → 24 kHz from SPRINGLab/IndicTTS-Hindi)
- Notebook 1 (Kokoro): ~70 s on local CPU (no GPU); 30/30 OK
- Notebook 2 (IndicF5): unfinished — burned ~v1–v10 (≈ 60+ min combined) on Kaggle; final blocker is UserSecretsClient bug
- Notebook 3 (Indic Parler-TTS): ~17 min on Kaggle T4 x2 (v9, after switch from P100); 30/30 OK
- Notebook 4 (SPRINGLab F5-Hindi): blocked at v2 (~10 min); deferred
- Notebook 5 (Orpheus-Hindi): blocked pre-run on gating; deferred

## Sanity-check summary

- Total audio files: 120 / 150 expected (80%) — Phase 1 final
- Zero-byte files: 0 (Kokoro 30/30, Parler 30/30, IndicF5 30/30, SPRINGLab 30/30 all non-empty)
- Missing logs: 1 (orpheus_hi — gating still pending external approval)
- `verify.py` exits 1 (expected): orpheus_hi dir is empty by design — the deliverable is Kokoro + Parler + IndicF5 + SPRINGLab.
