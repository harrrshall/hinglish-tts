# Known Limitations

Read this before installing. The 4.70 score is real, but it was measured on a specific eval
set with one reference voice under specific conditions. Below is what the score does not cover
and what the package does not do.

---

## 1. Acoustic texture

Every output clip has the characteristic texture of Vocos-vocoded speech. To a trained ear —
particularly anyone who has worked in audio production — the timbre is identifiable as
synthetic regardless of intelligibility score. This is a property of the vocoder and the
IndicF5 training distribution (2023–2024), not a bug in the preprocessing or the duration
patch. Clips that score 5/5 on intelligibility still sound like TTS because ASR is measuring
word accuracy, not timbral quality.

**What this means in practice:** if your use case requires audio that passes a "does this
sound human" test with audio-literate listeners, this package does not meet that bar. It is
suitable for voice interfaces, content prototyping, and accessibility tools where intelligible
synthesis at natural speed is the goal.

**What would change it:** fine-tuning on naturalistic Hindi speech with a higher-bandwidth
neural codec vocoder (e.g. EnCodec-based). That is a separate training project and is not
included here.

---

## 2. Flat prosody

Delivery is conditioned on a single neutral reference clip. Declarative sentences, questions,
and exclamations all receive a similar falling-then-flat intonation contour. Punctuation has
limited effect — the phonetic probe (`experiments/05_phonetic_probe/`) measured a ~44%
duration difference between plain and ellipsis+exclamation variants, and a raised terminal
pitch, but not the kind of dramatic expressive delivery a human speaker would produce.

The inference API has no mechanism for requesting "deliver this with urgency" or "read this
as a question." There is no text-level prosody conditioning in IndicF5.

**What this means in practice:** conversational back-and-forth, emotional scenes, and
multi-sentence narration with varied register will all sound flat. Single declarative
statements and neutral informational content are where the package performs best.

---

## 3. One fixed reference voice

The 4.70 score was measured using the reference clip in `data/reference_audio/hindi_ref.wav`.
The `synthesize()` API accepts any 3–10s reference clip, but voice-to-voice fidelity has not
been measured, and the following are true:

- The duration patch and preprocessing were validated against one voice. Canvas allocation
  behavior with other voices has not been checked.
- IndicF5's zero-shot cloning is sensitive to reference audio quality. Background noise,
  reverb, clipping, and non-speech sounds in the reference all degrade output quality.
- No speaker-similarity metric (e.g. speaker cosine similarity via an x-vector model) was
  computed. Informal listening suggests the model captures broad voice weight and register
  from a reference clip, but this was not quantified.

This package does not provide a validated plug-and-play "clone this voice" workflow. If
custom voice cloning is your use case, treat the reference-clip input as experimental and
evaluate on your specific target voice before committing.

---

## 4. Generalization not measured

The 30-sentence eval set covers four categories: pure Devanagari, pure Roman Hinglish,
mixed script, and English with Indian named entities. Within those categories it was designed
to cover common colloquial patterns. What it does not cover:

- Long-form content (sentences substantially over ~15 words)
- Technical and domain-specific vocabulary (medical, legal, financial)
- Code-switching in specialized registers (e.g. software engineering Hinglish)
- Regional Hindi dialects (Bhojpuri, Rajasthani, Haryanvi influence)
- Dense multi-language alternation within a single utterance

No native-speaker A/B comparison at scale has been conducted. The naturalness evaluation in
this package was a single informal listen over 30 clips — not a rated perceptual study with
multiple listeners and a statistical design. The 4.70 score is an intelligibility ceiling,
not a naturalness floor, and it is a 30-sentence sample, not a population estimate.

**If you are evaluating for production use**, run your own eval set. The rubric is
documented in `EVALUATION_REPORT.md` and is re-runnable against any new sentences with
the scoring scripts in `scoring/`.

---

## 5. IndicXlit edge cases on rare tokens

The preprocessing pipeline handles Roman tokens in four tiers:

1. **Short Hindi function words** (`mai`, `tu`, `aa`, `hu`): handled by the 4-entry
   function-word whitelist before IndicXlit sees the token.
2. **Common English loanwords** (`office`, `laptop`, `party`, etc.): handled by the
   36-entry loan whitelist.
3. **Indian proper nouns** (`Delhi`, `Mumbai`, `Aishwarya`, etc.): handled by the
   19-entry NE whitelist.
4. **Everything else**: falls through to IndicXlit transliteration.

IndicXlit handles common vocabulary reliably. It degrades on:

- **Rare proper nouns**: uncommon surnames, small-city place names, startup brands,
  regional names. The whitelist was built from a 30-sentence eval set and does not cover
  the long tail.
- **Short ambiguous tokens** (2–3 characters): common postpositions like `se`, `ko`, `ne`
  are not in the function-word whitelist. IndicXlit may render these with English phonetics.
- **Abbreviations**: `NGO`, `CEO`, `IIT` are lowercased to `ngo`, `ceo`, `iit` before
  lookup. They miss the whitelists and IndicXlit output is unpredictable.

**How to extend the whitelists:** add entries to `ENGLISH_LOAN_CANONICAL`,
`INDIAN_NE_CANONICAL`, or `ROMAN_HINDI_FUNCTION_WORDS` in
`scoring/scripts/lib_normalize.py`. No retraining required; changes take effect immediately.

---

## 6. Output is 24 kHz — resampling is the caller's responsibility

IndicF5 outputs 24 kHz mono PCM float32. `synthesize()` returns this array directly.
If your downstream system expects a different sample rate, resample before writing:

```python
import librosa
audio_16k = librosa.resample(audio, orig_sr=24000, target_sr=16000)
sf.write("out.wav", audio_16k, 16000)
```

No automatic resampling is applied. Common failure modes if you skip this:

- **Playback on a 44.1 kHz device without resampling:** the audio plays at 24/44.1 ≈ 54%
  of normal speed with a pitch shift down.
- **Writing 24 kHz audio to a 16 kHz pipeline:** the pipeline either rejects it or
  interprets the sample data incorrectly, producing corrupted or truncated audio.
- **Telephone/VoIP systems:** almost universally expect 8 kHz or 16 kHz. A 24 kHz WAV
  will not play correctly without explicit resampling.

`librosa`, `torchaudio.functional.resample`, and `soundfile`+`resampy` all handle this.
The choice is yours; the responsibility is yours.
