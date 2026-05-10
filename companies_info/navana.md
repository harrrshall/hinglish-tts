# Navana.ai

**Website:** https://navana.ai  •  **HQ:** Mumbai, India  •  **Founded:** 2018  •  **Stage:** Pre-Series A
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): India-focused full-stack voice AI platform offering proprietary ASR, telephony voice agents, and call-center intelligence purpose-built for Indian languages and noisy real-world environments.
- Total funding to date: ₹13.2 Cr (~USD 1.5 M) across 4 rounds (verified via Tracxn MCA filing + multiple press sources)
- Last round: ₹7 Cr (~USD 800 K), Pre-Series A, July 15 2025, lead: Antler India
- Headcount: ~9 (per MCA filing Aug 31 2025); LinkedIn shows ~20; Tracxn reports 7 employees with 17% YoY growth (Jul 2025). Small but growing — conflicting signals; MCA statutory filing most reliable.
- Revenue / ARR: ₹2.13 Cr (~USD 251 K) for FY 2024-25 (39% 1-yr revenue CAGR, 81% EBITDA CAGR — per Tracxn/MCA). No ARR figure publicly stated.

## 2. Funding History
| Date | Round | Amount (INR) | Amount (USD) | Lead | Other Investors | Source |
|------|-------|-------------|--------------|------|-----------------|--------|
| Apr 25 2019 | Seed | Undisclosed | Undisclosed | Village Capital / AngelList | — | Crunchbase, Tracxn |
| Jul 18 2020 | Grant | ~₹1.8 Cr | ~$218 K | Maharashtra State Innovation Society | — | Tracxn |
| Apr 09 2021 | Grant | ~₹5.2 Cr | ~$630 K | GSMA | — | Tracxn |
| ~2023–2024 | Angel | ₹6.2 Cr | ~$700 K | Sandeep Singhal (Nexus VP) | Stanford Angel Fund, Rajan Mehra, Saahil Goel | Multiple press (Entrackr, Startuprise) |
| Jul 15 2025 | Pre-Series A | ₹7 Cr | ~$800 K | Antler India | Ajay Agarwal, Ronnie Screwvala, Sandeep Singhal | Indian Startup News, Entrackr, CXO Today |
| Jun 04 2025 | Seed (Crunchbase) | Undisclosed | Undisclosed | 17 investors | — | Crunchbase (may overlap with Pre-Series A above) |
| **Total** | | **~₹13.2 Cr** | **~$1.5 M** | | | |

**Notes / conflicts:** Crunchbase lists 4 rounds totalling $1.48 M. The "Jun 04 2025" Crunchbase seed round may be the same as the "Jul 15 2025" Antler-led Pre-Series A reported in press (slight date discrepancy; likely filing vs. announcement dates). Post-money valuation not publicly disclosed.

## 3. Product & Customers

### Products
1. **Bodhi Speech API (ASR)** — Real-time (WebSocket at `wss://bodhi.navana.ai`) and batch (HTTP POST at `https://bodhi.navana.ai/api/transcribe`) speech-to-text. Covers 10 languages with domain-specific model variants (general vs. banking, all at 8 kHz / telephony grade). Key features: hotword/context biasing, confidence scoring (word-level + segment-level), number parsing (Hindi, Malayalam, Kannada, Gujarati, Marathi), partial transcript suppression, code-switch support (Hindi, Kannada, Tamil with English). Python SDK: `pip install bodhi-sdk`.
2. **AI Contact Center** — End-to-end telephony voice agent platform (build, launch, evaluate). Includes agent workflow builder, proprietary ASR, real-time transcription, post-call analytics, CRM/telephony integrations, on-premise option. Positioning: "build to launch in weeks, not months."
3. **Audio Intelligence API** — Batch processing of recorded calls; outputs transcripts, call summaries, quality scores, fraud-detection signals, agent performance metrics.
4. **Sayl.ai** (associated brand, same legal entity per Tracxn) — WhatsApp commerce automation for D2C brands; interactive campaigns, AI sales/support, Shopify integration. Different market from core voice AI.

