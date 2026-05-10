# Sarvam AI

**Website:** https://sarvam.ai  •  **HQ:** Bengaluru, Karnataka, India  •  **Founded:** August 2023  •  **Stage:** Series B (closing ~April 2026)
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch: India's full-stack sovereign AI platform — foundation models, voice/speech/translation APIs, and enterprise agents, all built and hosted entirely in India for 22 Indian languages.
- Total funding to date: ~$391M (seed + Series A: $41M; additional round Aug 2025: undisclosed; Series B closing: ~$350M)
- Last round: ~$300–350M, April 2026, led by Bessemer Venture Partners; co-investors Nvidia, Amazon/AWS, HCLTech, Accel, Prosperity7, Glade Brook Capital; post-money valuation $1.5B (unicorn)
- Headcount: ~150 as of Q1 2026 (114 verified as of Aug 2025; 226% YoY growth claimed)
- Revenue / ARR: ₹29.1 crore (~$3.5M) as of FY2025 (year ending March 2025) — verified via disclosed financials; ARR for FY2026 not publicly available

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| Dec 2023 | Seed + Series A (combined) | $41M | Lightspeed Venture Partners | Peak XV Partners, Khosla Ventures | TechCrunch, YourStory, Inc42 |
| Aug 2025 | Strategic/bridge | Undisclosed | Avvanti Advisors | Unknown | Tracxn, ipoplatform.com |
| Apr 2026 | Series B (closing) | ~$300–350M | Bessemer Venture Partners | Nvidia, Amazon/AWS, HCLTech, Accel, Prosperity7 Ventures, Glade Brook Capital | Bloomberg, BW Businessworld, Outlook Business |

**Post-money valuation (Series B):** $1.5 billion (Bloomberg, April 2026; verified claimed — formal close pending as of May 2026)

**Note on IndiaAI Mission compute:** In April 2025, the Government of India (IndiaAI Mission) provided subsidised access to 4,096 NVIDIA H100 GPUs at Yotta's Shakti data centre, valued at ~₹247 crore; in exchange Sarvam gave the government an equity stake. This is a non-cash quasi-funding event, not a traditional round.

## 3. Product & Customers

### Products

Sarvam operates across three layers: (1) foundation models (open-weight and API), (2) developer APIs / platform, and (3) enterprise products.

