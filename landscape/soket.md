# Soket AI Labs

**Website:** https://soket.ai  •  **HQ:** Gurugram, Haryana, India  •  **Founded:** December 2019  •  **Stage:** Seed
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): India-first AI lab building open-source multilingual foundation models (Pragna / Project EKA) and a real-time speech API (TensorStudio) that serve Indian-language voice agents at sub-$0.012/min pricing.
- Total funding to date: ~$2.35M private + ₹177.08 Cr (~$21M) IndiaAI Mission government grant (non-dilutive compute + ancillary)
- Last round: $2.2M Seed — March 19, 2026 — Lightspeed India, Together Fund (+ 3 undisclosed)
- Headcount: ~15 employees as of Sep 2025 (was ~10 mid-2024; +50% in 12 months); also 20+ individuals and 8+ academic/partner orgs via Project EKA
- Revenue / ARR: Not publicly disclosed. TensorStudio (voice API at $0.012/min) is primary revenue stream; customers reported in BFSI; no ARR figure public.

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| 2024 (approx.) | Angel | $150K | Undisclosed | Undisclosed | Inc42 |
| Mar 19, 2026 | Seed | $2.2M | Lightspeed India | Together Fund + 2 VC + 1 strategic (undisclosed) | SignalBase |
| 2025 (announced May 2025) | Govt Grant / IndiaAI Mission | ₹177.08 Cr (~$21M non-dilutive, compute + 25% ancillary) | MeitY / IndiaAI Mission | N/A — government scheme | Inc42, APAC News Network |

**Notes:**
- The ₹177.08 Cr grant covers actual GPU compute costs for training Project EKA 120B, plus 25% for datasets and personnel. It is structured as financial assistance (equity + debt blend per original reporting), not a direct cash transfer.
- Soket publicly stated a target of $15M Series A "in the coming months" (as of ~H1 2024 Inc42 coverage); no confirmed close as of 2026-05-10.
- Earlier Inc42 article references an additional planned $7M seed raise; relationship to the confirmed $2.2M seed unclear — likely the same round reported at different stages.

## 3. Product & Customers

### Products

**1. Pragna-1B** (launched April 30, 2024)
- Open-source multilingual LLM, 1.25B parameters, Apache 2.0 license
- Decoder-only transformer; 22 layers, 32 attention heads, 2048 context length, vocab 69,632
- Languages: Hindi, Gujarati, Bangla, English
- Training: ~150B tokens (Bhasha-wiki, SlimPajama, Sangraha-Verified)
- Available on Hugging Face (soketlabs/pragna-1b) and Microsoft Azure AI Foundry catalog
- Tokenizer efficiency: ~2.85 tokens/word for Kannada vs. Gemma-7b's 5.8 (claimed 2x throughput gain from tokenization alone); 3–6.5x speed over Llama-2-7B for Indic languages

**2. BHASHA Series Models** (on HuggingFace, partially released)
- `bhasha-7b-8k-hi-base`: 7B param, 8K context, Hindi-only pre-trained
- `bhasha-7b-8k-base`: 7B param, 8K context, pre-trained on 22 scheduled Indian languages
- `bhasha-7b-8k-instruct`: Instruction-tuned variant
- `Indic-Llama-2-7b`: Fine-tuned Llama-2 for Indic languages

**3. SARTHI / sarthi-agri-v1** (on HuggingFace)
- 29B parameter text-generation model (verified on HF)
- Focused on agriculture advisory use cases; showcased at India AI Impact Summit 2026
- Target: vernacular farmer advisories (Rajasthan, Karnataka contexts noted in coverage)

**4. Gemma-3-Dhvani** (on HuggingFace, 1B)
- 1B parameter text generation model; fine-tuned on Hindi/Indic data; 2 likes on HF