### Pricing
Not publicly available on website or docs. Error code 402 in API docs suggests credit-based billing model; contact `billing@navanatech.in`. No free tier confirmed.

### Languages & Voices
**ASR (Bodhi):** 10 Indian languages, 40+ dialects, 8 kHz telephony-optimised. Verified model IDs (from Gitbook docs, verified 2026-05-10):
- Bengali (bn), English India (en-IN), Hindi (hi), Hinglish (hi-en), Kannada (kn), Malayalam (ml), Marathi (mr), Tamil (ta), Telugu (te), Gujarati (gu), Odia (or — v3 only general)
- Each language has general-v2 and banking-v2 variants
- CEO claims 15 languages as of Happy Llama 2026 (LinkedIn, early 2026) — not yet reflected in public docs (10 confirmed in API docs as of research date)

**TTS:** Not offered. Bodhi is STT-only (confirmed in Gitbook docs).

**Voice cloning:** Not offered as a public product.

### Named Customers
| Customer | Use Case | Metric | Source |
|----------|----------|--------|--------|
| Bajaj Finserv / Bajaj Finance | Multilingual voicebot for personal loan disbursal (6 languages) | ₹150 Cr/month (Oct 2024); scaled to ~₹1,000 Cr/month (claimed, ~Apr 2026) | Indian Startup News, X/@Rahul_J_Mathur |
| Ujjivan Small Finance Bank | "Hello Ujjivan" voice banking app, 9 languages | 725 K downloads in year 1 (99% women users, 50K monthly loan repayments, 40K loan consent requests) | Latestly (Mar 2024), Indian Startup News |
| 40+ undisclosed enterprises | Banking, insurance, fintech | — | Company claims, all press coverage |

