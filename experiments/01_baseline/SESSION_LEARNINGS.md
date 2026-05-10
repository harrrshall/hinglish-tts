# Operational Learnings — Kaggle TTS Audit Pipeline

For next session: read this first to skip ~2 hours of debugging cycles.

---

## Kaggle GPU & Environment

### 1. Default GPU is P100 (sm_60), but PyTorch needs sm_70+
**Signal:** `cudaErrorNoKernelImageForDevice` or `Tesla P100-PCIE-16GB with CUDA capability sm_60 is not compatible`.
**Fix:** Always switch to **GPU T4 x2** in `Settings → Accelerator` (not in `kernel-metadata.json` — that field doesn't exist). T4 x2 is also faster for TTS than a single P100.
**Cost:** Each P100 run wasted ~5-10 min before erroring.

### 2. numpy must pin to `>=2.0,<2.1` (not <2.2)
**Why:** TTS packages (parler-tts, IndicF5) downgrade numpy to 1.26.4 during `pip install`. Pre-installed scipy expects numpy 2.x. **But numpy 2.1+ removes `_center` from `numpy._core.umath`**, breaking scipy's array_api_compat.
**Fix:** After every TTS install, add `!pip install -q 'numpy>=2.0,<2.1'`. The version 2.0.2 lands and works.
**Signal of wrong pin:** `ImportError: cannot import name '_center' from 'numpy._core.umath'`.

### 3. Dataset mount path uses `datasets/` subdirectory
**Files mount at:** `/kaggle/input/datasets/<user>/<dataset>/...` not `/kaggle/input/<dataset>/`.
**Fix:** Use `Path("/kaggle/input").rglob(name)` to find files regardless of mount path.

---

## Kaggle Secrets & HF Auth

### 4. CLI push CANNOT attach secrets
The `kernel-metadata.json` schema has no `secrets` field (Kaggle/kaggle-api#582 open feature request). Secrets must be attached via UI. Across CLI pushes, secret bindings sometimes don't persist.
**Workaround:** UI `Save & Run All` after attaching the secret commits a real version with binding. Subsequent CLI pushes inherit.
**Fallback:** Embed token in HF_LOGIN_CELL with env-var fallback (`os.environ.get("HF_TOKEN", "")`) so user can hardcode if needed.

### 5. `UserSecretsClient` connection error is a known transient bug
`Connection error trying to communicate with service` (Kaggle product feedback #467871, #467883). The same kernel may work on next run. Don't blame your code — retry first.

### 6. HF gated repos require manual gating accept
Token alone isn't enough. Visit each model page, click "Agree and access repository". Check status at `huggingface.co/settings/gated-repos` — should show "accepted" not "pending".
**Approval lag varies:** ai4bharat models auto-approve; SachinTelecmi/Orpheus-tts-hi requires manual review by `Sachin@Telecmi.com` (still pending after 1+ session).

### 7. HF tokens page requires password re-prompt to view
Even when logged in, viewing `/settings/tokens` triggers a security checkup. Cannot be auto-driven; user types password manually. After confirm, HF only shows full token at creation time — existing tokens are truncated (`hf_…EDqK`).

---

## Kernel ID & Slug Behavior

### 8. CLI title-derived slug overrides `id` mismatch
If `kernel-metadata.json` has `"id": "user/foo"` but title would slug to "user/foo-bar", Kaggle creates `user/foo-bar` and warns. After first push, **update metadata `id` to match the actual deployed slug** for future pushes (or get 409 Conflict).
**Actual slugs from this project:**
- `harshalsinghcn/hinglish-tts-audit-indicf5`
- `harshalsinghcn/hinglish-tts-audit-parler`
- `harshalsinghcn/hin-springlab-f5-hindi-tts`
- `harshalsinghcn/hin-orpheus-hindi-tts`

### 9. Don't CLI push after user UI edits
A CLI push overwrites the notebook code, including any hardcoded tokens or manual cell edits the user added. Once user is in UI mode, stop CLI pushes for that kernel.

---

## TTS Model Specifics

### 10. SPRINGLab F5-Hindi-24KHz needs the rumourscape F5-TTS fork
SWivid upstream F5-TTS has 22 transformer blocks; SPRINGLab checkpoint has 18. Loading mismatched: `Missing key(s) in state_dict: transformer.transformer_blocks.18...`.
**Need to investigate:** Why `pip install -e /tmp/f5_hi` (rumourscape) doesn't expose `f5_tts` as importable module. Check the fork's `pyproject.toml`/`setup.py`.

### 11a. IndicF5 needs `transformers==4.49.0` (verified via HF community)
**Symptom:** `RuntimeError: Tensor.item() cannot be called on meta tensors` during model load (Vocos init).
**Cause:** Newer transformers (5.x+) defaults to meta-init for `trust_remote_code=True` models; IndicF5's custom code can't materialize meta tensors via `.to(device)`.
**Fix (verified):** Pin `transformers==4.49.0`, `accelerate==0.33.0`, `safetensors==0.4.3` in install cell. Source: [HF discussion #16](https://huggingface.co/ai4bharat/IndicF5/discussions/16). Affects MANY users — not just our setup.
**Wrong fix attempted:** `with torch.device("cpu"):` doesn't help. The bug is in the model's custom code path, not the device init.

### 11. Orpheus-Hindi has gated start_of_speech_token (128257)
Not in the original notebook stub. The HF model card has the verbatim `generate_speech` function — copy exactly. Token boundary tokens (128258-128262) are documented; AUDIO_CODE_BASE_OFFSET is 128266.

### 12. Indic Parler-TTS requirements
- `transformers==4.46.1` (newer breaks parler-tts)
- Don't pin `torchaudio==2.6.0 --index-url cu121` — that wheel doesn't exist. Use whatever Kaggle pre-installed.
- DESCRIPTION prompt must be constant across all 30 sentences (per AGENT.md).

---

## Browser Automation Patterns That Worked

### 13. Settings → Accelerator submenu requires hover, not click
Clicking "Accelerator" closes the menu. Use `computer` action `hover` to expand the submenu, then click the option.

### 14. Add-ons → Secrets to attach token to a specific kernel
Path: top toolbar `Add-ons` → click `Secrets` (top option) → `Add secret` → paste label + value. The HF_TOKEN secret saved in one kernel propagates to user account level — visible (with checkbox) when opening Secrets panel in other kernels.

### 15. Save Version button (top right) opens commit modal
Default type: "Save & Run All (Commit)". Click `Save` → version increments and starts running. Active Events panel (bottom-left) shows "Running: just now" with version number and GPU type.

---

## Patterns to Avoid Next Session

- ❌ Don't rely on `os.environ.get("HF_TOKEN")` alone — Kaggle doesn't expose secrets as env vars. Use `from kaggle_secrets import UserSecretsClient`.
- ❌ Don't push CLI version after user clicks Save Version in UI — overwrites their edits.
- ❌ Don't push v3+ in rapid succession on a flaky issue — wait for one to complete and check log first.
- ❌ Don't trust the "Successful" label in Active Events — means "completed without crash", not "produced wavs". Always check `log.json` for OK count.

---

## Session 2026-05-08 additions

### 16. **Pre-Save-Version checklist (mandatory)**
Before clicking Save Version → Save & Run All on any TTS kernel, verify all of:
1. **GPU setting:** `kaggle kernels pull <slug> -p /tmp/x -m && cat /tmp/x/kernel-metadata.json | grep machine_shape` — must be `"NvidiaTeslaT4"` not `"NvidiaTeslaP100"`. **The Settings → Accelerator change in editor mode does NOT auto-persist to the kernel-level GPU setting.** Cost of skipping: v11 ran on P100, hit cudaErrorNoKernelImageForDevice 30/30, wasted ~5 min + quota.
2. **`is_private: true`** if any token is hardcoded in source. Kaggle kernels are PUBLIC by default. Verify before pasting any secret.
3. **Active Events panel** shows correct GPU on the version that's about to run. Look for "Version #N with GPU T4 x2" — if it says P100, the kernel-level setting wasn't updated.

### 17. **"Successful" in Active Events ≠ produced wavs (re-confirmed)**
v11 was labeled "Successful" but log.json had 0/30 OK (all `cudaErrorNoKernelImageForDevice`). Kaggle's "Successful" only means the notebook didn't crash with an unhandled exception at notebook level — our per-sentence try/except caught all 30 errors and the notebook exited 0. **Always read log.json directly.**

### 18. **Switching GPU on a running kernel kills the session**
When you change Settings → Accelerator on a running kernel, Kaggle stops the active session immediately ("Session stopped" toast). Useful: lets you abort a doomed P100 run without waiting. Caveat: any in-flight cell state is lost.

### 19. **Kaggle notebook editor cells are virtualized — DOM queries don't reach cell content**
Monaco/CodeMirror renders cells via canvas; `document.querySelectorAll` won't find `hf_token` strings. To navigate to a specific cell:
- Click the **Edit menu** in the toolbar — the act of opening Edit *side-effects scroll* the focused cell into view (this is how I finally found the HF login cell after 15 min of failed scroll attempts).
- Or click a visible cell prompt `[ ]:` indicator + use J/K (next/prev) keyboard shortcuts in command mode (Esc first).
- Window-level scroll, programmatic `scrollTo`, and CodeMirror text-content searches all fail.

### 20. **HF token creation flow (when user is already logged in)**
- `/settings/tokens` may auto-redirect to `/settings/tokens/new?tokenType=fineGrained` if a session-level token-creation intent is set — that's NOT a password reprompt, just the UI assuming you want to make a new one. Click "Return" link to see the existing tokens list.
- Token modal at creation shows full `hf_...` value with a **Copy** button — value is only visible THIS one time. Click Copy immediately, do not close the modal.
- Existing tokens in the list show truncated values (`hf_...elKq`); only the creation modal shows full value.
- For TTS gated-repo downloads: **Read preset** is sufficient. Don't pick Fine-grained unless you need scoped access — Read works for ai4bharat/* and gated repos with `huggingface.co/<repo>` access accepted.

### 21. **Cleanest hardcode point in HF_LOGIN_CELL**
Don't replace or rewrite the cell. The line `hf_token = os.environ.get("HF_TOKEN", "")` has a string default (the third argument). Replace `""` with `"hf_<your_token>"`. Pros: 1-character edit, the `os.environ.get` fallback path activates only if UserSecretsClient fails (which it does, currently), so the hardcoded value gets used. The login still works through the existing pipeline.

### 22. **Kaggle CLI metadata pull preserves source code state**
`kaggle kernels pull <slug> -p <dir>` downloads the latest committed notebook source. Use this to verify what was actually pushed/saved without trusting the editor view. v11's source as pulled showed the hardcoded token line correctly — so I knew the user's paste landed in the right place.

### 23. **Don't act on cached learnings without re-verifying the symptom**
User feedback (saved as `feedback_verify_dont_assume.md`): even though the existing learnings doc said "P100 sm_60 not compatible with Kaggle PyTorch", I should have pulled v11's actual log.json to confirm the failure mode before stopping the run and switching GPU. Verifying took 30 seconds and would have made my action explainable to the user. The cached belief was right, but acting on it without verification undermines trust.

### 24. **SPRINGLab F5-Hindi unblock recipe (verified 2026-05-08)**

The "rumourscape fork doesn't expose `f5_tts` module" failure in v1 was **misdiagnosed**. Root cause was a missing `matplotlib` dependency that `f5_tts.infer.utils_infer` imports at top-level. The package WAS installed correctly (setuptools 61+ auto-discovers `src/<package>/` layouts even without explicit `[tool.setuptools.packages.find]` in pyproject.toml).

**Working install path (verified by local venv test, then pushed to Kaggle as v3):**
```bash
pip install -q matplotlib tomli soundfile pydub
pip install -q git+https://github.com/rumourscape/F5-TTS.git
pip install -q 'numpy>=2.0,<2.1'
```

**Working inference recipe:**
```python
from f5_tts.infer.utils_infer import load_model, load_vocoder, infer_process, preprocess_ref_audio_text
from f5_tts.model import DiT

# Verified from rumourscape src/f5_tts/infer/infer_cli.py:160 and infer_gradio.py:53
F5TTS_small_model_cfg = dict(dim=768, depth=18, heads=12, ff_mult=2, text_dim=512, conv_layers=4)
ema_model = load_model(DiT, F5TTS_small_model_cfg, ckpt_path, vocab_file=vocab_path, device=device)
vocoder  = load_vocoder(vocoder_name="vocos", is_local=False, device=device)

# Run preprocess_ref_audio_text ONCE before the loop — does silence-trim + transcript fix
ref_audio_p, ref_text_p = preprocess_ref_audio_text(ref_audio, ref_text)
for sentence in sentences:
    wave, sr, _ = infer_process(ref_audio_p, ref_text_p, sentence, ema_model, vocoder, indic=True)
```

Key facts:
- The rumourscape fork is the canonical match: it has `F5TTS_small_model_cfg` baked in (matches SPRINGLab's depth=18 architecture) AND adds an `indic=True` flag to `infer_process` for Hindi text handling. SWivid upstream lacks both.
- SPRINGLab/F5-Hindi-24KHz is **CC-BY-4.0, NOT gated**. `hf_hub_download(repo_id="SPRINGLab/F5-Hindi-24KHz", filename="model_2500000.safetensors")` works without HF token. (The vocos vocoder is also public.) Skip the entire HF-token dance for this kernel.
- `infer_process` returns `(wave, sample_rate, combined_spectrogram)`. wave is a numpy array.

### 25. **`kernel-metadata.json` `machine_shape` is settable via CLI (contra prior belief)**

Set `"machine_shape": "NvidiaTeslaT4"` in metadata.json before `kaggle kernels push` — the CLI accepts it, the kernel launches on T4. Verified 2026-05-08 with SPRINGLab v3 push: metadata went in as T4, status went RUNNING on T4, no UI Settings → Accelerator step needed.

This was previously believed to require UI-only configuration (per item #1 in this doc) — that belief is incorrect or outdated. Saves a manual UI step per kernel and prevents the v11-style P100-by-default disaster on first push.

**However:** if the kernel was previously committed via UI with a different GPU, the kernel-level setting from the last UI Save may persist and override CLI metadata. Always run the pre-flight check after push:
```bash
kaggle kernels pull <slug> -p /tmp/x -m
grep machine_shape /tmp/x/kernel-metadata.json
```
to confirm the value Kaggle actually persisted.

### 26. **Triage: "module not found after pip install" — 30s verification beats 30min guessing**

Before assuming a packaging bug:
1. `import <package>` — does it return a module object?
2. Try a real submodule (e.g. `from <package>.<sub> import <symbol>`) — does the actual ImportError name a transitive dep?
3. `<package>.__file__` — None means namespace package only (real packaging issue); a real path means the package is fine.

In v1 of SPRINGLab kernel, step 2 would have shown `ModuleNotFoundError: matplotlib`, not anything about `f5_tts`. The fix would have been one extra pip install line, not switching forks/architectures.

### 27. **AssemblyAI > local Whisper for short-clip multilingual ASR (verified 2026-05-08)**

For 120 short Hindi clips (~3s each), AssemblyAI Universal-2 ran in 7 min with 5 parallel workers and cost ~$0.05 total. Local CPU faster-whisper-large-v3 was projected at 45+ min and required a 3GB model download that repeatedly failed on this network. Universal-2 supports Hindi + Hinglish code-switching natively, no fine-tune needed.

**Operational rules:**
- Read API key from `os.environ.get("ASSEMBLYAI_API_KEY")` ONLY. Never write to a script file. Document the env-var requirement in the script's docstring.
- Free tier queues over-concurrency requests instead of rejecting; 5 workers worked fine. 10+ likely also OK but untested.
- Each request returns within 5–20 sec for clips under 5 sec. Latency is dominated by polling, not transcription.
- Empty transcripts can come back for very short (<2s) clips — the API's confidence threshold. Build the rubric to handle empty-transcript as "low confidence" rather than treating it as a hard "missing words" signal (see learning #29).

### 28. **Two-stage scoring pattern: deterministic signal extraction + LLM-as-judge**

Pattern that worked for the Hinglish TTS audit (120 clips × 8 score columns):

```
Stage 1 (deterministic, local, parallel):
  for each clip:
    - DSP signals (silence, end-pop, terminal-sample) — librosa, < 0.1s/clip
    - ASR transcripts — AssemblyAI three-way (lang=hi, lang=en, auto-detect)
    - MOS predictors — UTMOS + SQUIM_SUBJECTIVE + SQUIM_OBJECTIVE
  → audit/signal_vectors.json (one structured object per clip, 16-23 fields)

Stage 2 (LLM-as-judge, batched parallel):
  - JUDGE_PROMPT.md = versioned rubric with explicit anchors per column
  - Split signals into N batches of 10 clips each
  - Spawn N parallel sub-Agent calls; each reads JUDGE_PROMPT.md + one batch
  - Each Agent writes JSON list of scoring objects to audit/judge_responses/
  - judge.py --collect assembles auto_scores.csv
```

Why this beats monolithic LLM-as-judge:
- Signals are deterministic and reproducible across runs.
- Claude (text-only) judges from structured signal vectors instead of audio it can't hear.
- Audit trail: every score's `notes` cell cites which signals drove it.
- Idempotent re-runs possible (modulo Claude's sampling).
- Re-rubric without re-extracting signals (just edit JUDGE_PROMPT.md and re-judge).

### 29. **MOS predictors (UTMOS, SQUIM) drift on Hindi by ~1.5–2 ranks**

Verified by comparing Claude-judged auto-scores against the user's manual scoring of all 120 clips:
- Auto naturalness rated **1.5–2 Likert ranks higher** than human judgment across all 4 TTS models.
- Auto intelligibility gap was smaller (0.2–1.0).
- Cause: UTMOS22 and torchaudio SQUIM models are trained on English speech corpora. They tend to score Hindi-acceptable audio higher than a Hindi-native listener does.

**How to apply:** for any future Hindi/Indic TTS audit using these predictors, treat them as **relative-ranking signal** (compare model A vs model B on the same sentence) rather than absolute MOS. Or: stack with a separate human-calibrated bias correction. Or: use a Hindi-trained MOS predictor if one becomes available.

### 30. **ThreadPoolExecutor + threading.Lock for I/O-bound + CPU-bound mixed pipelines**

The Stage 1 pipeline mixes parallelizable ASR (network I/O) with non-thread-safe MOS (torch CPU inference). Solution:

```python
ASR_PARALLEL = 5
_MOS_LOCK = threading.Lock()

def extract_one(model, wav, gt):
    # DSP — fast, pure numpy, thread-safe
    dsp = compute_dsp(wav)
    # ASR — slow, network-bound, parallelizable
    asr = lib_asr.transcribe_all(wav)
    # MOS — torch CPU inference, NOT thread-safe → serialize
    with _MOS_LOCK:
        mos = lib_mos.all_mos_signals(audio, sr)
    return {**dsp, **asr, **mos}

# Pre-warm @lru_cache singletons BEFORE the pool starts to avoid races
_ = lib_mos.all_mos_signals(first_audio, first_sr)

with ThreadPoolExecutor(max_workers=ASR_PARALLEL) as exe:
    futures = {exe.submit(extract_one, *args): args for args in jobs}
    for fut in as_completed(futures):
        ...
```

Result: 6× speedup (45 min → 7 min) for 120 clips. The lock serializes MOS but ASR (the slow part) remains parallel.

### 31. **`speechmos` (Microsoft) ≠ `tarepan/SpeechMOS` UTMOS**

The PyPI package `speechmos` is by Microsoft and contains **DNSMOS / PLCMOS / AECMOS** — NOT UTMOS. Same name, different package. Importing `from speechmos import utmos` fails.

UTMOS22 lives at `tarepan/SpeechMOS` on GitHub and loads via `torch.hub`:
```python
predictor = torch.hub.load("tarepan/SpeechMOS:v1.2.0", "utmos22_strong",
                           trust_repo=True, verbose=False)
score = predictor(audio_tensor, sr=16000).item()
```

Caveat: torch.hub downloads release artifacts from GitHub which can be **very slow** (50–150 KB/s on some networks vs 2–3 MB/s for HF / torchaudio CDN). The 392 MB UTMOS download took ~5 min on a fast network in this session, but stalled out earlier.

### 32. **Pipe buffering hides background command progress; use `python -u` AND don't pipe to tail**

When running a long script in background with `python ... 2>&1 | tail -20`, **nothing appears in the output file until the pipe closes** — `tail` buffers all input. For visibility on long-running scripts:
- Add `python -u` (unbuffered stdout) to the command.
- Drop the `| tail -N` pipe so output streams to the file as it's produced.
- Then `cat <output_file> | tail -25` periodically to check progress.

Cost of getting this wrong this session: ~30 min of wondering whether ASR was stuck before realizing the pipe was buffering.

---

## Quick reference paths

```
audit/                                project workspace
audit/eval_sentences.tsv              30 sentences, sacred
audit/reference_audio/                hindi_ref.{wav,txt}
audit/results/{kokoro,indicf5,...}/   wavs land here
/tmp/build_kaggle_kernels.py          kernel generator
/tmp/kaggle-kernels/{02..05}/         pushed kernel dirs
/home/cybernovas/kaggle-env/          kaggle CLI venv
~/.kaggle/kaggle.json                 credentials
```

```bash
# Push a kernel
export KAGGLE_USERNAME=harshalsinghcn KAGGLE_KEY=<key>
/home/cybernovas/kaggle-env/bin/kaggle kernels push -p /tmp/kaggle-kernels/02_indicf5

# Check status
/home/cybernovas/kaggle-env/bin/kaggle kernels status harshalsinghcn/hinglish-tts-audit-indicf5

# Download outputs (after COMPLETE/ERROR)
/home/cybernovas/kaggle-env/bin/kaggle kernels output harshalsinghcn/hinglish-tts-audit-indicf5 -p /tmp/kout/
```