**5. TensorStudio** (https://tensorstudio.ai)
- Real-time Speech API powered by Pragna model — primary commercial revenue vehicle
- Sub-500ms TTFB latency (claimed); $0.012/minute pricing
- Features: multilingual voice agents, tool calling, RAG-backed responses, conversation analytics, voice interruption handling, custom voice creation/cloning
- SDKs: Python and Node.js (GitHub repos: soketlabs/realtime-sdk-python, soketlabs/plivo-integration)
- Integration time claimed: 1–4 weeks

**6. DHRITH** (launched November 6, 2025)
- India's first emotion-aware ASR system; developed under Project EKA
- Features: emotion tagging, code-mixed Hindi-English fluency, speaker diarisation, context-aware transcription
- Benchmarked on CoSHE-Eval (their own dataset); API access forthcoming for developers/enterprise

**7. Project EKA** (https://eka.soket.ai) — in development
- Target: 100B+ parameter Sparse MoE foundation model, instruction-tuned
- Training corpus target: 2T+ tokens for Indic languages (20 trillion tokens mentioned in some coverage)
- Open-source weights release planned under unrestricted license
- Collaborators: IIT Gandhinagar, IIT Roorkee (formal MoU with IIT Roorkee confirmed)
- Government backing: ~1,500–18,000 GPUs allocated (conflicting reports; confirmed H100 access via IndiaAI GPU pool)
- Timeline: phased (1B → 7B → 120B); 7B expected ~6 months from late 2024

**8. COOM Training Framework** (open source)
- Megatron-Core-based LLM training framework inspired by DeepSeek's HAI-LLM
- Targets FP8, MoE, Multi-Head Latent Attention, Multi-Token Prediction
- 26 stars, 6 forks; Python; website eka.soket.ai

### Pricing
| Product | Price | Notes |
|---------|-------|-------|
| TensorStudio Realtime Speech API | $0.012/minute | Publicly listed on website |
| Pragna-1B model weights | Free (Apache 2.0) | Self-host or via HF |
| BHASHA series weights | Free (HF) | Partial release; licenses vary |
| Project EKA (planned) | Open-source weights free | Commercial API TBD |

Free tier: Not explicitly stated. Contact sales model implied for TensorStudio enterprise.

### Languages & Voices
- **LLM languages (Pragna-1B):** Hindi, Gujarati, Bangla, English (4)
- **Tokenizer training languages:** Hindi, Bangla, Urdu, Tamil, Kannada, Gujarati (6)
- **BHASHA-7B-8K-Base:** 22 scheduled Indian languages (per HF card)
- **Project EKA target:** 6 scripts, 20–22 languages
- **TensorStudio voices:** Multiple voice styles (friendly, authoritative, empathetic) — specific voice list not publicly documented
- **DHRITH ASR:** Hindi-English code-switching; regional accents (Haryanvi, UP Hindi, South Indian); emotion tagging

### Named Customers
- No named enterprise customers with public case studies found.
- Vertical focus confirmed: BFSI (banking, financial services, insurance), healthcare, telecom, edtech
- Agriculture advisory (sarthi-agri) implied for Karnataka/Rajasthan government contexts
- Inc42 confirms banking sector is currently active, with insurance, healthcare, telecom, edtech as expansion targets

### Integrations / SDKs
- Plivo telephony integration (soketlabs/plivo-integration)
- Python SDK (soketlabs/realtime-sdk-python — port of OpenAI Realtime API beta)
- Node.js SDK (separate GitHub repo)
- Microsoft Azure AI Foundry (Pragna-1B listed in catalog)
- Google Cloud (Pragna-1B pre-training partnership; Soket listed as Gemma-based solution at Google I/O India 2025)

## 4. Technical Architecture

### Model approach
- Pragna-1B: Decoder-only transformer (TinyLlama-inspired), custom BPE tokenizer covering 6 Indian scripts; Grouped Query Attention; FlashAttention2; Rotary Positional Encoding
- BHASHA-7B: Fine-tuned 7B transformer on 22 Indian languages, 8K context
- Project EKA: Sparse Mixture-of-Experts (Sparse MoE), targeting 120B+ parameters; training on NVIDIA Megatron + NeMo stack via COOM framework
- Inference: NVIDIA NeMo / Megatron stack on A100/H100 GPUs (IndiaAI GPU pool)

### Training data
| Dataset | Scale | Languages | License | Notes |
|---------|-------|-----------|---------|-------|
| bhasha-wiki | 44.1M articles, 45.1B Indic tokens, 117 GiB | Hindi, Gujarati, Urdu, Tamil, Kannada, Bengali | CC-BY-SA 3.0 | Translated from 6.3M English Wikipedia articles using IndicTrans2; 3,360 GPU-hours on AWS |
| bhasha-wiki-indic | 200,820 rows, 1.54B tokens | Same 6 | CC-BY-SA 3.0 | India-context curated subset; 84% semantic filtering accuracy |
| bhasha-sft | 13M+ instruction-response pairs | Hindi, Gujarati, Bengali, English | See HF | For supervised fine-tuning; 18.1M downloads on HF |
| SlimPajama | 627B tokens | English (primary) | Open | External; used in Pragna-1B training |
| Sangraha-Verified | 15M tuples | Indic | Open (AI4Bharat) | Used in Pragna-1B training |
| SARTHI-AgriData | 220K rows | Indic (agri domain) | See HF | 52 likes on HF; used for agriculture model |
| CoSHE-Eval | 1,985 clips, ~30 hours | Hindi-English code-switched | Research-only, non-commercial | ASR benchmark; Nov 2025 |
| Project EKA corpus (planned) | 2T–20T tokens | 20–22 Indic languages | TBD | OCR, ASR, synthetic data pipeline; IIT Gandhinagar collaboration |

### Latency profile
- TensorStudio Speech API: Sub-500ms TTFB (claimed); "natural dialogue" target
- Pragna-1B tokenizer: ~3x–7x faster token generation vs. Llama-2-7B for Indic languages (due to more efficient tokenization alone)
- No published RTF (real-time factor) for TTS/ASR components

### Voice cloning
- TensorStudio supports custom voice creation and cloning (per website copy); technical specs not public

### Prosody / emotion control
- DHRITH ASR captures emotion tags (`[excited]`, `[sarcastically]`, etc.) and tone annotations
- Pitch and pace metadata included in CoSHE-Eval benchmark
- Full TTS prosody/emotion control specs not publicly documented

### Indic language strategy
- "Balanced tokenization" — custom BPE tokenizer trained across 6 Indian scripts before merging into unified tokenizer; reduces fertility score (tokens per word) dramatically vs. GPT-4o/Gemma for Kannada, Tamil, Urdu, Gujarati
- Training data prioritizes India-originated content via bhasha-wiki-indic curation
- Code-switching focus (DHRITH, CoSHE-Eval) recognizes Hindi-English code-mixed speech as primary enterprise use case
- Agriculture domain specialization (SARTHI) for vernacular farmer advisories

### Inference stack
- NVIDIA Megatron-Core (via COOM framework) for training
- Text Generation Inference (TGI) for HuggingFace / Azure Foundry deployment
- TensorStudio hosted API (cloud inference; self-hosted path not publicly documented)

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Introducing "Bhasha" Indic Language AI Datasets | Blog | Apr 17, 2024 | https://soket.ai/blogs/bhasha_wiki |
| Availability of the Bhasha SFT Dataset | Blog | Apr 19, 2024 | https://soket.ai/blogs/ |
| Introducing Pragna-1B: Soket AI Labs' Multilingual LLM | Blog / Model Card | Apr 30, 2024 | https://soket.ai/blogs/pragna_1b |
| Dhrith: Emotionally Intelligent ASR for India's Multilingual Voices | Blog | Nov 6, 2025 | https://soket.ai/blogs/ |
| CoSHE-Eval: A Code-Switching ASR Benchmark for Hindi–English Speech | Blog / Dataset | Nov 12, 2025 | https://soket.ai/blogs/coshe_eval |

No arXiv papers found under "Soket AI Labs" affiliation as of 2026-05-10. Research output has been primarily blog posts and HuggingFace model/dataset releases.

## 5. Open Source Footprint

### GitHub
**Org:** https://github.com/soketlabs (verified — 19 public repos)

| Repo | Stars | Forks | License | Last commit (approx.) | Notes |
|------|-------|-------|---------|-----------------------|-------|
| coom | 26 | 6 | None listed | Active (94 commits) | Megatron-Core-based LLM training framework; FP8, MoE, MLA support; for Project EKA |
| llm-foundry | 2 | — | None listed | Active | LLM training code for foundation models |
| plivo-integration | 1 | — | None listed | Recent | Plivo ↔ TensorStudio relay server; JS |
| realtime-sdk-python | — | — | MIT (inherited) | Recent | Python port of OpenAI Realtime API beta |
| telephony-agent-container | — | 0 | None listed | Recent | Telephony + tool-calling agent container; JS |
| soket-webui-interface | — | 0 | None listed | — | Demo UI for agri model |
| soket-website | — | 0 | None listed | — | Company website (MDX) |
| docs | — | 0 | None listed | — | Documentation (MDX) |
| opencode (fork) | — | 18,553 forks | MIT | — | Forked upstream open-source coding agent |
| models.dev (fork) | — | 941 forks | MIT | — | Forked AI models database |
| litgpt (fork) | — | 1,461 forks | Apache-2.0 | — | Forked LLM training repo |

**Community signal:** Low GitHub stars overall (max 26 on coom); most engagement is on HuggingFace datasets rather than code.

### Hugging Face
**Org:** https://huggingface.co/soketlabs (verified)

**Models (9):**
| Model | Downloads (last month) | Likes | License | Notes |
|-------|----------------------|-------|---------|-------|
| pragna-1b | ~200 | 21 | Apache 2.0 | Flagship 1.25B multilingual model |
| sarthi-agri-v1 | 64 | 3 | — | 29B agri advisory model |
| bhasha-7b-8k-hi | 16 | 3 | — | Hindi-only 7B |
| bhasha-7b-256-hi | 17 | 4 | — | Hindi 7B, 256 context |
| bhasha-7b-2k-hi | 26 | 2 | — | Hindi 7B, 2K context |
| Indic-Llama-2-7b | 8 | 1 | — | Llama-2 7B Indic fine-tune |
| pragna-1b-it-v0.1 | — | 1 | — | Instruction-tuned Pragna-1B v0.1 |
| gemma-3-dhvani | — | 2 | — | 1B Hindi Gemma-3 fine-tune |
| whisper_indic_hi_ai4bharat | 17 | 1 | — | Whisper fine-tune for Hindi |

**Datasets (8):**
| Dataset | Downloads | Likes | Notes |
|---------|-----------|-------|-------|
| bhasha-wiki | 44.4M | 1.1k | Flagship dataset; highest community traction |
| bhasha-sft | 18.1M | 270 | SFT instruction pairs |
| bhasha-wiki-indic | 1.41M | 209 | India-curated subset |
| SARTHI-AgriData | 220k | 52 | Agriculture domain |
| CoSHE-Eval | 1.99k | 263 | Hindi-English ASR benchmark; research-only license |
| bhasha-wiki-translated | 160k | 117 | Translated Wikipedia |
| bhasha-wiki-indic-context | 101k | 102 | Contextual subset |
| indic_qna_v1 | 149k | 5 | QnA pairs |

**Spaces (3):** Pragna Audio Chatbot, Pragna Chat, Multilingual Audio Pragna ChatBot

**Community signal:** bhasha-wiki (1.1k likes, 44.4M downloads) and bhasha-sft (270 likes, 18.1M downloads) are genuine community assets — among the most-used open Indic language datasets. CoSHE-Eval (263 likes) gaining traction.

### Top contributors
- Abhishek Upperwal (CEO/Founder) — primary GitHub committer (github.com/upperwal)
- Siddhant Panda (Principal Data Scientist) — confirmed team member
- Sandipan Ray — confirmed team member (LinkedIn)
- Mayank Singh — IIT Gandhinagar collaborator (academic partner, not direct employee)
- Additional contributors not publicly visible (org members not listed)

## 6. Team

### Founders
- **Abhishek Upperwal** — Founder & CEO
  - LinkedIn: https://www.linkedin.com/in/upperwal/
  - Education: M.Tech/PhD in Computational and Data Sciences, IISc Bangalore (2018); specialization in High-Performance Computing and Distributed Systems
  - Background: Data scientist; worked on Smart Cities Mission post-IISc; incorporated Soket Labs Dec 2019 but company remained dormant until ~2022–2023
  - Motivation: Sam Altman's June 2023 "hopeless" remark about India building frontier AI catalyzed Upperwal's pivot to LLM development
  - GitHub: https://github.com/upperwal

- **Rajesh Rani** — Co-director (MCA filing; role not publicly described)
  - Listed as director in MCA/Zaubacorp records alongside Upperwal; no LinkedIn or public profile found

### Key technical hires
| Name | Role | LinkedIn |
|------|------|---------|
| Siddhant Panda | Principal Data Scientist | https://www.linkedin.com/in/siddhant-panda-85a24aa6/ |
| Sandipan Ray | Team member (role unconfirmed) | https://in.linkedin.com/in/sandipan-ray-147796145 |

Note: Inc42 article lists additional names (Mayank Chawla, Soumya Kochhar, Ritwika Das Gupta, Sayantan Ray, Rohitaash Debsharma, M Bharath) as part of the broader team. Roles not confirmed.

### Recent joiners (last 12mo)
- Company actively recruiting two Project EKA co-founders (per Inc42 reporting, ~H2 2024)
- Headcount grew from ~10 (mid-2024) to ~15 (Sep 2025), implying 5+ hires in 12 months
- Specific recent joiner names not publicly available

### Notable departures (last 12mo)
- Not publicly available; no departure reports found

### Open roles signal
- Careers email: careers@soket.ai
- Hiring for AI scientists, engineers (stated in $2.2M seed press release context)
- No structured job board found on soket.ai as of research date

## 7. Moat & Defensibility

- **Data moat:** Strong — bhasha-wiki (44.1M multilingual Wikipedia translations, 45.1B Indic tokens) and bhasha-sft (13M+ instruction pairs) are among the largest open Indic LLM datasets. CoSHE-Eval is the only standardized Hindi-English code-switching ASR benchmark. SARTHI-AgriData adds domain-specific vertical depth. 1.1k HF likes on bhasha-wiki confirms genuine community value. Data pipeline uses IndicTrans2 + OCR/ASR/synthetic data for Project EKA corpus targeting 2T+ tokens.

- **Model moat:** Moderate — Pragna tokenizer efficiency (2.26 tokens/word Hindi vs. 3–6x worse for GPT-4/Gemma) is a genuine architectural innovation. However, Pragna-1B benchmarks (Arc ~0.30, HellaSwag ~0.35) show modest absolute performance; advantage is efficiency, not raw capability. Project EKA 120B could shift this if delivered.

- **Distribution moat:** Moderate-to-growing — Government selection under IndiaAI Mission grants credibility, GPU access, and likely preferential positioning for public-sector deployments (defence, agriculture, education, governance). TensorStudio's telephony integrations (Plivo) target BFSI contact centers where switching cost is high. Azure AI Foundry listing provides enterprise distribution channel.

- **Brand / community moat:** Moderate — bhasha-wiki/sft datasets are widely cited in Indic NLP community. "India's first open-source multilingual model" positioning (Pragna-1B) established early mindshare. Abhishek Upperwal is visible on conference circuit (NASSCOM TLF, Global India AI Summit, AIM Cypher 2025). GitHub star count is low but HuggingFace engagement is meaningful.

- **Regulatory moat:** Growing — One of only 4 startups selected under MeitY's ₹10,372 Cr IndiaAI Mission. This creates quasi-regulatory moat: government alignment, priority GPU access, and potential for procurement preferences in public-sector AI. Defence sector ambitions could trigger DPDP / security clearance requirements that favor incumbents.

- **Replication cost (6mo, $10M competitor):** A well-funded competitor could replicate bhasha-wiki-class datasets using IndicTrans2 in ~3–6 months, and fine-tune open-source 7B–13B models competitively. However, replicating the IndiaAI Mission relationship, government GPU allocation, and the community trust around bhasha-wiki within 6 months would be extremely difficult. TensorStudio's BFSI customer integrations add switching-cost protection. Estimate: $3–5M to replicate technical assets; impossible to replicate government position quickly.

- **Moat strength: 3/5** — Strong data and government-access moat for India's Indic NLP market; model capabilities still maturing and not yet frontier-class; distribution moat depends on Project EKA delivery.

## 8. Risks & Problems

### Technical complaints
- No Reddit, HN, or GitHub issue discussions found criticizing Soket AI's products specifically (low volume suggests limited production deployment at scale)
- Pragna-1B benchmarks are self-reported; third-party independent evals not found
- Inc42 notes that Soket faced GPU delivery delays from IndiaAI Mission ("delays in receiving promised GPU support from the government") — slowing Project EKA timeline
- Bhasha-wiki uses machine translation (IndicTrans2), which is noted in multiple sources as a limitation: "quality of benchmarking data is currently suboptimal, largely stemming from the reliance on datasets generated through machine translations"
- Pragna-1B GSM8K score = 0 (math reasoning essentially absent); context length only 2048 tokens (short for enterprise tasks)

### Pricing pain points
- No public pricing complaints found; $0.012/min pricing is competitive vs. ElevenLabs (~$0.15/min), Deepgram (~$0.005/min for ASR-only), Assembly AI
- Limited transparency on enterprise tier pricing beyond base rate

### Safety / misuse
- Company emphasizes "ethical AGI" and "Building AGI with a Conscience" — safety is part of brand identity
- No specific safety incident reports found
- CoSHE-Eval uses a research-only, non-commercial license — limiting commercial misuse of benchmark
- Risks in agriculture/defence domains if models produce hallucinated crop advice or incorrect information in low-resource language contexts

### Legal / regulatory
- No litigation found
- MCA/Zaubacorp records show authorized capital ₹10 lakh, paid-up ₹1.06 lakh — minimal capitalization pre-2024; raises no red flags but shows company was shell until recently
- CIN: U72900HR2019PTC078548 — incorporated Dec 14, 2019 in Haryana
- Government grant structure (equity + debt blend per early reporting) may create future dilution or repayment obligations — exact terms not public

### Churn signals
- No churn signals found (insufficient public customer base data)
- Small team (15 people) managing ambitious 120B model development is a key execution risk

## 9. Competitive Position

- **Direct competitors:**
  - Sarvam AI (Bengaluru) — better-funded, more team, also IndiaAI Mission selected, has released 30B and 105B models; stronger in ASR/TTS breadth
  - Krutrim (Ola) — corporate-backed, Krutrim-2 at 12B params, distribution advantage via Ola ecosystem
  - Gnani.ai — also IndiaAI Mission selected; specialized in voice AI, 14B voice model; more enterprise BFSI traction
  - AI4Bharat (IIT Madras research lab) — foundational Indic NLP datasets/models; Soket uses some of their data
  - Reverie Language Technologies — enterprise Indic NLU/translation
  - Gan.ai — IndiaAI Mission selected; 70B multilingual model with TTS focus
  - Global: OpenAI, Google (Gemini), Anthropic — Soket explicitly positions as India-sovereign alternative

- **Where it's winning:**
  - Largest open Indic LLM pre-training dataset (bhasha-wiki) in the community
  - First published Hindi-English code-switching ASR benchmark (CoSHE-Eval)
  - Real-time speech API at competitive pricing for BFSI contact centers
  - Government validation and GPU allocation under IndiaAI Mission
  - Efficient tokenization for low-resource Indian languages (Kannada, Tamil, Urdu, Gujarati)
  - Azure AI Foundry marketplace presence gives enterprise distribution

- **Where it's losing:**
  - Raw model capability: Sarvam's 105B model (released 2026) outclasses Pragna-1B; Krutrim-2 has more parameters
  - Team size: 15 vs. Sarvam's larger headcount and VC backing
  - Language breadth: Pragna-1B supports only 4 languages; Sarvam targets 22
  - No named enterprise customers with public case studies (trust-building at early stage)
  - GitHub community engagement (26 max stars) vs. AI4Bharat/Sarvam open-source visibility

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| Apr 2024 | Launched bhasha-wiki and bhasha-wiki-indic datasets on HuggingFace | soket.ai blog |
| Apr 30, 2024 | Launched Pragna-1B — "India's first open-source multilingual LLM" — with Google Cloud | Business Standard, Analytics India Magazine |
| May 2024 | Pragna-1B listed in Microsoft Azure AI Foundry model catalog | ai.azure.com |
| May 2025 | MeitY selects Soket AI Labs alongside Sarvam, Gnani, Gan.ai for IndiaAI Mission 120B LLM development | Inc42, APAC News Network |
| May 2025 | Soket announced ₹177.08 Cr IndiaAI Mission grant (compute + ancillary) | Multiple sources |
| May 2025 | Google I/O India 2025: Soket listed as Gemma-based solution builder alongside Sarvam and Gnani.ai | Analytics India Magazine |
| Jun 2025 | AIM reports Project EKA phased roadmap (1B→7B→120B within 10 months) with Upperwal quotes | X/@Analyticsindiam |
| Nov 6, 2025 | Launched DHRITH: India's first emotion-aware ASR system | soket.ai blog, AIM, CXO DigitalPulse |
| Nov 12, 2025 | Published CoSHE-Eval: first Hindi-English code-switching ASR benchmark (30 hours, 1,985 clips) | soket.ai blog, HuggingFace |
| Mar 19, 2026 | Closed $2.2M Seed round led by Lightspeed India and Together Fund | SignalBase |
| Feb 2026 | Showcased EKA, DHRITH, SARTHI, TensorStudio at India AI Impact Summit 2026 (New Delhi) | LinkedIn posts, India AI Impact Summit |

**Velocity verdict:** Accelerating. After a slow 2019–2023 period, the company has shipped four distinct product lines (Pragna, TensorStudio, DHRITH, SARTHI) in 18 months, secured government backing worth ~$21M in compute credits, closed institutional seed funding, and built the most-used open Indic NLP datasets on HuggingFace. Execution risk remains high given team size and Project EKA ambitions, but momentum through early 2026 is strong.

## 11. Bull Case / Bear Case

**Bull:**
Soket wins as the government-aligned open-source Indic AI lab. The bhasha-wiki/sft datasets become the standard pre-training corpus for Indian LLMs (community lock-in). Project EKA's 120B model ships in 2026 as the first fully open-source frontier Indic model, triggering enterprise and government procurement. TensorStudio captures BFSI contact-center spend where Indian-language voice accuracy beats AWS/Azure. IndiaAI Mission GPU access and ₹177 Cr grant let a 15-person team punch 10x above their weight. Lightspeed backing catalyzes Series A at $50M+ as EKA ships.

**Bear:**
Soket gets outcompeted by Sarvam AI (better-funded, larger team, already at 105B parameters) and Krutrim (telco distribution moat). Project EKA delays continue due to government GPU logistics and team bandwidth. Pragna-1B remains the only production model with modest benchmarks; TensorStudio churn accelerates as Sarvam's voice API matures. The $2.2M seed is insufficient to build a 120B model without government compute being reliably delivered. The 15-person team cannot execute simultaneously on model training, data curation, SDK development, and enterprise sales.

## 12. What I Couldn't Find
- Exact ARR / revenue figure for TensorStudio
- Named enterprise customers with verified case study links
- Full investor names for 3 of 5 participants in $2.2M seed round
- Rajesh Rani's background and role (MCA co-director)
- CTO designation (none publicly confirmed)
- Specific voice count in TensorStudio (website says "diverse voices" without enumeration)
- IndiaAI Mission grant disbursement status (whether GPUs have been received)
- Project EKA 7B model release status (expected ~H1 2025 per Inc42 reporting — not confirmed released as of May 2026)
- Any arXiv preprints under Soket AI affiliation
- Bhashini or ONDC direct integration (no evidence found; Soket is adjacent to these ecosystems but no formal integration confirmed)
- Advisory board composition (none publicly listed)
- Detailed DHRITH technical specs (WER benchmarks, language coverage beyond Hindi-English)

## Sources
1. https://soket.ai — Company website (verified)
2. https://soket.ai/llm — Products page (verified)
3. https://soket.ai/blogs/pragna_1b — Pragna-1B blog post / technical details (verified)
4. https://soket.ai/blogs/bhasha_wiki — Bhasha dataset blog (verified, Apr 17, 2024)
5. https://soket.ai/blogs/coshe_eval — CoSHE-Eval blog (verified, Nov 12, 2025)
6. https://soket.ai/blogs — Full blog index (verified)
7. https://eka.soket.ai — Project EKA page (verified)
8. https://tensorstudio.ai — TensorStudio product page (verified)
9. https://docs.tensorstudio.ai/sdk/overview — TensorStudio SDK docs (verified)
10. https://github.com/soketlabs — GitHub organization (verified; 19 repos)
11. https://github.com/soketlabs/coom — COOM framework repo (verified; 26 stars, 6 forks)
12. https://huggingface.co/soketlabs — HuggingFace organization (verified; 9 models, 8 datasets, 3 spaces)
13. https://huggingface.co/soketlabs/pragna-1b — Pragna-1B model card (verified; Apache 2.0; 200 downloads/mo; 21 likes)
14. https://huggingface.co/datasets/soketlabs/CoSHE-Eval — CoSHE-Eval dataset (verified; 263 likes)
15. https://inc42.com/startups/can-soket-ai-power-indias-foundational-llm-dream/ — Inc42 deep-dive profile (primary source for company history, funding, team)
16. https://inc42.com/buzz/indiaai-mission-soket-ai-gnani-ai-gan-ai-to-develop-indigenous-ai-models/ — IndiaAI Mission selection coverage
17. https://www.trysignalbase.com/news/funding/soket-ai-labs-raises-22m — $2.2M seed round details; Lightspeed India + Together Fund confirmed (verified)
18. https://www.business-standard.com/technology/tech-news/soket-ai-labs-launch-pragna-1b-ai-model-in-collaboration-with-google-cloud-124051500685_1.html — Pragna-1B + Google Cloud launch (Business Standard)
19. https://apacnewsnetwork.com/2025/04/sarvam-ai-soket-ai-labs-among-first-to-be-backed-under-rs-10000-cr-indiaai-mission/ — IndiaAI Mission first selection round
20. https://startuppedia.in/trending/trending/govt-selects-3-more-startupssoket-ai-labs-gnani-ai-and-gan-ai-to-build-llms-under-india-ai-mission-9324005 — Second cohort selection
21. https://analyticsindiamag.com/ai-news-updates/soket-ai-labs-launches-realtime-speech-api-offers-multilingual-capabilities/ — TensorStudio speech API launch
22. https://www.zaubacorp.com/SOKET-LABS-TECHNOLOGY-AND-RESEARCH-PRIVATE-LIMITED-U72900HR2019PTC078548 — MCA registration details; CIN U72900HR2019PTC078548; directors: Rajesh Rani + Abhishek Upperwal (403 returned but data extracted from search snippets)
23. https://www.linkedin.com/in/upperwal/ — Abhishek Upperwal LinkedIn
24. https://www.linkedin.com/in/siddhant-panda-85a24aa6/ — Siddhant Panda (Principal Data Scientist) LinkedIn
25. https://in.linkedin.com/in/sandipan-ray-147796145 — Sandipan Ray LinkedIn
26. https://ai.azure.com/catalog/models/soketlabs-pragna-1b — Pragna-1B on Microsoft Azure AI Foundry
27. https://indiaai.gov.in/article/soket-ai-lab-s-bhasha-series-to-support-models-attuned-to-indian-languages — IndiaAI gov coverage of Bhasha series
28. https://analyticsindiamag.com/ai-news-updates/soket-ai-labs-unveils-dhrith-indias-emotion-aware-speech-recognition-system/ — DHRITH launch
29. https://aihubblog.com/soket-ai-labs-dhrith-voice-recognition/ — DHRITH secondary coverage
30. https://macgence.com/blog/project-eka-driving-the-future-of-ai-in-india/ — Project EKA overview
31. https://tracxn.com/d/companies/soket-ai/__T1WEKQib0Arvt0k8IwYGmjM2lIRL9MLPNhBZPuXLnfE — Tracxn profile (headcount: 15 as of Sep 2025)
32. https://pitchbook.com/profiles/company/541580-41 — PitchBook profile (headcount: 10)
33. https://www.bwdisrupt.com/article/sarvam-qure-ai-soket-gnani-ai-secure-spot-in-india-s-top-100-ai-startups-600829 — India Top 100 AI Startups list
34. https://techchilli.com/ai-india/soket-ai-labs-pioneering-ethical-agi-development-and-indigenous-language-models-in-india/ — Company profile
35. https://x.com/Analyticsindiam/status/1933136946861379849 — AIM tweet on Project EKA roadmap
36. https://www.youtube.com/watch?v=Q5NYa6zfE9A — Abhishek Upperwal at NASSCOM Technology & Leadership Forum
37. https://www.f6s.com/member/upperwal — Upperwal F6S profile
38. https://analyticsindiamag.com/ai-news-updates/meity-to-back-sarvam-ai-soket-ai-labs-gnani-ai-for-indiaai-mission/ — MeitY selection announcement