### Integrations / SDKs
- **Telephony:** Twilio (streaming ASR example repo), Freeswitch (open-source C++ module)
- **Python SDK:** `bodhi-sdk` (pip)
- **Voice agent framework:** Bolna (MIT fork of bolna-ai/bolna) supports Twilio, Plivo, Exotel, Vonage for telephony; Deepgram, OpenAI, Llama, ElevenLabs and others for LLM/TTS (Navana's own ASR can plug in)
- **On-premise deployment:** Available on request for data localization / RBI compliance

## 4. Technical Architecture

### Model approach
Proprietary end-to-end ASR models. Architecture not publicly disclosed. Given 8 kHz telephony focus and streaming WebSocket interface, likely conformer-based encoder with CTC/RNNT decoder (consistent with MUCS 2021 baseline recipes which used ESPnet conformer). Not autoregressive LLM-based. No diffusion or flow-matching TTS — ASR-only stack. Model versioning: v2 for most languages (general + banking), v3 for Odia general.

### Training data
- **MUCS 2021 dataset** (co-organised by Navana Tech): ~600 hours transcribed speech across 7 Indian languages (Hindi, Marathi, Odia, Tamil, Telugu, Gujarati, Bengali) + 2 code-switched pairs (Hindi-English, Bengali-English). OpenSLR 104. (2021)
- **RESPIN-S1.0** (co-built with IISc ARTPARK, funded by Bill & Melinda Gates Foundation): 10,000+ hours, 9 languages, 38 dialects, 18,000+ speakers, domains: agriculture & finance. Published NeurIPS 2025 Datasets & Benchmarks Track. Open access at spiredatasets.ee.iisc.ac.in. (2025)
- **Proprietary enterprise data:** "hundreds of thousands of real-world conversations" — claimed, not independently verified.
- **Collaboration partners (data/research):** IISc Bangalore (ARTPARK), Bill & Melinda Gates Foundation, IIT Madras, Microsoft Research India, IIM Ahmedabad, Bharat Inclusion Initiative.
- Claimed ~15,000 hours across 9 languages and 45 dialects from academic collaborations (not independently verified; possibly includes RESPIN).

### Latency profile
- **Streaming ASR:** Real-time via WebSocket; no specific TTFB/RTF published. Docs advise running clients on Indian servers or using on-premise for lowest latency. No numeric SLA published.
- **Claimed:** "85%+ accuracy with faster reaction times" (Mar 2024 Bodhi launch press). RTF not stated.
- Enterprise deployments handle "millions of calls" (claimed).

### Voice cloning
Not offered.

### Prosody / emotion control
Not applicable — product is ASR (STT), not TTS.

### Indic language strategy
- Bottom-up: collect dialect-rich, domain-specific data (RESPIN agriculture + finance domains chosen deliberately for target verticals).
- Telephony-native: 8 kHz models rather than high-fidelity 16 kHz, meeting actual BFSI IVR constraints.
- Domain specialisation: separate banking model variants (e.g., `hi-banking-v2-8khz`) fine-tuned for financial vocabulary.
- Code-switching support built in for Hindi, Kannada, Tamil (mixed Hinglish calls common in BFSI sales).
- No stated AI4Bharat or IndicTTS model lineage; independent model development, though collaborative on data (RESPIN published jointly with IISc/ARTPARK which also collaborates with AI4Bharat).

### Inference stack
- Cloud-hosted (`bodhi.navana.ai`); Indian data residency by design.
- On-premise deployment available (custom engagement).
- Also maintains forks/integrations with **sherpa-onnx** (Apache-2.0, C++/ONNX runtime inference, embedded/edge-capable) — suggests on-device inference capability is being explored.
- GoLang package (`sherpa-onnx-go`) for non-Python server deployments.
- No GPU type, cloud provider, or container details publicly disclosed.

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| MUCS 2021: Multilingual and Code-Switching ASR Challenges for Low Resource Indian Languages | Conference paper (Interspeech 2021) | Aug 2021 | https://navana-tech.github.io/MUCS2021/MUCS-21-Paper.pdf |
| MUCS 2021 Challenge Dataset (OpenSLR 104) | Dataset | 2021 | https://www.openslr.org/104/ |
| RESPIN-S1.0: A read speech corpus of 10000+ hours in dialects of nine Indian Languages | NeurIPS 2025 D&B | Sep 2025 | https://openreview.net/forum?id=qL8M2dOY4L |
| Bodhi multilingual voice model launch (2nd gen, 11+ languages) | Press/blog | Mar 8 2024 | https://www.latestly.com/technology/indian-artificial-intelligence-startup-navana-ai-launches-bodhi-second-generational-multilingual-voice-model-available-in-11-languages-5808215.html |
| RESPIN ASRU Challenge 2023 baseline | GitHub repo | 2023 | https://github.com/bloodraven66/RESPIN_ASRU_Challenge_2023 |

## 5. Open Source Footprint

### GitHub
Organization: https://github.com/navana-tech (verified 2026-05-10)

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| sherpa-onnx-go-linux | 0 | 10 | Apache-2.0 | May 7 2026 | Go package, Linux ONNX speech inference |
| bodhi-python-sdk | 0 | 0 | — | Jan 8 2026 | Bodhi ASR Python client |
| hotwords-validator | 0 | 0 | — | Oct 31 2025 | Hotword/context biasing validation tool |
| bodhi-streaming-asr-example | 2 | 0 | — | Sep 30 2025 | Streaming ASR demo (Python) |
| bodhi-freeswitch-module | 1 | 0 | MIT | Jun 4 2025 | C++ Freeswitch integration |
| bolna | 0 | 292 | MIT | Dec 16 2024 | Fork of bolna-ai; full-stack voice agent framework |
| sherpa-onnx-go | 0 | 13 | Apache-2.0 | Nov 27 2024 | Go package for ONNX speech inference |
| sherpa-onnx | 0 | 1,392 | Apache-2.0 | Nov 12 2024 | Fork of k2-fsa/sherpa-onnx; C++ ONNX runtime STT/TTS/SR |
| bodhi_python_latency_test | 0 | 0 | — | Jul 18 2024 | Latency benchmarking tool |
| bodhi-streaming-asr-twilio-example | 0 | 0 | — | May 31 2024 | Twilio + streaming ASR integration |
| is21ss_challenge_indic_asr_baseline_recipe | ~22 | — | — | 2021 | Pinned; MUCS/Interspeech 2021 baseline; most-starred repo |
| MUCS2021 | 0 | 2 | — | 2021 | Workshop website repo |

**Observations:** Low organic star counts on own repos. High fork counts on sherpa-onnx (1,392) and bolna (292) are inherited from upstream forks, not original work. The `is21ss_challenge_indic_asr_baseline_recipe` (~22 stars) is the only repo with meaningful organic community interest. Open source presence is primarily integration/example code rather than model release.

### Hugging Face
No Navana.ai or navana-tech organisation found on Hugging Face (verified 2026-05-10). Their RESPIN dataset is published under IISc/ARTPARK affiliation, not directly under Navana.

| Model/Dataset | Downloads | Likes | License | Notes |
|---------------|-----------|-------|---------|-------|
| RESPIN-S1.0 (IISc collab) | — | — | — | At spiredatasets.ee.iisc.ac.in, not HF |

### Top contributors
Not publicly visible (small team, most repos lack contributor graphs accessible without login). Srinivasa Raghavan K M (ML lead, LinkedIn confirmed) is the primary technical contributor based on LinkedIn presence; Jai Nanavati (CTO) leads engineering overall.

## 6. Team

### Founders
- **Raoul Nanavati** — Co-Founder & CEO. BA Political Science & Economics, McGill University; MBA, Cornell Tech (NYC). Prior: CEO/Co-founder BYOF Studios; Head of Product Strategy at WOI. LinkedIn: https://www.linkedin.com/in/raoul-nanavati-39403b1a/
- **Jai Nanavati** — Co-Founder & CTO. BE Engineering, University of Michigan; MBA, Cornell Tech (NYC). Prior: Enterprise Software Engineer at WOI and Elemential Labs. LinkedIn: https://in.linkedin.com/in/jai-nanavati-4ab22064

Both brothers incorporated NAVANA TECH INDIA PRIVATE LIMITED on Sep 30 2018 (CIN: U72900MH2018PTC315075), ROC Mumbai. They are the only two directors on record.

### Key technical hires
- **Srinivasa Raghavan K M** — ML/Speech AI Lead (title inferred from LinkedIn role at Navana.ai). Involved in voice AI from 2018. LinkedIn: https://www.linkedin.com/in/srinivasa-raghavan-k-m-02455547/

### Recent joiners (last 12mo)
Open roles as of May 2026: Account Manager (remote), Enterprise Sales Manager (Mumbai), Product Designer (remote), Lead Voice AI QA (remote), Senior Backend Engineer GoLang (remote). Indicates active hiring in sales, engineering, and QA — consistent with post-funding scaling. Specific named hires not publicly available.

### Notable departures (last 12mo)
Not publicly available.

### Open roles signal
5 open roles (May 2026): sales-heavy (2 sales roles) with technical positions (GoLang backend, Voice AI QA). Signal: commercialising and scaling post-Pre-Series A, not in pure R&D mode.

## 7. Moat & Defensibility

- **Data moat:** Moderate-strong. Co-built RESPIN-S1.0 (10,000+ hours, 38 dialects, 9 languages, NeurIPS 2025) with IISc/ARTPARK — gives access to dialect-rich training data that global players don't have at this resolution. Co-organised MUCS 2021 (600+ hours, 7 languages). Also accumulating proprietary enterprise call data from 40+ production deployments. However, RESPIN is open access, so the data moat from the published corpus alone is limited; value is in the proprietary call data and fine-tuning.
- **Model moat:** Moderate. Bodhi v2 banking models (domain-specific fine-tuning for BFSI) + 8 kHz telephony-native architecture are differentiated from generic ASR APIs. But no published benchmarks vs. Whisper, AI4Bharat, or Sarvam. "85%+ accuracy" is a company claim, unverified. Model architecture not disclosed, no open weights.
- **Distribution moat:** Moderate. BFSI-first GTM (Bajaj Finance, Ujjivan) creates stickiness through deep workflow integration (loan disbursal workflows, IVR compliance). RBI alignment + SOC 2 + ISO 27001 + data localisation lowers enterprise procurement friction. 40+ enterprise clients in BFSI/insurance/fintech as of mid-2025.
- **Brand / community moat:** Low. Low GitHub star counts, no HF presence, minimal developer community. Conference presence (Interspeech 2021, NeurIPS 2025, India AI Impact Summit 2026, Happy Llama 2026 Growth Award) builds credibility but not community.
- **Regulatory moat:** Moderate. RBI-aligned and data-localisation compliant — a genuine barrier for foreign ASR vendors entering Indian BFSI. SOC 2 Type II and ISO 27001 certifications are table stakes but meaningful checkboxes for enterprise procurement. No known government (Bhashini/ONDC) contracts — notable absence given competitors like Sarvam.
- **Replication cost (6mo, $10M competitor):** A well-funded team (~$10M) could likely assemble comparable Indic ASR using AI4Bharat IndicConformer + RESPIN (open access) + cloud telephony within 6-9 months. Navana's real moat is enterprise relationships, compliance certifications, and proprietary fine-tuning data — not the model architecture. Estimated replication cost of the full enterprise stack: $2-4M in talent + infrastructure; the relationships and compliance certifications cannot be bought quickly.
- **Moat strength: 2.5/5** — Strong domain focus (BFSI + Indic) and early enterprise traction, but thin open-source presence, undisclosed model benchmarks, small team, and a competitive landscape (Sarvam, Gnani, AI4Bharat) with far greater resources.

## 8. Risks & Problems

### Technical complaints
No public complaints found on Reddit, Hacker News, X, or GitHub issues (too small a company to surface in public discourse). The Bodhi API docs reveal a 402 error code requiring billing contact, suggesting no self-serve free tier — potential friction for developer adoption. Latency SLAs not published.

### Pricing pain points
No public pricing. Credit-based billing model but no published rates. Enterprise-only sales motion creates a high barrier for SMB/developer experimentation. Comparison with Sarvam (which also has usage-based pricing) is not possible without direct engagement.

### Safety / misuse
Not addressed in public documentation. Voicebot and ASR products used in financial services (loan disbursal, consent collection) carry risks around consent authenticity and voice fraud. No published fairness or bias testing. RESPIN dataset includes "noisy" subsets (semi-noisy and noisy partitions) — production accuracy in very noisy conditions not benchmarked publicly.

### Legal / regulatory
No known litigation. Operating in BFSI voice automation space means exposure to RBI's evolving guidelines on voice-based consent and automated loan processing. No Bhashini or government digital public good designation, which could affect future government tenders.

### Churn signals
No public churn signals. Bajaj Finance deepening from ₹150 Cr/month to ₹1,000 Cr/month loan disbursal via Navana AI is a strong anti-churn signal. Ujjivan app metrics (725K downloads, repeat monthly transactions) also positive. However, Bajaj Finance has also announced deployment of 600-800 autonomous AI agents from multiple vendors (Medianama, Feb/May 2026), suggesting Navana is one of several AI vendors — concentration risk.

## 9. Competitive Position

- **Direct competitors (India-focused Indic ASR/voice AI):**
  - **Sarvam.ai** — Foundational model company, $54M raised, Bhashini-aligned, government-backed, 10+ Indic languages, broader LLM+speech stack. Far better resourced.
  - **Gnani.ai** — Bengaluru, Series A ($7.72M), 12+ Indian languages, voice AI for BFSI, TTS (Vachana), longer operating history in same vertical.
  - **Smallest.ai** — Pune, Series A ($5.16M), 50+ languages, TTS-first, sub-100ms latency, developer-friendly.
  - **AI4Bharat** (IIT Madras) — Open-source, IndicConformer ASR, Indic-Parler-TTS, no commercial product but sets open benchmark.
  - **Murf** — English-first TTS, but expanding.
  - **ElevenLabs / Deepgram** — Global, no Indic specialisation, but enterprise credibility.
  - **BharatGen / VoicERA** — MeitY-backed open-source voice stack (launched India AI Impact Summit 2026) — potential commoditisation threat.

- **Where it's winning:**
  - BFSI-specific, telephony-native (8 kHz) ASR with domain fine-tuning for financial vocabulary.
  - Deep RBI/compliance alignment enabling enterprise BFSI deployments that foreign or less-compliant players cannot easily match.
  - Demonstrated production scale: ₹1,000 Cr/month in voice-assisted loan disbursal at Bajaj Finance.
  - Dialect coverage: 38 dialects via RESPIN, likely among best in class for rural/semi-urban Indian speakers.

- **Where it's losing:**
  - No TTS product (Gnani, Smallest, Sarvam all have TTS), limiting full-stack conversation AI play.
  - No Bhashini/government ecosystem integration (Sarvam is the designated government speech AI partner).
  - Developer adoption: no free tier, no HF model cards, no open weights — developers default to AI4Bharat or Sarvam.
  - Funding gap vs. Sarvam ($54M) and Gnani ($7.72M) vs. Navana's $1.5M total.
  - Revenue at ₹2.13 Cr (~$250K) is low for a 7-year-old company with 40+ enterprise clients — suggests limited deal sizes or heavy services revenue.

## 10. News & Momentum (last 12 months)
| Date | Event | Source |
|------|-------|--------|
| Jul 15 2025 | Raises ₹7 Cr Pre-Series A led by Antler India; total funding ₹13.2 Cr ($1.5M) | Indian Startup News, Entrackr, CXO Today |
| Sep 18 2025 | RESPIN-S1.0 paper accepted at NeurIPS 2025 Datasets & Benchmarks Track (w/ IISc) | OpenReview |
| Oct 2025 (est.) | Bajaj Finance loan disbursal via Navana reaches ₹150 Cr/month (Sanjiv Bajaj public statement ~6 months before Apr 2026) | X/@Rahul_J_Mathur |
| Early 2026 | Language count expands to 15 Indian languages (CEO LinkedIn claim) | Raoul Nanavati LinkedIn |
| Feb 2026 | Participated in India AI Impact Summit 2026; Raoul Nanavati on panel "Voice AI Beyond the Demo: What Actually Breaks at Scale?" | LinkedIn, luma.com event |
| ~Mar–Apr 2026 | Bajaj Finance loan disbursal via Navana grows to ~₹1,000 Cr/month | X/@Rahul_J_Mathur (Apr 2026 post) |
| 2026 | Wins Growth Breakthrough Award at Happy Llama 2026 (Analytics India Magazine AI startup conference) | happyllama.analyticsindiamag.com |

**Velocity verdict:** Moderate positive. The Pre-Series A in Jul 2025 and the NeurIPS 2025 paper are the key milestones. The Bajaj Finance scale-up from ₹150 Cr to ₹1,000 Cr/month is the most impressive commercial signal — but it's a single client. Conference appearances and the Happy Llama award indicate growing brand presence in India's AI ecosystem. Overall momentum is real but the company remains early-stage with limited publicly verifiable revenue and a thin team.

## 11. Bull Case / Bear Case

**Bull:** India's BFSI sector is the highest-value voice AI market in the world by transaction volume, and Navana is the only fully RBI-compliant, telephony-native Indic ASR provider with live production proof at Bajaj Finance scale (₹1,000 Cr/month). As AI-voice lending regulation tightens, compliance certifications become a durable moat. RESPIN dataset collaboration with IISc provides long-term dialect coverage that is structurally difficult for global hyperscalers to replicate. A Series A raise at 5-10x current ARR multiple would unlock sales team expansion and product breadth (TTS, LLM integration).

**Bear:** Navana has raised only $1.5M in 7 years — a sign of capital efficiency or a sign of difficulty raising. Revenue of ~$250K after 7 years is concerning. Sarvam.ai (government-backed, $54M raised) is building a full-stack Indic speech+LLM platform that could commoditise Bodhi ASR within 12-18 months. MeitY's open-source VoicERA stack (launched Feb 2026 on Bhashini infrastructure) poses direct commoditisation threat to enterprise BFSI ASR. No TTS = no full conversation product = limited pricing power. Single customer concentration risk (Bajaj Finance appears to be primary revenue driver). Small team (7-9 people) creates execution risk for enterprise contracts.

## 12. What I Couldn't Find
- Exact pricing / per-minute or per-call rates for Bodhi ASR API
- Post-money valuation for any round
- Full list of 40+ enterprise customers beyond Bajaj Finance and Ujjivan
- Named advisors or board members beyond the two founders
- Specific model architecture (encoder type, parameter count, training compute)
- TTFB / RTF benchmarks vs. competitors
- Any public G2/Capterra/Trustpilot reviews
- Bhashini, ONDC, or government tender involvement (searched — not found)
- Telco customers (not found in any source)
- Departure names or recent specific hire names beyond Srinivasa Raghavan
- Revenue breakdown between API, contact center platform, and services
- Sayl.ai revenue/customer traction (separate brand under same legal entity)

## Sources
1. https://navana.ai — Official website (fetched 2026-05-10)
2. https://navana.ai/about-us — About page (fetched 2026-05-10)
3. https://navana.ai/ai-contact-center — Product page (fetched 2026-05-10)
4. https://navana.ai/careers — Careers page (fetched 2026-05-10)
5. https://navana.gitbook.io/bodhi — Bodhi API documentation (fetched 2026-05-10)
6. https://navana.gitbook.io/bodhi/llms-full.txt — Full Bodhi API technical spec (fetched 2026-05-10)
7. https://indianstartupnews.com/funding/homegrown-voice-ai-startup-navana-ai-raises-rs-7-crore-in-a-round-led-by-antler-india-9501575 — Pre-Series A funding news (Jul 2025)
8. https://cxotoday.com/media-coverage/navana-ai-raises-pre-series-a-led-by-antler-bringing-total-funding-to-1-5m/ — Funding details (Jul 2025)
9. https://entrackr.com/snippets/voice-ai-startup-navanaai-raises-rs-7-cr-in-pre-series-a-round-9500014 — Entrackr funding snippet
10. https://theheadandtale.com/ai-emerging-tech/voice-technology-startup-navana-ai-bags-pre-series-a-funding/ — Full funding round details including prior angel round
11. https://startuprise.org/navana-ai-raises-pre-series-a-round/ — Prior angel round details (Stanford Angel Fund, Nexus)
12. https://tracxn.com/d/companies/navana-tech/__pNXWBJUtIrJbiBS2i2JHQOULqc6CV1FFCedsBZxll4s — Company profile, financials, team (Tracxn, verified)
13. https://tracxn.com/d/legal-entities/india/navana-tech-india-private-limited/__l61dgf8M9gJPfbOgijJBDczUIlSqFF_rBwtSS4h4oXQ — MCA filing details: CIN, directors, revenue, employee count
14. https://www.crunchbase.com/organization/navana-tech — Crunchbase profile (4 rounds, $1.48M)
15. https://pitchbook.com/profiles/company/342941-59 — PitchBook profile
16. https://github.com/navana-tech — GitHub organisation (fetched 2026-05-10)
17. https://github.com/navana-tech/bolna — Bolna repo (voice agent framework fork)
18. https://github.com/navana-tech/MUCS2021 — MUCS 2021 challenge repo
19. https://navana-tech.github.io/IS21SS-indicASRchallenge/ — MUCS 2021 challenge website
20. https://navana-tech.github.io/MUCS2021/MUCS-21-Paper.pdf — MUCS 2021 Interspeech paper
21. https://www.openslr.org/104/ — MUCS 2021 dataset (OpenSLR 104)
22. https://openreview.net/forum?id=qL8M2dOY4L — RESPIN-S1.0 NeurIPS 2025 paper
23. https://kernel.iisc.ac.in/our-languages-our-data/ — IISc article on RESPIN/Navana collaboration
24. https://www.latestly.com/technology/indian-artificial-intelligence-startup-navana-ai-launches-bodhi-second-generational-multilingual-voice-model-available-in-11-languages-5808215.html — Bodhi v2 launch (Mar 8 2024)
25. https://www.siliconindia.com/news/general/navanaai-unveils-bodhi-multilingual-voice-model-amid-indias-ai-embrace-nid-228327-cid-1.html — Bodhi launch coverage
26. https://yourstory.com/companies/navanaai — YourStory company profile
27. https://www.facebook.com/yourstorycom/posts/brothers-raoul-and-jai-nanavati-founded-navanaai-after-seeing-everyday-struggles/1227948182700487/ — YourStory founders story
28. https://www.linkedin.com/in/raoul-nanavati-39403b1a/ — Raoul Nanavati LinkedIn
29. https://in.linkedin.com/in/jai-nanavati-4ab22064 — Jai Nanavati LinkedIn
30. https://www.linkedin.com/in/srinivasa-raghavan-k-m-02455547/ — Srinivasa Raghavan LinkedIn
31. https://www.linkedin.com/company/navanatech — Navana.ai LinkedIn company page
32. https://wellfound.com/company/navanatech/people — Wellfound team page (403 blocked)
33. https://www.youtube.com/watch?v=O3ExwwPaNs4 — Founder Talks: Raoul & Jai Nanavati (JioGenNext)
34. https://x.com/Rahul_J_Mathur/status/1971437946797494293 — Bajaj Finance ₹1,000 Cr/month claim (Apr 2026)
35. https://www.medianama.com/2026/02/223-bajaj-finance-800-ai-agents-lending-operations/ — Bajaj Finance AI agent deployment
36. https://www.medianama.com/2026/05/223-q4fy26-bajaj-finance-autonomous-agent-target-800-600-fy27/ — Bajaj Finance Q4FY26 AI update
37. https://happyllama.analyticsindiamag.com/awards/ — Happy Llama 2026 Growth Breakthrough Award
38. https://luma.com/lreain78 — Voice AI After-Hours event at India AI Impact Summit 2026
39. https://www.linkedin.com/posts/navanatech_indiaaiimpactsummit2026-voiceai-enterpriseai-activity-7429457107156086784-yYik — India AI Impact Summit participation (LinkedIn)
40. https://analyticsindiamag.com/ai-trends/these-7-indian-voice-ai-startups-are-getting-loud — Indian voice AI landscape overview
41. https://smallest.ai/blog/smallest-ai-vs-sarvam-ai — Competitor comparison (Smallest vs Sarvam)
42. https://www.zaubacorp.com/NAVANA-TECH-INDIA-PRIVATE-LIMITED-U72900MH2018PTC315075 — MCA/Zauba Corp CIN verification
43. https://mycorporateinfo.com/business/navana-tech-india-private-limited — Corporate info verification
44. https://www.marcamoney.com/navana-ai-raises-7-crore-in-pre-series-a-funding-led-by-antler/ — Additional funding coverage
45. https://startup.siliconindia.com/startup-funding/navana-ai-secures-rs-7-crore-in-funding-led-by-antler-india-nwid-50248.html — SiliconIndia funding coverage
46. https://startupnews.fyi/2025/07/15/voice-ai-startup-navana-ai-raises-rs-7-crore-in-round-led-by-antler-india/ — StartupNews.fyi coverage
47. https://unlistedzone.com/navanaai-secures-pre-series-a-funding-to-revolutionize-voice-ai-for-indian-enterprises — UnlistedZone coverage
48. https://ddnews.gov.in/en/meity-launches-open-source-voicera-voice-ai-stack-on-bhashini-infrastructure-at-india-ai-impact-summit-2026/ — MeitY VoicERA (competitive threat context)
49. https://tracxn.com/d/artificial-intelligence/ai-startups-in-voice-ai-in-india/__s7thq7EI12tPI5Mmcnok_vjilY5MhlglLRUi8kzPmHs/companies — Indian voice AI landscape (Tracxn)
50. https://www.linkedin.com/posts/lokesh-kannan-a92751102_voiceai-india-speechmodels-activity-7383363494773112832-U2vC — RESPIN/IISc collaboration LinkedIn post
