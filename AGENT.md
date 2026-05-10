

## 1. What we're building

A **state of art-grade Hinglish (Hindi-English code-mixed) text-to-speech system in the tens-of-millions parameter range**, built primarily by **fine-tuning an existing open Hindi-capable TTS model**, not by training from scratch. Quality target: competitive with closed Hinglish TTS APIs (Audixa, Gnani.ai) on naturalness *and* materially better on the specific Hinglish failure modes (mixed-script handling, Roman-Hindi vs English disambiguation, code-switch boundary smoothness).

The deliverable at the end is: weights + inference code + a reproducible training recipe + an honest evaluation report. Not a product, not a SaaS, not a voice-cloning service.

---

## 2. Direction (locked, May 2026)

**We fine-tune. We do not pretrain.** From-scratch training (Kokoro-style replication, ~500–2000 A100-hours) is explicitly out of scope until/unless the audit phase shows no existing base model is fixable, which would be a surprising outcome.

The current plan has three phases. We are in Phase 1.

### Phase 1 — Baseline audit (in progress)

Score four candidate base models on a hand-built 30-sentence Hinglish eval set covering pure-Devanagari, pure-Roman-Hindi, mixed-script, and English-with-Indian-named-entities. Pure inference, no training. Output: chosen base model + permanent eval set + diagnosis of which Hinglish failure modes the field is currently bad at. See `AUDIT_PLAN.md`.

Candidates being tested: **Kokoro v1.0 Hindi** (82M, Apache-2.0, smallest), **IndicF5** (~330M, AI4Bharat, F5-TTS-based, ref-audio prompted), **Indic Parler-TTS Mini** (~880M, AI4Bharat × HF, text-description prompted, joint Indic+English training — strongest Hinglish prior), **SPRINGLab F5-Hindi-24KHz** (151M, closest to our param target). Orpheus 150M is held in reserve (Modal-friendly, LoRA on T4 works) and only auditioned if the four primaries all fail.

### Phase 2 — Pipeline shakedown

Pick one base model from Phase 1. Set up a minimal LoRA / PEFT fine-tune on a *single speaker, ~30 minutes of audio, ~1 hour of T4 time*. Goal is not quality; goal is to verify the entire pipeline (data loader → tokenizer → loss → checkpoint → inference → eval) end-to-end before we spend real compute. We only commit to a real training run after this skeleton works.

### Phase 3 — Real fine-tune