**Foundation Models:**
| Model | Params | Released | Notes |
|-------|--------|----------|-------|
| Sarvam-2B | 2B | Aug 2024 | Trained from scratch; 4T tokens; 10 Indic languages |
| Sarvam-1 | 2B | Oct 2024 | Tokenizer-optimised; 2T Indic tokens; 10 languages; open-weight |
| Sarvam-M | 24B | May 2025 | Fine-tuned from Mistral Small; SFT + RLVR; hybrid think/non-think; open-weight |
| Sarvam-Translate | 4B | Jun 2025 | Fine-tuned from Gemma3-4B-IT (collab AI4Bharat); 22 official Indian languages; open-weight |
| Sarvam-30B | 30B | Feb 2026 | Trained from scratch; MoE (128 experts, 2.4B active); Apache 2.0; open-weight |
| Sarvam-105B | 105B | Feb 2026 | Trained from scratch; MoE (128 experts, 10.3B active); Apache 2.0; open-weight |
| Sarvam Vision | 3B | Feb 2026 | State-space VLM; OCR + document intelligence; 23 languages |
| Shuka-1 | — | 2024 | Audio LLM (India's first audio LLM in Hindi); open-weight HF |

**Speech & Translation APIs:**
- **Bulbul v2/v3 (TTS):** Text-to-speech; 11 Indian languages; 35+ professional voices; LLM-based prosody; zero-shot voice cloning; consent-driven brand voice creation; streaming at 8kHz (telephony) and 48kHz (studio)
- **Saarika / Saaras v3 (ASR):** Streaming speech-to-text; 22 Indian languages; code-mixed support; low-latency decoding; diarization variant available
- **Mayura / Sarvam-Translate:** Translation API; 22 Indian languages; handles colloquial language and code-mixing

**Enterprise Products:**
- **Samvaad:** Omnichannel conversational AI agent platform (voice, WhatsApp, in-app); connects to enterprise tools; multilingual across 11 languages; available on AWS Marketplace
- **Akshar:** Document intelligence workbench; powered by Sarvam Vision; extracts structured data from unstructured Indian documents
- **Sarvam Studio:** AI video dubbing and document translation workspace; zero-shot voice cloning across languages; 11 Indian languages; launched Feb 12 2026; beta rollout to production partners (government, education, media)

**Consumer / Emerging Products:**
- **Indus (app):** AI chat assistant powered by Sarvam-105B; web + iOS + Android; multilingual mid-chat; launched Feb 20 2026; India-only; waitlisted rollout
- **Sarvam Kaze (hardware):** AI smart glasses; embedded camera + mic; real-time visual understanding; 11 Indian languages; EdgeAI for offline operation; unveiled at India AI Impact Summit Feb 2026; PM Modi demo'd them; consumer launch planned May 2026; controversy: critics allege white-label Chinese OEM hardware with Sarvam AI software layer (not confirmed)

**Chanakya (vertical):** Secure, air-gapped AI framework for defence, regulated finance, government departments; on-premise deployments; dual-use (enterprise + strategic sectors); announced Mar 30 2026

### Pricing
All users start with ₹1,000 free credits (never expire). Pay-per-use with optional subscription plans:

| Plan | Monthly cost | Bonus credits | Rate limit |
|------|-------------|--------------|------------|
| Starter | ₹0 | — | 60 req/min |
| Pro | ₹10,000 | ₹1,000 | 200 req/min |
| Business | ₹50,000 | ₹7,500 | 1,000 req/min |

**API rates (pay-per-use):**
| Service | Rate |
|---------|------|
| Sarvam 105B input / cached / output | ₹4 / ₹2.5 / ₹16 per 1M tokens |
| Sarvam 30B input / cached / output | ₹2.5 / ₹1.5 / ₹10 per 1M tokens |
| Sarvam Vision | ₹1.50 per page |
| Speech-to-Text (Saaras v3) | ₹30 per hour of audio |
| Speech-to-Text with Diarization | ₹45 per hour of audio |
| Text-to-Speech Bulbul v3 | ₹30 per 10,000 characters |
| Text-to-Speech Bulbul v2 | ₹15 per 10,000 characters |
| Translation (Mayura/Translate) | ₹20 per 10,000 characters |
| Language Identification | ₹3.50 per 10,000 characters |

Enterprise Samvaad and Akshar: custom contract pricing, not publicly listed.

### Languages & Voices
- **ASR (Saaras v3):** 22 scheduled Indian languages
- **TTS (Bulbul v3):** 11 languages — Hindi (hi-IN), Bengali (bn-IN), Tamil (ta-IN), Telugu (te-IN), Gujarati (gu-IN), Kannada (kn-IN), Malayalam (ml-IN), Marathi (mr-IN), Punjabi (pa-IN), Odia (od-IN), English (en-IN); 35+ professional voice artists; code-mixing supported; expansion to 22 languages planned
- **Translation:** 22 official Indian languages across 12 scripts
- **LLMs:** Primary focus on 10 spoken Indian languages; tokenizer optimised across 22 scheduled languages

### Named Customers
- **Tata Capital:** Samvaad deployed across consumer loan products; 20 million+ monthly multilingual voice interactions; sentiment detection + human escalation (verified — Sarvam website case study)
- **EkStep Foundation:** "Listen at Scale" deployment — Sarvam case study on website
- **UIDAI (Aadhaar):** Partnership announced March 2025 for AI-driven voice interactions and multilingual support in Aadhaar services (verified — UIDAI press release)
- **Government of Odisha:** MOU signed Feb 2026; 50MW AI-optimised data facility; Vision AI for mining safety; Odia voice technologies
- **Government of Tamil Nadu + IIT Madras:** Digital Sangam Sovereign AI Research Park; 20MW data centre; Vivasāya Nanban (AI farm advisory for 8M households); Unified Citizen Helpline
- **BHASHINI (MeitY):** Sarvam models integrated into national language AI platform serving 600 crore+ AI requests; 500+ government websites

**Industry verticals:** BFSI (Tata Capital), Government/Civic, Agriculture, Education, Healthcare, Media/Content

### Integrations / SDKs
- **LiveKit** — real-time voice infrastructure for voice AI agents
- **Pipecat** — open-source Python framework; Sarvam STT + LLM built-in
- **n8n** — workflow automation; 1,000+ app connections
- **LangChain** — Sarvam Cloud integration (partner package in progress as of early 2026)
- **LlamaIndex** — community integration requested/in development
- **Microsoft Azure Marketplace** — listed
- **AWS Marketplace** — Sarvam Samvaad listed
- **Google Cloud** — listed
- **TCS, Infosys** — system integrator partnerships
- **Vercel AI SDK** — community-built provider
- **Google DeepMind Gemmaverse** — Sarvam-Translate featured

## 4. Technical Architecture

### Model approach
- **LLMs (30B, 105B):** Heterogeneous Mixture-of-Experts (MoE); sparse expert FFN with 128 experts; rotary positional embeddings (RoPE); RMSNorm stabilization; sigmoid-based routing (not softmax); Grouped Query Attention (GQA) in 30B; Multi-head Latent Attention (MLA, similar to DeepSeek-V3) in 105B for KV-cache compression; trained entirely from scratch using NVIDIA NeMo + Megatron-LM
- **Sarvam-1 (2B):** Autoregressive LM; SwiGLU activation; RoPE; GQA; bfloat16 mixed-precision
- **Sarvam-M (24B):** Post-trained from Mistral Small base; SFT + RLVR (Reinforcement Learning with Verifiable Rewards); asynchronous GRPO architecture with adaptive sampling
- **Bulbul v3 (TTS):** LLM-based architecture; parses text for prosodic elements; streaming output; cross-lingual transfer learning; not a traditional AR vocoder + acoustic model stack (specific codec not publicly disclosed)
- **Sarvam Vision (3B):** State-space Vision Language Model (VLM); not a standard transformer-based VLM

### Training data
- **Sarvam-1:** ~2 trillion Indic tokens (Sarvam-2T corpus); ~1T Indic + ~1T English + code; 10 Indian languages
- **Sarvam-30B:** 16 trillion tokens spanning code, web, mathematics, multilingual; dedicated Indic sub-corpora
- **Sarvam-105B:** 12 trillion tokens; same categories; emphasizes 10 most-spoken Indian languages
- **Sarvam-Translate:** Fine-tuned from Gemma3-4B-IT; in collaboration with AI4Bharat; document-level translation dataset
- **Samvaad-Hi-v1 dataset (open-sourced Aug 2024):** 100,000 high-quality multi-turn conversations; 700,000+ turns; English, Hindi, Hinglish with Indic context
- Training infrastructure: NVIDIA NeMo framework + Megatron-LM for pre-training; Nemo-RL for post-training/RL; executed on 1,024–4,096 H100 GPUs at Yotta's Shakti cluster (government-subsidised compute from IndiaAI Mission)
- Data sourcing/licensing: Not fully public; primarily web data, synthetic data pipelines, and Indian-language corpora; AI4Bharat collaboration for language datasets

### Latency profile
- **Sarvam-30B (H100):** 3x–6x higher throughput/GPU vs Qwen3 baseline (claimed, not independently verified)
- **Sarvam-105B (L40S):** 1.5x–3x throughput improvements at typical operating points (claimed)
- **Apple Silicon M3 (GGUF):** 20–40% higher token throughput with MXFP4 mixed-precision
- **Bulbul v3 TTS:** Low-latency streaming at "near real time" — specific TTFB not published
- **Samvaad voice agents:** <500ms end-to-end latency claimed; deploys in <24 hours
- Real-time factor for ASR/TTS: Not publicly published

### Voice cloning
- Zero-shot voice cloning in Bulbul v3: retains speaker voice characteristics across languages (used in Sarvam Dub/Studio)
- Consent-driven tool for enterprise brand voice creation
- Min sample length for cloning: Not publicly specified
- Fine-tune based cloning: Not documented publicly

### Prosody / emotion control
- Bulbul v3 automatically infers emphasis, pauses, tone, and pacing from context and intent (LLM-based inference, no manual knobs documented)
- Cross-lingual transfer: voices trained in one language transfer to others
- Emotion tags / SSML-style control: Not documented in public API reference

### Indic language strategy
- Lineage: Both founders co-founded AI4Bharat at IIT Madras; Sarvam-Translate built with AI4Bharat; Shrutilipi and IndicTTS ecosystem inherited indirectly
- Custom tokenizer with 1.4–2.1 fertility across Indic scripts (2–4x more efficient than generic multilingual tokenizers)
- 22-language coverage across 12 scripts (Devanagari, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Odia, etc.)
- Dedicated Indic pre-training corpus (Sarvam-2T)
- On-device: Sarvam-M and 30B available as GGUF for local inference; Kaze glasses use EdgeAI model for offline operation

### Inference stack
- Cloud: Proprietary serving infrastructure; NeMo-optimised serving; listed on Azure, AWS, Google Cloud
- Local/on-device: GGUF and MXFP4 quantised weights released on HuggingFace
- Chanakya: Air-gapped, on-premise deployment for government/defence
- NVIDIA collaboration: Library support across pre-training, alignment, and serving as part of IndiaAI Mission partnership

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Announcing Series A | Blog | Dec 2023 | https://www.sarvam.ai/blogs/announcing-series-a |
| Sarvam Product Launch (full-stack GenAI platform) | Blog | Aug 2024 | https://www.sarvam.ai/blogs/sarvam-launch |
| Sarvam-2B + Samvaad-Hi-v1 dataset | Blog + Dataset | Aug 2024 | https://www.marktechpost.com/2024/08/14/... |
| Sarvam-1 (2B open-weight) | Blog | Oct 2024 | https://www.sarvam.ai/blogs/sarvam-1 |
| Sarvam-M (24B hybrid reasoning) | Blog | May 2025 | https://www.sarvam.ai/blogs/sarvam-m |
| Sarvam-Translate (22-language translation) | Blog | Jun 2025 | https://huggingface.co/sarvamai/sarvam-translate |
| India's Sovereign LLM announcement | Blog | Apr 2025 | https://www.sarvam.ai/blogs/indias-sovereign-llm |
| Sarvam Vision (OCR/document intelligence) | Blog | Feb 2026 | https://www.sarvam.ai/blogs/Sarvam-vision |
| Open-Sourcing 30B and 105B | Blog | Feb 2026 | https://www.sarvam.ai/blogs/sarvam-30b-105b |
| Bulbul v3 (TTS) | Blog | Feb 2026 | https://www.sarvam.ai/blogs/bulbul-v3 |
| Sarvam Studio (AI dubbing) | Blog | Feb 2026 | https://www.sarvam.ai/blogs/sarvam-studio |
| NVIDIA co-design blog | Technical blog | 2026 | https://developer.nvidia.com/blog/how-nvidia-extreme-hardware-software-co-design-delivered-a-large-inference-boost-for-sarvam-ais-sovereign-models/ |
| Partnerships with Indian States (Odisha, Tamil Nadu) | Blog | Feb 2026 | https://www.sarvam.ai/blogs/partnerships-with-indian-states |
| Chanakya secure AI vertical | Blog | Mar 2026 | https://www.itvoice.in/sarvam-ai-unveils-chanakya-a-sovereign-ai-framework-for-high-security-sectors |

**arXiv papers:** No dedicated arXiv preprints found as of May 2026. Research is released via the company blog and HuggingFace model cards. Pratyush Kumar has 5,293+ Google Scholar citations (prior AI4Bharat work). This is a gap relative to peers like AI4Bharat which publishes on arXiv.

## 5. Open Source Footprint

### GitHub
**Org URL:** https://github.com/sarvamai (32 public repositories as of April 2026)

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| sarvam-ai-cookbook | 153 | 78 | — | Feb 2026 | Jupyter notebooks; primary developer resource |
| sarvam-mcp | 2 | 1 | — | Apr 2026 | MCP server integration |
| sarvam-ai-sdk | 6 | 2 | — | Apr 2026 | TypeScript SDK |
| skills | 60 | 8 | Mixed | Mar 2026 | Practical skills/examples for building with Sarvam APIs |
| llm_intent_entity | 59 | 13 | Python | Apr 2026 | LLM-based evaluation for ASR intent/entity |
| llm_wer | 26 | 8 | Python | Apr 2026 | LLM-based WER evaluation for ASR |
| Megatron-Bridge | 0 | 306 | Python | Mar 2026 | Bridge tooling (fork of NVIDIA Megatron-LM) |
| Megatron-LM | 0 | 3.9k | Python | Jan 2026 | Fork of NVIDIA Megatron-LM (training infra) |
| indic_nlp_library | 10 | 177 | Python | May 2025 | Indic NLP tools |
| pyannote-audio | 1 | 1.1k | Jupyter | Jun 2025 | Fork for diarization |
| sarvam-streaming-apis | 1 | 1 | HTML | Jun 2025 | Streaming API demos |
| computer_use_agents | 4 | 417 | Python | May 2025 | Computer use agents |
| Shoonya-Backend / Frontend | 0 | 16/17 | Py/JS | May 2024 | Data annotation platform (legacy) |

Most high-fork repos are forks of established OSS projects (Megatron-LM, mlx-lm, pyannote, torchtune). Original repos have modest stars. Flagship developer resource is `sarvam-ai-cookbook` (153 stars).

### Hugging Face
**Org URL:** https://huggingface.co/sarvamai (14+ models as of May 2026)

| Model | Downloads | Likes | License | Notes |
|-------|-----------|-------|---------|-------|
| sarvamai/sarvam-30b | 52.2k | 190 | Apache 2.0 | Primary open-weight 30B |
| sarvamai/sarvam-105b | 20.2k | 266 | Apache 2.0 | Primary open-weight 105B |
| sarvamai/sarvam-translate | 6.71k | 130 | — | 22-language translation |
| sarvamai/sarvam-m | 2.54k | 342 | — | Highest likes; 24B hybrid reasoning |
| sarvamai/sarvam-30b-fp8 | 779 | 11 | — | Quantised serving variant |
| sarvamai/sarvam-30b-gguf | 499 | 18 | — | Local inference |
| sarvamai/sarvam-105b-gguf | 114 | 15 | — | Local inference |
| sarvamai/sarvam-105b-fp8 | 367 | 5 | — | Quantised serving |
| sarvamai/sarvam-m-q8-gguf | 140 | 16 | — | Quantised |
| sarvamai/sarvam-1 | — | — | — | 2B October 2024 release |
| sarvamai/shuka-1 | — | — | — | Audio LLM |
| sarvamai/sarvam-m-gguf | 48 | 9 | — | Local inference |
| datasets: sarvamai/samvaad-hi-v1 | — | — | — | 100K Hindi/Hinglish conversations |

Download counts as of late April/early May 2026. Note: Sarvam-M faced a controversy in May 2025 where downloads spiked suspiciously from ~300/day to ~100,000/day over a weekend; allegations of bot-farming were made but not confirmed.

### Top contributors
- **saurabh-sarvam** (GitHub: saurabh-sarvam) — active in cookbook and API tooling
- **vinayak-sarvam** (GitHub: vinayak-sarvam) — built Vercel AI SDK provider
- Core research team names not prominently visible on GitHub; company uses internal repos for model training

## 6. Team

### Founders
**Dr. Pratyush Kumar (CEO & Co-founder)**
- Education: BTech EE IIT Bombay; PhD Computer Engineering ETH Zurich (2014)
- Prior roles: Research at IBM, Microsoft Research; Faculty at IIT Madras; Co-founder AI4Bharat (IIT Madras); Co-founder One Fourth Labs (Padh.ai)
- Research: 5,293+ Google Scholar citations; fields: SysDL, NLP, AI for social good
- GitHub: Not prominently public
- LinkedIn: https://in.linkedin.com/in/pratyush-kumar-iitb (profile exists; details behind paywall)

**Dr. Vivek Raghavan (Co-founder)**
- Education: BTech EE IIT Delhi; PhD ECE Carnegie Mellon University
- Prior roles: VP at Magma Design Automation; Synopsys; Avant! Corporation; 12 years volunteering with UIDAI on Aadhaar biometrics; AI Evangelist at EkStep Foundation; advisor to AI4Bharat and Bhashini
- Founded and sold 2 EDA companies before Sarvam
- Tech advisor to UIDAI
- LinkedIn: https://in.linkedin.com/in/vivek-raghavan-16005424

### Key technical hires
- **Shubham Arora** — Head of Sales and Business Development
- **Chaitra Acharya** — Head of Finance / Director Finance
- Specific ML/research hire names are not publicly listed on the website or in news coverage; the company maintains a relatively low public profile for individual researchers below co-founder level.

### Recent joiners (last 12mo)
- Company grew from ~50–60 employees (early 2024) to 114 (Aug 2025) to ~150 (Q1 2026) — 226% YoY growth claimed. Hiring spans: ML Engineers (Speech AI), Frontend Engineers (React Native), DevOps, Backend, SRE, Forward Deployed Engineers, Product, GTM roles.
- 24 open positions as of May 2026 (per Uplers job listings).

### Notable departures (last 12mo)
- None publicly reported.

### Open roles signal
As of May 2026: 24 open roles across engineering (ML, frontend, backend, DevOps, SRE), product, GTM, and internships. Active hiring in ML Speech AI and autonomous agent engineering suggests ASR/TTS and agentic product lines are expanding. Careers: https://www.sarvam.ai/careers

## 7. Moat & Defensibility

- **Data moat:** Strong — Sarvam-2T corpus of 2T+ Indic tokens is proprietary; Samvaad-Hi-v1 dataset open-sourced; AI4Bharat data lineage (Shrutilipi, IndicSUPERB) from academic collaboration; growing production data from Tata Capital, UIDAI, government deployments creates flywheel; however, AI4Bharat datasets are public, so partial replication is possible.

- **Model moat:** Moderate and strengthening — 30B and 105B trained from scratch on Indic-optimised corpus with custom tokenizer and MoE architecture; clear benchmark leadership on Indic language tasks (90% win rate claimed); Sarvam Vision beats Gemini Pro and GPT on Indian OCR benchmarks; but models released as Apache 2.0 open-weight, so weights themselves are not proprietary.

- **Distribution moat:** Strong — Government of India equity partner (IndiaAI Mission); UIDAI/Aadhaar integration; BHASHINI platform; Odisha and Tamil Nadu state MOU partnerships; Tata Capital (major BFSI anchor); Azure + AWS + GCP marketplace listings; TCS and Infosys SI channel; first-mover advantage in government-grade (Chanakya) air-gapped deployments.

- **Brand / community moat:** Moderate — Named for "all" (Sanskrit Sarvam); "14 launches in 14 days" campaign at India AI Impact Summit Feb 2026 generated significant media coverage; PM Modi demo'd Kaze glasses; 153-star cookbook and modest GitHub community; Indus app on App Store/Play Store; but brand is still nascent outside India.

- **Regulatory moat:** Moderate — ISO certification + SOC 2 Type II (claimed in enterprise materials); DPDP Act alignment (building consent-driven voice cloning, data stored in India); government equity stake creates regulatory protection; Chanakya vertical targets classified/regulated environments; India's AI regulation posture (DPDP, proposed AI governance framework) could advantage domestic vendors; EU AI Act exposure minimal (India-focused).

- **Replication cost (6mo, $10M competitor):** At $10M/6 months a competitor could fine-tune open-weight models (Llama, Gemma, Mistral) on public Indic datasets (AI4Bharat, Common Voice) and match Sarvam-M quality — but could NOT replicate: (a) government relationships and IndiaAI Mission mandate, (b) Sarvam's custom from-scratch 30B/105B models requiring ~$20–50M in compute alone, (c) the UIDAI/BHASHINI/state-government integrations, (d) production-hardened Samvaad agent platform. Net: API-level parity achievable; full-stack sovereign moat is not replicable at $10M.

- **Moat strength: 4/5** — Government mandates and India-specific data flywheel create a defensible position that global AI labs cannot easily replicate, but open-weight model releases and dependence on NVIDIA compute reduce technical exclusivity.

## 8. Risks & Problems

### Technical complaints
- **Pipecat integration broken (GitHub Issue #3783, pipecat-ai/pipecat):** Sarvam integration depends on outdated sarvamai SDK v0.1.21 which lacks support for Saaras v3 STT `mode` parameter; upgrading to v0.1.25 still doesn't expose the `prompt` parameter. Active open issue. Source: https://github.com/pipecat-ai/pipecat/issues/3783
- **Indus app limitations:** Users cannot delete chat history without deleting account; no option to disable reasoning mode which can slow responses; available only in India.
- **Sarvam-M low initial adoption:** Initial 334 downloads in 2 days post-launch (May 2025); Deedy Das (Menlo Ventures) publicly called it "embarrassing" on X, contrasting with ~200,000 downloads for a Korean college students' open-source model. Source: multiple news reports.
- **Sarvam-M download spike controversy:** Downloads surged from ~300/day to ~100,000/day in one weekend in May 2025; community alleged bot-farming to inflate HF metrics. Sarvam did not publicly respond. Source: avidclan.com investigation, analyticsindiamag.com.
- **Coding capability gaps:** User reviews note coding performance lags Claude/GPT; Indus app rated 4.4 stars on Google Play but users specifically note coding as a weakness.

### Pricing pain points
- API pricing is in INR only, with limited transparency about enterprise Samvaad/Akshar costs; no public SLA or uptime guarantees found.
- Rate limits on Starter tier (60 req/min) are restrictive for production testing.

### Safety / misuse
- Voice cloning consent flow exists but implementation details (minimum consent, audit trail) are not publicly documented.
- No published safety card, red-teaming report, or responsible AI framework found publicly.

### Legal / regulatory
- **"Wrapper" controversy (May 2025):** Critics and media accused Sarvam of marketing Sarvam-M as a "sovereign Indian model" while it was a fine-tuned version of French company Mistral's model. Sarvam's position: post-training is legitimate R&D. Reputationally damaging but no legal action resulted.
- **Kaze glasses white-label allegations:** Critics allege Sarvam Kaze smart glasses are Chinese OEM hardware rebranded as "Made in India." Sarvam has not published bill of materials. Potential exposure under Make in India / PLI scheme regulations if hardware is not substantially manufactured domestically.
- **DPDP Act (India):** Sarvam stores and processes Indian citizens' voice and document data; compliance required under Digital Personal Data Protection Act 2023. Actively positioning as DPDP-aligned but audit details not public.
- **IndiaAI Mission equity grant:** A public commentator (Rahul Mathur on X) calculated that the government received ~₹148 crore in equity for ~₹247 crore in GPU access, implying ~60% recovery rate — raising questions about terms of the deal and whether the equity stake creates future complications (e.g., government rights, IP ownership of sovereign LLM).
- No known litigation or IP disputes as of May 2026.

### Churn signals
- No evidence of major customer churn. Tata Capital case study is published; UIDAI partnership ongoing.
- The "wrapper" controversy caused temporary community backlash but no reported enterprise customer losses.

## 9. Competitive Position

**Direct competitors:**
- **Speech/TTS/ASR:** ElevenLabs (global; premium; weak Indic), Murf AI (Indian; weaker Indic depth), Microsoft Azure Speech (22 Indic languages via Cognitive Services), Google Cloud TTS/STT (broad Indic), AWS Polly/Transcribe (limited Indic)
- **Indian-language LLMs / APIs:** Krutrim (Ola's AI; competing on LLM + voice), CoRover.ai (enterprise voice bots India), Gnani.ai (Indic ASR/voice), Yellow.ai (enterprise conversational AI)
- **Research/open-source ecosystem:** AI4Bharat (academic; not commercial; Sarvam's partner and origin), BHASHINI (government; not commercial; Sarvam's distribution channel)
- **Global LLMs with Indic support:** OpenAI GPT-4o, Google Gemini, Anthropic Claude, Meta Llama — all lack dedicated Indic fine-tuning depth and are cloud-dependent (not sovereign)

**Where it's winning:**
- Indic OCR/document intelligence: Sarvam Vision 84.3% accuracy on olmOCR-Bench beats Gemini Pro, GPT, DeepSeek on Indian-language benchmarks (claimed; Feb 2026)
- AI dubbing quality: In ~280 head-to-head comparisons, Sarvam Studio preferred over ElevenLabs, YouTube Dub, Rask AI by domain experts (claimed; Sarvam-published study)
- Government mandates: Only company with IndiaAI Mission sovereign LLM contract; UIDAI partnership; state-level MOU with Odisha and Tamil Nadu
- Indic LLM benchmarks: Sarvam-105B achieves 90% win rate on Indian language dimensions vs comparable models (claimed; not independently audited)
- Token efficiency: 2–4x more efficient tokenizer for Indic scripts vs generic multilingual tokenizers

**Where it's losing:**
- Global reasoning benchmarks: Sarvam-105B Math500 (98.6), AIME25 (88.3) are strong but frontier models (o3, Gemini Ultra) are ahead on general reasoning
- Developer community adoption: GitHub stars/forks modest for original repos; HF downloads lag global open-weight models at similar parameter counts
- Consumer brand awareness outside India
- Coding: User feedback consistently flags coding as a weak point vs Claude/GPT

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| May 2025 | Sarvam-M (24B) launched; faces "wrapper" controversy and download spike allegations | NewsBytesApp, AIM |
| May 2025 | Sarvam AI selected under IndiaAI Mission to build India's sovereign LLM; 4,096 H100 GPUs allocated | MeitY, MediaNama |
| Jun 2025 | Sarvam-Translate (22 languages, Gemma3-based) released on HuggingFace | HuggingFace model card |
| Aug 2025 | Bridge funding round (Avvanti Advisors); headcount at 114 | Tracxn |
| Mar 2025 | UIDAI partnership announced for Aadhaar AI voice integration | UIDAI press release |
| Feb 5 2026 | Sarvam Vision (3B VLM; 84.3% OCR accuracy) launched at India AI Impact Summit | BusinessToday |
| Feb 6 2026 | Odisha state MOU signed; 50MW AI data facility announced | BusinessToday |
| Feb 9 2026 | Tamil Nadu + IIT Madras Digital Sangam partnership announced | BusinessToday, ProjectsToday |
| Feb 12 2026 | Sarvam Studio (AI dubbing platform) launched | News9live |
| Feb 14–18 2026 | "14 launches in 14 days" blitz at India AI Impact Summit, Bharat Mandapam, New Delhi | MediaNama |
| Feb 17 2026 | Sarvam Kaze AI smart glasses unveiled; PM Modi demos them | Business Standard, Digit |
| Feb 18 2026 | Sarvam-30B and 105B open-sourced (Apache 2.0) | TechCrunch, Sarvam blog |
| Feb 20 2026 | Indus AI chatbot app launched on iOS, Android, web | TechCrunch |
| Mar 2026 | Sarvam Startup Program launched (API credits for early-stage companies) | TheHansIndia |
| Mar 30 2026 | Chanakya secure AI vertical unveiled for defence/government | BusinessToday, convergence-now.com |
| Apr 2026 | Series B (~$300–350M) at $1.5B valuation announced; investors include Nvidia, Amazon, Bessemer, HCLTech | Bloomberg, BW Businessworld |
| Apr/May 2026 | Pixxel partnership announced: India's first orbital AI data centre satellite "Pathfinder" (Q4 2026 launch) | Telecom Review Asia |
| May 2026 | Sarvam-M model released on HuggingFace (announced May 23 2026 via X) | Sarvam X/Twitter |
| May 2026 | Kaze glasses consumer launch expected | Multiple sources |

**Velocity verdict: Accelerating.** The company executed the most concentrated product release in Indian AI history (14 launches in 14 days in Feb 2026), secured unicorn status within 30 months of founding, won India's sovereign LLM mandate, and is closing the largest-ever private Indian AI fundraise. Momentum is high but sustained execution at this pace with a ~150-person team will be a test.

## 11. Bull Case / Bear Case

**Bull:**
- Sarvam is the structural beneficiary of India's Sovereign AI policy — government equity partner, compute access, and mandate insulate it from foreign competition in the public sector
- The only Indian company with end-to-end coverage: foundation models → speech/vision APIs → enterprise agents → consumer app → hardware — a true full-stack play
- 1.4B-person market with 22 language groups severely underserved by global AI; Sarvam's tokenizer efficiency and Indic corpus give it a durable technical edge for Indic-language use cases
- Series B ($350M) gives 2–3 years of runway to reach commercial scale; NVIDIA, Amazon, HCLTech as investors unlock compute, cloud distribution, and SI channel simultaneously
- BFSI + government verticals in India have long deployment cycles but high ACVs and very low churn once embedded (witness Tata Capital)

**Bear:**
- Revenue (₹29.1 crore FY2025) is tiny relative to $1.5B valuation (~52x revenue multiple) — needs dramatic commercial acceleration to justify valuation
- Open-source Apache 2.0 models remove API lock-in; competitors can fine-tune Sarvam-30B for free
- "Wrapper" controversy and HF download spike damaged credibility with the developer community at a critical growth phase
- Global frontier models (GPT, Gemini, Claude) are adding Indic language support and have vastly more resources; if they close the quality gap, Sarvam's moat narrows to government mandates
- Hardware ambition (Kaze) is speculative — smart glasses is a notoriously difficult product category; white-label hardware allegations could create regulatory risk under Make in India scheme
- Orbital AI satellite partnership with Pixxel is visionary but 2026 Q4 at the earliest — significant execution risk
- ~150-person team is thin for the breadth of products being maintained

## 12. What I Couldn't Find
- CIN (Corporate Identification Number) — not found in any public source; MCA portal search would require direct lookup
- Exact legal entity name registered with MCA (likely "Sarvam AI Private Limited" or similar, but not verified)
- Pre-money/post-money valuation for Dec 2023 Series A — not disclosed; only the $41M raise amount is public
- Specific TTFB (Time to First Byte) benchmarks for Bulbul v3 TTS or Saaras v3 ASR
- Detailed voice cloning minimum sample duration requirements
- Published SSML/emotion control API for Bulbul v3
- Official SOC 2 Type II audit report or ISO 27001 certification number (mentioned in enterprise marketing but not linked to a public certificate)
- Specific ASR word error rates (WER) by language published in a neutral benchmark
- Named advisors or board members beyond the two founders (board composition not public)
- ARR or GMV for FY2026
- Detailed breakdown of the IndiaAI Mission equity terms (only third-party calculations found)
- Whether Kaze glasses hardware is manufactured in India or is a Chinese OEM white-label (company has not published BOM)
- arXiv paper DOIs for any Sarvam model (no preprints found; all releases are via blog/HuggingFace)

## Sources
1. https://en.wikipedia.org/wiki/Sarvam_AI
2. https://www.sarvam.ai/
3. https://www.sarvam.ai/models
4. https://www.sarvam.ai/api-pricing
5. https://www.sarvam.ai/about-us
6. https://www.sarvam.ai/integrations
7. https://www.sarvam.ai/blogs/announcing-series-a
8. https://www.sarvam.ai/blogs/sarvam-1
9. https://www.sarvam.ai/blogs/sarvam-m
10. https://www.sarvam.ai/blogs/sarvam-30b-105b
11. https://www.sarvam.ai/blogs/bulbul-v3
12. https://www.sarvam.ai/blogs/sarvam-studio
13. https://www.sarvam.ai/blogs/indias-sovereign-llm
14. https://www.sarvam.ai/blogs/partnerships-with-indian-states
15. https://www.sarvam.ai/stories/tata-capital-ai-voice-transformation
16. https://www.sarvam.ai/partnerships/pixxel
17. https://techcrunch.com/2023/12/06/indias-sarvam-ai-raises-41-million-from-lightspeed-khosla-peak-xv/
18. https://techcrunch.com/2026/02/18/indian-ai-lab-sarvams-new-models-are-a-major-bet-on-the-viability-of-open-source-ai/
19. https://techcrunch.com/2026/02/20/indias-sarvam-launches-indus-ai-chat-app-as-competition-heats-up/
20. https://techcrunch.com/2026/02/18/indias-sarvam-wants-to-bring-its-ai-models-to-feature-phones-cars-and-smart-glasses/
21. https://www.bloomberg.com/news/articles/2026-04-02/india-ai-startup-sarvam-raises-funds-at-1-5-billion-valuation
22. https://www.businessworld.in/article/sarvam-ai-350-million-funding-bessemer-nvidia-amazon-2026-600618
23. https://inc42.com/features/sarvam-and-the-sovereign-ai-dream/
24. https://www.medianama.com/2025/04/223-india-sovereign-llm-sarvam-ai-government-funding-not-open-source-but-proprietary/
25. https://www.medianama.com/2026/02/223-here-what-companies-unveiled-at-india-ai-impact-summit-2026/
26. https://uidai.gov.in/en/media-resources/media/press-releases/18688-uidai-partners-with-indigenous-genai-company-sarvam-ai-to-enhance-user-experience-of-aadhaar-services.html
27. https://techobserver.in/news/egov/bhashini-platform-600-crore-requests-sarvam-models-321387/
28. https://www.pib.gov.in/PressReleasePage.aspx?PRID=2231169&reg=3&lang=1
29. https://huggingface.co/sarvamai
30. https://huggingface.co/sarvamai/sarvam-30b
31. https://huggingface.co/sarvamai/sarvam-105b
32. https://huggingface.co/sarvamai/sarvam-m
33. https://huggingface.co/sarvamai/sarvam-translate
34. https://huggingface.co/sarvamai/shuka-1
35. https://github.com/orgs/sarvamai/repositories
36. https://github.com/sarvamai/sarvam-ai-cookbook
37. https://github.com/pipecat-ai/pipecat/issues/3783
38. https://tracxn.com/d/companies/sarvam/__pdMzZ7Rkxe_acM5ctqBwOaZ9aoqOdLTKSvAsHq-7kFw
39. https://www.marktechpost.com/2024/08/14/sarvam-ai-releases-samvaad-hi-v1-dataset-and-sarvam-2b-a-2-billion-parameter-language-model-with-4-trillion-tokens-focused-on-10-indic-languages-for-enhanced-nlp/
40. https://developer.nvidia.com/blog/how-nvidia-extreme-hardware-software-co-design-delivered-a-large-inference-boost-for-sarvam-ais-sovereign-models/
41. https://www.business-standard.com/technology/tech-news/sarvam-105b-model-sovereign-ai-india-foundation-model-launch-impact-summit-126021900551_1.html
42. https://www.business-standard.com/companies/start-ups/sarvam-ai-story-history-founders-pratyush-kumar-vivek-raghavan-126021900804_1.html
43. https://www.businesstoday.in/technology/news/story/sarvam-ai-unveils-sarvam-vision-a-multilingual-document-intelligence-model-514873-2026-02-05
44. https://www.businesstoday.in/technology/news/story/sarvam-takes-on-elevenlabs-with-ai-dubbing-push-for-indian-languages-514203-2026-02-02
45. https://www.businesstoday.in/technology/story/sarvam-ai-unveils-chanakya-vertical-for-critical-high-security-ai-needs-523050-2026-03-30
46. https://www.businesstoday.in/technology/news/story/sarvam-ai-partners-with-odisha-and-tamil-nadu-to-build-national-compute-grid-515267-2026-02-09
47. https://www.analyticsvidhya.com/blog/2025/05/bulbul-v2-by-sarvam/
48. https://analyticsindiamag.com/ai-features/bhashini-ai4bharat-and-sarvam-might-finally-solve-indias-language-divide/
49. https://analyticsindiamag.com/ai-features/sarvam-ais-backlash-exposes-the-sad-state-of-indian-ai/
50. https://www.avidclan.com/blog/sarvam-ai-sovereign-language-tax/
51. https://www.newsbytesapp.com/news/science/sarvam-ai-s-new-language-model-draws-muted-response-heavy-criticism/story
52. https://www.outlookbusiness.com/start-up/news/sarvams-indic-ai-model-hype-hope-and-the-hunt-for-tech-sovereignty
53. https://deepmind.google/models/gemma/gemmaverse/sarvam-ai/
54. https://aws.amazon.com/marketplace/pp/prodview-x5iks3edtmaio
55. https://scholar.google.com/citations?user=4pr87jAAAAAJ&hl=en
56. https://www.xrom.in/post/sarvam-kaze-ai-smart-glasses-india-launch-galgotias-controversy-white-label-reality-check
57. https://www.telecomreviewasia.com/news/network-news/29147-pixxel-sarvam-launch-indias-first-orbital-ai-satellite/
58. https://in.linkedin.com/in/vivek-raghavan-16005424
59. https://docs.sarvam.ai/api-reference-docs/integration/build-voice-agent-with-pipecat
60. https://docs.sarvam.ai/api-reference-docs/integration/build-voice-agent-with-live-kit