Curated Hinglish data + the right text-normalization layer + the chosen base + LoRA or partial fine-tuning. Specifics depend on Phase 1+2 outcomes. The Hinglish strategy is one of three (we'll know which after the audit):

(a) *Single-model*: base already handles code-switching → light fine-tune for voice/accent only. Likeliest if Indic Parler-TTS wins.

(b) *Text-normalization*: Romanized Hindi → Devanagari via AI4Bharat's IndicXlit at preprocessing time, base model receives unified Devanagari+English. This is the [Flipkart 2023 approach](https://arxiv.org/abs/2312.01103) and the safest fallback.

(c) *Hybrid G2P*: Heavier text-frontend engineering à la Kokoro/misaki — a dedicated Hinglish G2P that emits IPA before the acoustic model sees anything. Most engineering effort but most controllable.

We will not commit to (a)/(b)/(c) before Phase 1 data is in.

---

## 3. What to take care of (the watch list)

### Compute hygiene

- **See `RESOURCE.md` for the authoritative list of free compute (quotas, CLI setup, allocation strategy per phase) and the local machine spec.** Summary: no local CUDA GPU (Intel UHD G4 integrated only, 15 GB RAM) — all training runs in cloud. Tier-1 free stack in priority order: Kaggle P100 (30 hrs/wk) → Modal.com ($30/mo recurring) → Colab T4 (~15–30 hrs/wk) → Lightning Studios (22 hrs/mo) → Saturn (30 hrs/mo). GCP $300 new-user credit held in reserve for Phase 3 (90-day expiry on activation).
- **Never start a training run without first measuring** time-per-step and VRAM peak on a 10-step probe. T4 OOM at step 500 wastes a session.
- **Save every checkpoint** + a JSON sidecar with hyperparams, dataset hash, and git SHA. Provenance > storage cost.
- **Mixed precision is not free.** StyleTTS2 stage 1 NaNs in fp16 (issue #10/#11). Many TTS losses are numerically tender. Default to fp32 unless we have a working fp16/bf16 baseline for *that exact stack*.

### Eval discipline

- The 30-sentence eval set from Phase 1 is **sacred**: never modified retroactively, never used for training, never expanded except by adding new sentences (and re-scoring all prior models).
- **Listen, don't just look at metrics.** MOS-like scores are lossy. We commit to A/B listening before any model declared "better."
- Score at least three boolean failure flags per sentence: `roman_treated_as_english`, `silence_or_skip_on_unknown_word`, `end_of_clip_pop`. These are the Hinglish-specific failure modes worth tracking longitudinally.

### Data and tokenizer drift

- **The single most common TTS regression cause is phonemizer mismatch between base-model training and our fine-tune.** Whatever base we pick, we use *exactly* its training-time phonemizer config (espeak-ng version, `preserve_punctuation`, `with_stress`, language code, IPA dialect). Document this in the run config.
- **Sample rate must match the base model.** Resample once at preprocessing, never at runtime. 24 kHz is the dominant rate (Kokoro, IndicF5, IndicTTS); LJSpeech is 22.05; LibriTTS is natively 24.
- **Synthetic-data licensing**: do not train on outputs of closed proprietary TTS APIs unless their ToS explicitly permits it. If we use synthetic Hinglish data, we generate it from open-licensed models only (or our own earlier checkpoints). All data sources go in `DATA_SOURCES.md` with license annotations.

### Hinglish-specific gotchas

- The four hard cases of Hinglish (pure Devanagari, pure Roman-Hindi, mixed-script, English-with-Indian-NEs) need separate evaluation. A model that aces three and fails one is not "75% there" — the failure mode usually dominates user perception.
- **Roman-Hindi disambiguation is genuinely hard.** "hai" (Hindi "is") vs "hi" (English greeting) vs "Hi" (proper noun). Models without context-aware language ID on tokens will fail predictably. The MoH (Map-only-Hindi) pipeline and HingBERT-LID are the standard precedents to study before designing our normalization layer.
- **Mixed-script sentences cannot be solved by language-ID alone**: in `Kal mujhe ऑफिस जाना hai`, the script switches mid-token. Robust handling requires either token-level LID or a unifying script normalization step.
- **Indian proper nouns in English sentences** ("Bengaluru", "Khanna", "Aishwarya") are an under-discussed failure mode for English-trained TTS — they often produce mangled or English-phonetic mispronunciations. This is part of the Hinglish problem even for "pure English" inputs from Indian users.

### Architecture-specific traps (carry forward from the Kokoro doc + StyleTTS2 lessons)

- Catastrophic forgetting during sequential single-speaker fine-tuning of multispeaker bases. Mitigation: shuffle speakers across batches; never curriculum.
- End-of-clip pop on bases finetuned from short-clip data (Kokoro inherits this from LJSpeech). Mitigation: append ~100 ms of silence + stop token to all training clips.
- DDP is broken in StyleTTS2 `train_second.py` (issue #7). If we ever return to that codebase, use DataParallel only.
- Below `batch_size=2` or `max_len=100`, the StyleTTS2 trainer crashes — do not chase smaller-batch-fits-on-T4 fantasies; we'd be fighting the wrong battle.

---

## 4. Working principles for the assistant (Claude)

1. **Search before asserting.** TTS moves fast — model versions, fine-tuning recipes, and library APIs change month to month. For any factual claim about a model, dataset, library, or training recipe, web-search first. Cite sources where the user might want to follow up.

2. **Don't reinvent.** Always check whether a pretrained sub-module, dataset, or recipe already exists before recommending a custom one. The Kokoro doc's principle ("aggressive front-end engineering replaces neural-backbone scale") applies recursively to *us* — using existing G2P, ASR aligners, codecs, and tokenizers is correct.

3. **Push back on expensive proposals which maybe not good risk vs reward.** Before any experiment estimated at > 4 GPU-hours, the assistant asks: "is there a 30-minute sanity check we could run first that would invalidate this idea cheaply?" If yes, do that first. Compute is the binding constraint.

4. **Update the research log every substantive session.** New verified facts → log. Mistakes → log. Decisions and the reason for them → log. The user maintains the file; the assistant proposes diffs. there is the file 

5. **Beginner-friendly but technically precise.** The user has not trained TTS from scratch before. Explain the *why* of every recommendation (why this loss, why this sample rate, why this LR). Don't dumb down the math; do connect it to intuition.

6. **One step at a time.** Don't dump six phases of plan when the user is on phase one. If the user asks "what's next?", answer for the immediate next step in detail, and the one after in outline only.

7. **Track time-to-first-result, not just GPU-hours.** A two-day setup is not "free" because it ran on Colab. The assistant should flag setup overhead explicitly.

8. **Listen for drift.** If the user starts asking about pretraining, voice cloning for celebrities, or end-to-end voice agents, that's scope creep. Politely note it and bring the focus back to the Hinglish fine-tune objective.

---

## 5. What we will NOT do (the negative scope)

- Pretrain PL-BERT, AuxiliaryASR, JDCNet, or any other auxiliary network. Public checkpoints exist; we use them.
- Replicate hexgrad's proprietary synthetic-audio data pipeline.
- Build a custom phonemizer when misaki (Hindi module exists) or espeak-ng (handles Hindi natively) suffices.
- Train on outputs of closed-source TTS APIs whose ToS forbids it.
- Optimize before measuring. Always: baseline → measure → identify the largest deficit → target it.
- Pretend our model is "production-ready" before it has passed at least 100 native-speaker A/B comparisons.
- Claim novelty for things that are not novel. The contribution of this project is "open-source Hinglish TTS that handles code-switching well under tight compute," not a new architecture.

---

## 6. Files and structure (what lives where)

make this files if the repo don't have
```
/RESEARCH_LOG.md      ← append-only log of decisions, mistakes, learnings.
                        Authoritative; if any other doc disagrees, log wins.
/AGENT.md             ← this file. Updated when direction changes.
/RESOURCE.md          ← local machine spec + free cloud compute (quotas, CLI setup,
                        per-phase allocation strategy). Update when quotas/credits change.
/AUDIT_PLAN.md        ← Phase 1 audit recipe, eval-set spec, scoring rubric.
/DATA_SOURCES.md      ← (to create in Phase 2) every dataset, license, hash, sample rate.
/runs/<date>_<name>/  ← (Phase 2+) one folder per training run with config, log, checkpoints, samples.
/audit/               ← Phase 1 outputs: eval_sentences.tsv, audio/, scores.tsv, DIAGNOSIS.md.
```

The git repo is the project's source of truth. Both audio outputs and the research log live in git (audio via Git LFS or HF dataset upload — decide before the audit produces > 100 MB).


