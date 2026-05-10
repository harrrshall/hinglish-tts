# India Voice AI — Comparison Matrix
> Generated 2026-05-10 | Sources: individual company dossiers; MCA = Ministry of Corporate Affairs filings; Latka = GetLatka.com self-reported; ⚠️ = data conflict flagged

---

## 1. Quick-Reference Table

| Company | Stage | Total Funding (USD) | Last Round (Date) | Headcount | Revenue / ARR | Model Approach | Languages | GitHub Stars (total) | Indic Focus | Moat Score | Velocity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Sarvam AI** | Series B (closing) | ~$391M | ~$350M Apr 2026 | ~150 | ₹29.1 Cr FY2025 (MCA) | Proprietary full-stack (Sarvam-30B, 105B MoE, Bulbul TTS, Saaras ASR) | 22 Indian scheduled | ~153 (cookbook) | Primary mission | 4/5 | Hypergrowth |
| **Krutrim (Ola)** | Growth / Unicorn | ~$280M+ | $50M Jan 2024 valuation round | ~549 (post-200 layoffs) | ₹101.7 Cr FY2025 ⚠️ 90% related-party Ola; FY26 ₹300 Cr target | Proprietary (Krutrim-1/2, Dhwani ASR) — model work paused | 22 Indian | ~19 max per repo | Yes | 3/5 | Decelerating |
| **Convin.ai** | Series A | ~$8.94M | $6.5M Aug 2024 | ~148 | $22.7M claimed ⚠️ (Latka, unverified; conflicts with funding size) | Proprietary 7B LLM (200B tokens, 35+ languages, 23 Indic) | 35+ (23 Indic) | 0 (GitHub 404) | Yes | 3/5 | Stable |
| **Gnani.ai** | Series B | ~$28M+ | $10M Mar 2026 | ~169–200 | ₹53.87 Cr FY2025 (MCA, profitable) | Proprietary (Vachana STT 1M hrs, Inya VoiceOS 5B, Vachana TTS) | 12+ Indian | ~11 max per repo | High | 3.5/5 | Accelerating |
| **Mihup** | Series A | ~$10.8M | $10.8M Sep–Nov 2024 | ~75–100 | ₹20.2 Cr FY2025 (MCA) | Proprietary ASR+NLU+dialogue | 120+ claimed, 20+ Indian | 0 (empty) | High | 3/5 | Accelerating |
| **CoRover.ai** | Series A | ~$4M+ strategic | $4M Sep 2024 + HDFC strategic Aug 2025 | ~101 | $10.5M Latka ⚠️ vs ₹12 Cr MCA | Fine-tuned (BharatGPT 3B + NVIDIA Riva speech) | 22+ text, 14 voice | ~minimal (4 repos) | Government-grade | 4/5 | Stable |
| **GreyLabs AI** | Series A | ~$10.2M | $10.2M Oct 2025 | ~49–71 | $11M Latka ⚠️ vs ₹3.81 Cr FY2025 MCA | Proprietary STT + fine-tuned LLM for BFSI | English, Hindi, Hinglish | 0 (none) | Partial | 3.5/5 | Accelerating |
| **Nurix AI** | Series A | ~$25M+ | ~$16M Mar 2026 | ~132 | ₹5.35 Cr FY2025 (MCA) | Model-agnostic orchestration (LiveKit, OpenAI Realtime forks) | 15+ Indian claimed | 0 (all forks) | Partial | 2/5 | Accelerating |
| **Smallest.ai** | Seed | ~$8.26M | $8.26M Oct 2025 | ~23 | ₹93.2L FY2024-25 (MCA) | Proprietary full-stack (Lightning TTS, Pulse STT, Electron SLM, Hydra S2S) | 12 (Lightning), 38 (Pulse) | ~40 (SDK) | Partial | 2.5/5 | Accelerating |
| **Soket AI Labs** | Seed | ~$2.2M | $2.2M Mar 2026 | ~15 | Not disclosed ($0.012/min pricing) | Proprietary OSS (Pragna-1B, BHASHA-7B, DHRITH ASR) + ₹177 Cr compute grant | 22 (BHASHA) | ~26 (coom repo) | High (IndiaAI Mission) | 3/5 | Accelerating |
| **Bolna AI** | Seed | ~$6.3M | $6.3M Jan 2026 | ~25 | ~$700K ARR | Orchestration middleware (MIT OSS SDK, no proprietary models) | 10+ via Sarvam integration | 639 (bolna repo) + 285 forks | Via partners | 2.5/5 | Accelerating |
| **Ringg AI** | Series A | ~$5.5M | $5.5M Jan 2026 | ~18 | Not disclosed | Proprietary (Parrot STT V1 NeMo-based, Squirrel TTS V1.0 38 Indian voices) | 20+, 9 Indian | 0 (no GitHub org) | High | 2/5 | Accelerating |
| **SpeakX** | Pre-Series B | ~$28M+ | $16M Oct 2025 | ~27 | $7.5M ARR claimed ⚠️ vs ₹9.63 Cr FY2025 MCA | App layer (Google Gemini) | Hindi UI, English target | ~0 (forks only) | Consumer Hindi | 2.5/5 | Stable |
| **Stimuler** | Pre-Series A | ~$5.75M | $3.75M Apr 2025 | ~34 | ₹3.16 Cr FY2025 (MCA, 5× YoY) | App layer (Hume AI EVI + WhisperS2T) | English only | 0 (forks only) | None (global ESL) | 2.5/5 | Accelerating |
| **Fundamento** | Pre-Series A | ~$5.4M | $1.9M Oct 2025 | ~52 | ₹4.13 Cr FY2025 (MCA) | LLM-agnostic + Dialecto proprietary ASR | 30+ claimed | 0 (none) | Partial | 2/5 | Stable |
| **Arrowhead** | Seed | ~$3M | $3M Jan 2026 | Not disclosed | ₹71.2L FY2025 (MCA) | Fine-tuned LLMs (base model undisclosed) | 10+, 7 Indian | 0 (GitHub 404) | Partial | 3/5 | Uncertain |
| **Navana.ai** | Pre-Series A | ~$800K | ₹7 Cr (~$800K) Jul 2025 | ~9–20 | ₹2.13 Cr FY2025 (MCA) | Proprietary ASR only (Bodhi STT, 10 Indian languages) | 10 Indian (Bodhi) | ~22 (is21ss repo) | High | 2.5/5 | Accelerating |
| **Vobiz.ai** | Seed | ~$1M | $1M May 2026 | Not disclosed | Not disclosed ($5M ARR target FY27) | CPaaS/telephony infra only (integrates Sarvam, ElevenLabs, LiveKit) | Via partners | ~2 (16 repos) | Via partners | 2/5 | Accelerating |
| **Pype AI** | Pre-Seed | ~$1.2M | $1.2M Nov 2025 | ~13 | ₹3.35L FY2025 (MCA, trivial) | Commodity (Pipecat + Azure OpenAI) | 20+ claimed | ~82 (Whispey 65 + Agensight 17) | Partial | 2/5 | Early |

---

## 2. Company Profiles at a Glance

### Sarvam AI
- **What it is:** India's flagship sovereign AI platform — full-stack LLM, ASR, TTS, and VLM built from scratch for 22 Indian scheduled languages; IndiaAI Mission sovereign LLM contract winner.
- **Key differentiation:** Only Indian company with frontier-scale proprietary models (Sarvam-30B, 105B MoE) AND government mandate; UIDAI, Bhashini, and Aadhaar-scale deployments give irreplicable data flywheel.
- **Biggest risk:** $350M Series B at $1.5B valuation raises the bar impossibly high — must compete with OpenAI/Google globally, not just in India; burn rate at this scale is existential if model advantage erodes.
- **Surprising fact:** Revenue was only ₹29.1 Cr (~$3.5M) FY2025 despite >$40M raised by then — the Series B is a bet on future revenue, not current traction.
- **Bhashini exposure:** Primary — 600 crore+ AI API requests routed through Bhashini.
- **Open-source signal:** sarvam-30b 52.2K HF downloads, sarvam-105b 20.2K downloads (as of dossier date).
- **Capital efficiency:** ~$100M+ raised per ~$3.5M revenue — lowest in the cohort; intentional for deep tech.

### Krutrim (Ola)
- **What it is:** Ola's AI subsidiary; India's first AI unicorn ($1B valuation Jan 2024); originally full-stack (LLM + cloud + chip + consumer app), now pivoting hard to cloud/GPU-as-service.
- **Key differentiation:** Largest headcount in cohort; only company building AI infrastructure (GPU cloud) alongside models; Bhasha Kritika dataset (16.2M HF downloads) is a genuine open-source contribution.
- **Biggest risk:** Strategic pivot confusion — model work paused, chip work paused, consumer Kruti app shut; layoffs of 200+ signal financial stress despite FY26 profit target; 90% FY25 revenue was related-party Ola traffic (not real market revenue).
- **Surprising fact:** Despite being declared India's first AI unicorn, Krutrim did NOT win the IndiaAI Mission sovereign LLM contract — Sarvam did. HF Krutrim-2-instruct model has only 47 downloads.
- **Revenue quality risk:** ₹101.7 Cr FY2025 revenue is ~90% from parent company Ola — strip that out and real third-party revenue is ~₹10 Cr.
- **Open-source signal:** BhashaKritika dataset 16.2M HF downloads; models themselves have negligible adoption.
- **Moat caveat:** Moat is 3/5 despite unicorn status; cloud moat is real but model moat has weakened.

### Gnani.ai
- **What it is:** Enterprise voice AI platform for BFSI contact centers; proprietary full-stack (ASR, TTS, VoiceOS) with 1M+ hours of Indic speech training data; only profitable company in the cohort.
- **Key differentiation:** Only company that is both profitable AND building proprietary models; Inya VoiceOS 5B is a voice-native (not text-wrapped) architecture; 12+ language ASR trained on banking-domain telephony audio.
- **Biggest risk:** Positioned in crowded BFSI voice AI segment against Convin, GreyLabs, Mihup, Fundamento simultaneously; differentiation from commodity orchestration players depends on ASR quality claims being defensible.
- **Surprising fact:** IndiaAI Mission selected (compute grant) AND Bhashini finalist — dual government validation, rare in cohort.
- **Financial health:** ₹53.87 Cr FY2025 revenue (MCA verified), positive EBITDA — most capital-efficient proprietary model company in cohort.
- **Capital efficiency:** ~$28M raised, ~₹54 Cr revenue = best efficiency ratio for a proprietary-model company.
- **Headcount depth:** 169–200 employees, largest engineering team in contact-center segment.

### Nurix AI
- **What it is:** Enterprise conversational AI via NuPlay platform — voice agents for customer-facing workflows; backed by Prosus, General Catalyst, Accel.
- **Key differentiation:** High-profile VC backing and enterprise customer credibility despite zero proprietary models; model-agnostic design means rapid adoption of new foundation models.
- **Biggest risk:** Zero proprietary IP — all five GitHub repos are forks with 0 stars; HF is empty; if Sarvam/OpenAI offer direct enterprise APIs, Nurix's orchestration layer faces disintermediation.
- **Surprising fact:** ₹5.35 Cr (~$640K) FY2025 revenue despite ~$25M+ raised — extreme gap between capital and traction suggests most revenue is contracted post-March 2025.
- **Model dependency:** Uses LiveKit, OpenAI Realtime API forks — no lock-in assets.
- **Bhashini:** None.
- **Velocity note:** Series A extension Mar 2026 signals investors doubling down despite slow revenue start.

### Ringg AI
- **What it is:** No-code voice agent platform for building multilingual outbound/inbound agents; India + MENA markets; proprietary STT and TTS models hosted on HuggingFace.
- **Key differentiation:** Squirrel TTS V1.0 was HuggingFace Space of the Week — rare organic community validation; 38 Indian voices; Parrot STT V1 benchmarked at 15% WER on Hindi telephony.
- **Biggest risk:** Smallest headcount (18) in the orchestration cohort; no GitHub organization at all; HF models have modest traction (Squirrel 80 likes); MENA expansion without India product-market fit first is a stretch.
- **Surprising fact:** Kunal Shah (CRED founder) and Groww Founder Fund in the cap table — fintech-adjacent networks may accelerate distribution into lending/fintech voice use cases.
- **Open-source signal:** RinggAI HF org is active; ASR dataset 435 downloads; no code on GitHub.
- **Bhashini:** None.
- **Languages note:** 9 Indian languages confirmed operational; 20+ is marketing claim.

### Bolna AI
- **What it is:** Open-source (MIT) voice agent orchestration SDK and API; India-focused but architected for global developers; YC F25 + General Catalyst backed.
- **Key differentiation:** 639 GitHub stars + 285 forks — highest open-source community signal in cohort by far; developer mindshare is the moat; not competing on models.
- **Biggest risk:** MIT license means any competitor (including Sarvam) can fork and productize; ~$700K ARR at $6.3M raised implies ~5.5× ARR multiple — not unusual for OSS but conversion to enterprise contract revenue must accelerate.
- **Surprising fact:** General Catalyst invested in both Bolna (orchestration) AND Nurix (enterprise orchestration) — simultaneously backing two competing middleware plays.
- **Open-source signal:** bolna-ai/bolna v0.10.35, 639 stars, 285 forks — strongest GitHub presence in cohort.
- **Capital efficiency:** ~$700K ARR / $6.3M raised = $111 revenue per $1K invested — middle of cohort.
- **Bhashini:** None (partners with Sarvam which is Bhashini-connected).

### Arrowhead
- **What it is:** Verticalized AI voice platform specifically for BFSI sales calls — insurance, lending, wealth management; fine-tuned LLMs on financial sales conversations.
- **Key differentiation:** Deep vertical focus on BFSI sales (not just contact center) with intent to build call-flow intelligence tuned to Indian financial regulation compliance.
- **Biggest risk:** Co-founder Chinmay Shah departed after funding — founding team instability is a red flag at Seed stage; ₹71.2L FY2025 revenue (~$85K) is negligible; GitHub 404 and HF 404 mean zero verifiable technical assets.
- **Surprising fact:** Kunal Shah (CRED) also invested here — he holds stakes in both Arrowhead AND Ringg AI, two competing voice agent platforms in the same BFSI vertical.
- **Verification gap:** No working GitHub or HuggingFace — cannot verify any proprietary model claims.
- **Bhashini:** None.
- **Revenue:** ₹71.2L FY2025 = lowest verifiable revenue of all companies with disclosed figures.

### Pype AI
- **What it is:** AI voice front desk for hospitals and healthcare clinics — appointment scheduling, patient intake, post-visit follow-up; India healthcare vertical.
- **Key differentiation:** First-mover in hospital voice AI in India; OSS contribution via Whispey (voice AI observability, 65 stars) signals developer-centric culture.
- **Biggest risk:** Commodity stack (Pipecat + Azure OpenAI) with trivial revenue (₹3.35L FY2025 = ~$4K) and Pre-Seed status; healthcare sales cycles in India are long; DPDP Act compliance for patient data adds regulatory burden.
- **Surprising fact:** Built two open-source tools (Whispey observability, Agensight agent monitoring) despite being a 13-person Pre-Seed startup — unusually high OSS output for stage.
- **Stack note:** Fully commodity — differentiates on vertical GTM, not technology.
- **Bhashini:** None.
- **Capital efficiency:** $1.2M raised, ~$4K revenue = worst ratio in cohort (appropriately early-stage).

### Smallest.ai
- **What it is:** Full-stack real-time voice AI platform — Lightning TTS (<100ms TTFB), Pulse STT (64ms, 38 languages), Electron SLM (~4B params), Hydra S2S end-to-end, Atoms agent platform.
- **Key differentiation:** Published arXiv paper (2504.03279) on Tenstorrent NPU optimization — only company in cohort with hardware-software co-design publication; sub-100ms TTFB claim is best-in-class for streaming TTS.
- **Biggest risk:** No models on HuggingFace to validate proprietary claims; ₹93.2L FY2024-25 revenue despite $8.26M raised; competing with Sarvam (better-funded, same full-stack thesis) head-on.
- **Surprising fact:** 38 languages for Pulse STT is broader than Sarvam's 22 Indian language claim — if real, significant technical achievement for a 23-person team.
- **Open-source signal:** smallest-inc SDK 40 GitHub stars — modest community; no model weights published.
- **Bhashini:** None.
- **arXiv note:** Paper 2604.03279 on Tenstorrent optimization (as of dossier date).

### GreyLabs AI
- **What it is:** BFSI contact center speech analytics and voice AI — real-time call scoring, agent assist, compliance monitoring; Cogno AI alumni-founded.
- **Key differentiation:** Pedigree from Cogno AI (acquired by Exotel 2021) gives founders prior exit credibility and BFSI distribution networks; proprietary STT fine-tuned on banking domain conversations.
- **Biggest risk:** Revenue conflict: $11M Latka claim vs ₹3.81 Cr (~$450K) MCA FY2025 — if MCA is right, Latka figure is 24× inflated, which is extreme even for ARR vs revenue differences.
- **Surprising fact:** Elevation Capital invested in both SpeakX (EdTech, Oct 2025) and GreyLabs (BFSI, Oct 2025) in the same month — back-to-back bets on voice AI applications in different verticals.
- **Revenue flag:** ⚠️ $11M Latka vs ₹3.81 Cr MCA — treat all revenue figures as unverified until FY2026 MCA filings.
- **Bhashini:** None.
- **Languages:** English, Hindi, Hinglish confirmed; broader claims unverified.

### SpeakX
- **What it is:** Consumer AI app for spoken English learning targeting India Tier 2/3 users; 10M+ downloads; EBITDA positive.
- **Key differentiation:** Largest consumer user base in cohort (10M+ downloads); only confirmed EBITDA-positive consumer app; WestBridge Capital backing indicates institutional confidence in EdTech monetization.
- **Biggest risk:** Revenue conflict: $7.5M ARR claimed vs ₹9.63 Cr (~$1.15M) MCA FY2025 — if MCA is accurate, ARR claim is ~6.5× higher than annual revenue; App layer (Google Gemini) means zero model moat.
- **Surprising fact:** Despite being an AI company, SpeakX's entire differentiation is GTM (distribution to Tier 2/3 India) not technology — the AI is commodity Google Gemini.
- **Revenue flag:** ⚠️ $7.5M ARR vs ₹9.63 Cr MCA — significant discrepancy; likely ARR is forward-run-rate and MCA is reported annual.
- **Bhashini:** None.
- **Indic note:** Hindi UI but English content — serves Indic speakers, not Indic language AI.

### Fundamento
- **What it is:** Agentic voice AI for BFSI collections and lending — outbound voice agents for loan recovery, EMI reminders, KYC; distinguishes via compliance-aware dialogue.
- **Key differentiation:** Strategic investor base includes celebrity investors KL Rahul and Ben Stokes (The Players Fund) — unusual; IIFL Fintech Fund adds BFSI-specific distribution credibility.
- **Biggest risk:** BFSI collections is a regulatory minefield — TRAI DLT, RBI guidelines on automated recovery calls, DPDP Act; 30+ language claim with zero public model evidence and no GitHub/HF; commodity-adjacent stack (Dialecto ASR only proprietary element).
- **Surprising fact:** Celebrity investor fund (cricketers KL Rahul + Ben Stokes) in a B2B voice AI startup — likely a fund diversification play, not domain expertise.
- **Stack note:** LLM-agnostic + Dialecto proprietary ASR; orchestration layer is commodity.
- **Bhashini:** None.
- **Capital efficiency:** ₹4.13 Cr FY2025 / ~$5.4M raised = moderate.

### Stimuler
- **What it is:** Voice-first AI English tutor (global ESL) — real-time conversation practice with AI; 5M+ installs; top EdTech app in Indonesia.
- **Key differentiation:** 85% revenue from outside India (primarily Indonesia, Southeast Asia) — most geographically diversified revenue in cohort; Hume AI EVI integration for emotion-aware conversation.
- **Biggest risk:** Fully dependent on Hume AI EVI and WhisperS2T — no proprietary models; if Hume changes pricing or API terms, Stimuler has no fallback; English-only limits Indic TAM.
- **Surprising fact:** Despite being an India-headquartered startup, India generates only 15% of revenue — it's effectively a Southeast Asian EdTech company registered in India.
- **Open-source signal:** Zero — GitHub forks only, HF empty.
- **Bhashini:** None.
- **5× YoY growth** ₹3.16 Cr FY2025 (MCA) — fastest growth rate among EdTech cohort members.

### Krutrim — see above (full profile under Krutrim section)

### Mihup
- **What it is:** Proprietary ASR + conversation intelligence platform with automotive voice AI; 1M+ Tata Motors vehicles deployed; IPO ambitions.
- **Key differentiation:** Only company in cohort with automotive OEM deployment at scale (Tata Motors 1M vehicles) — physical hardware integration creates switching costs that software-only players cannot replicate; Qualcomm NPU partnership Feb 2026 for on-device inference.
- **Biggest risk:** 120+ languages claimed with zero public evidence (no GitHub, no HF, no paper) — if actual coverage is 20 Indian languages, the rest is aspirational marketing; IPO ambition requires transparent financials, currently opaque.
- **Surprising fact:** ₹20.2 Cr FY2025 revenue with ~$10.8M raised makes Mihup the most capital-efficient proprietary-model company in the $10M+ raised segment.
- **Capital efficiency:** ₹20.2 Cr / $10.8M raised = best among mid-stage proprietary model companies.
- **Bhashini:** None.
- **Automotive moat:** 1M Tata Motors vehicles is a durable physical deployment moat — unmatched in cohort.

### CoRover.ai
- **What it is:** Government-grade conversational AI platform; created AskDISHA for IRCTC with 12B+ lifetime interactions and 65M MAU — India's most-used AI product by volume.
- **Key differentiation:** AskDISHA is the largest deployed AI product in India by interaction volume; HDFC Bank strategic investment (Aug 2025) bridges public and private sector; BharatGPT Mini 534M runs on-device.
- **Biggest risk:** Revenue conflict: $10.5M Latka vs ₹12 Cr (~$1.43M) MCA — Latka is 7× higher; government contracts are long-cycle, price-compressed, and renewal-uncertain; BharatGPT 3B model has non-commercial HF license limiting ecosystem adoption.
- **Surprising fact:** AskDISHA (12B+ interactions, 65M MAU) was built with a non-commercial model under government contract — the world's most-used government AI assistant arguably runs on restricted-license technology.
- **Bhashini:** Yes (fully integrated).
- **ONDC:** Yes (Digital Commerce integration).
- **Revenue flag:** ⚠️ $10.5M Latka vs ₹12 Cr MCA.

### Convin.ai
- **What it is:** Conversation intelligence and automated quality assurance for contact centers; proprietary 7B LLM trained on 200B tokens with 35+ language support including 23 Indic languages.
- **Key differentiation:** G2 #1 Speech Analytics Winter 2024 badge provides third-party validation; 7B proprietary LLM with 23 Indic languages is credible model investment; ICICI Bank, SBI Life, Flipkart, Titan as named customers.
- **Biggest risk:** $22.7M revenue claim (GetLatka) is implausible relative to $8.94M total funding — either ARR vs revenue timing difference or significant inflation; GitHub 404 means zero code verification.
- **Surprising fact:** If $22.7M revenue claim were accurate, Convin would be the highest revenue company in the cohort — but with only $8.94M raised, it would also be the most capital-efficient by a factor of 5×. The implausibility of this suggests heavy ARR inflation.
- **Revenue flag:** ⚠️ $22.7M Latka vs ~$8.94M total funding raised — likely ARR is inflated or includes multi-year contract TCV.
- **Bhashini:** None.
- **GitHub:** 404 — no verifiable OSS presence.

### Navana.ai
- **What it is:** India's smallest focused ASR specialist — Bodhi STT for 10 Indian languages optimized for 8kHz telephony audio; co-built RESPIN-S1.0 dataset (NeurIPS 2025, 10K hours).
- **Key differentiation:** NeurIPS 2025 dataset paper (RESPIN-S1.0 with IISc) is strongest academic pedigree in ASR-specialist cohort; Bajaj Finance deployment (₹1,000 Cr/month loan disbursal voice verification) is high-stakes production validation.
- **Biggest risk:** 9–20 headcount and ~$800K raised is dangerously undercapitalized; no TTS product means Navana cannot capture full-stack voice agent opportunities; one customer (Bajaj Finance) concentration risk.
- **Surprising fact:** RESPIN-S1.0 dataset (NeurIPS 2025) was co-built by a 9-person startup alongside IISc — unusual academic-startup collaboration for a company at this stage.
- **Open-source signal:** navana-tech/is21ss ~22 stars; RESPIN dataset hosted at IISc not HF.
- **Bhashini:** None.
- **Capital efficiency:** ₹2.13 Cr / $800K raised = $265 revenue per $1K invested — second-best in cohort after Gnani adjusted for stage.

### Vobiz.ai
- **What it is:** AI-native SIP trunking and CPaaS infrastructure for India — telephony plumbing layer enabling voice AI companies to deploy calls over Indian PSTN; not an AI model company.
- **Key differentiation:** Infrastructure-layer positioning means Vobiz can be a supplier to all other companies in the cohort (including competitors) rather than competing with them; direct PSTN interconnects give latency and cost advantages.
- **Biggest risk:** 2/5 moat — telephony infrastructure is a commodity; AWS Connect, Exotel, Kaleyra, MCUBE all compete; no disclosed revenue means no traction evidence; GitHub only ~2 stars across 16 repos.
- **Surprising fact:** Most recent funding in the cohort (May 2026) — Piper Serica VC Fund bet is the freshest signal of investor appetite for India voice AI infra layer.
- **Revenue:** Not disclosed; $5M ARR target FY27 is aspirational.
- **Bhashini:** None.
- **Stack note:** Integrates Sarvam, ElevenLabs, LiveKit, OpenAI — purely infrastructure, AI is in integrated layers.

### Soket AI Labs
- **What it is:** Open-source Indic LLM research lab + TensorStudio speech API; building Project EKA 120B MoE (planned); selected for IndiaAI Mission (₹177 Cr compute grant).
- **Key differentiation:** BHASHA-7B HF dataset has 44.4M downloads and 1.1K likes — strongest open-source community signal of any Indic LLM lab in cohort; Apache 2.0 license (Pragna-1B) is fully permissive; only Seed-stage company with government compute grant.
- **Biggest risk:** ARR not disclosed at all; $0.012/min TensorStudio pricing implies very early commercial stage; 15 headcount attempting 120B-parameter MoE is resource-stretched; no formal Bhashini integration despite government alignment.
- **Surprising fact:** BHASHA-7B HuggingFace dataset has more downloads (44.4M) than Sarvam's entire model portfolio combined — open-source data community traction exceeds much better-funded competitors.
- **Open-source signal:** bhasha-wiki 44.4M downloads + 1.1K likes = highest OSS traction in cohort.
- **Bhashini:** Adjacent (IndiaAI Mission selected but not formally Bhashini-integrated).
- **Compute grant:** ₹177 Cr ($21M) government compute allocation = effective capital multiplier on $2.2M raised.

---

## 3. Cross-Cutting Themes

### 3.1 Proprietary vs. Commodity Stacks

**Full proprietary stack (models + infra built in-house):**
Sarvam, Gnani, Krutrim, Mihup, Convin, Smallest.ai, Ringg (partial), Soket

**Proprietary models but commodity infra/orchestration:**
CoRover (BharatGPT fine-tuned + NVIDIA Riva speech), Navana (Bodhi STT only), Arrowhead (fine-tuned, base model undisclosed), GreyLabs (STT + fine-tuned LLM)

**Model-agnostic / Orchestration / App layer:**
Bolna (OSS orchestration SDK), Nurix (NuPlay platform on third-party models), Vobiz (telephony infra only), Pype (Pipecat + Azure OpenAI), Fundamento (LLM-agnostic + Dialecto ASR), SpeakX (Google Gemini), Stimuler (Hume AI EVI + WhisperS2T)

**Key insight:** 12 of 19 companies claim some proprietary model element; 7 are commodity/orchestration. However, of the 12 claiming proprietary models, only Sarvam, Gnani, Mihup, and Smallest.ai have verifiable model artifacts (HF weights, arXiv papers, or auditable benchmarks). Convin, Arrowhead, Fundamento, and GreyLabs have zero verifiable public model evidence.

### 3.2 Bhashini / Government Exposure

| Company | Bhashini Status | IndiaAI Mission |
|---|---|---|
| Sarvam | Primary integration (600 Cr+ API requests) | Yes — sovereign LLM winner |
| CoRover | Fully integrated | Not mentioned |
| Gnani | Bhashini finalist | Yes — selected |
| Soket | Adjacent (no formal API) | Yes — ₹177 Cr compute grant |
| Krutrim | Partial (BharatSah'AI'yak adjacent) | No (lost to Sarvam) |
| All others (14) | None | No |

**Risk concentration:** Sarvam and CoRover have significant government revenue dependency. Sarvam's IndiaAI Mission win and UIDAI/Bhashini relationships create a regulatory moat but also a single-counterparty revenue risk (government budget cycles, policy changes, elections).

### 3.3 Revenue Conflicts (MCA vs. Self-Reported)

All conflicts logged; MCA filings are treated as more reliable (audited, legally filed):

| Company | Claimed (source) | MCA FY2025 | Inflation Factor | Verdict |
|---|---|---|---|---|
| Convin.ai | $22.7M ARR (Latka) | Not available | Unknown | ⚠️ Implausible vs. $8.94M raised |
| GreyLabs | $11M ARR (Latka) | ₹3.81 Cr (~$450K) | ~24× | ⚠️ Extreme — treat as unverified |
| CoRover | $10.5M (Latka) | ₹12 Cr (~$1.43M) | ~7× | ⚠️ Likely includes multi-year TCV |
| SpeakX | $7.5M ARR (self) | ₹9.63 Cr (~$1.15M) | ~6.5× | ⚠️ ARR may be run-rate from recent months |
| Krutrim | ₹101.7 Cr FY25 | ₹101.7 Cr (MCA) | 90% related-party | ⚠️ Real third-party revenue ~₹10 Cr |

**Pattern:** ARR is commonly inflated 5–25× versus MCA-reported annual revenue in Indian AI startups. Analysts should anchor to MCA for capital efficiency comparisons.

### 3.4 Capital Efficiency Ranking
*(Revenue per $1M raised; MCA figures used where available; ARR used only if MCA unavailable)*

| Rank | Company | Revenue | Raised | $/M Ratio |
|---|---|---|---|---|
| 1 | Gnani.ai | ₹53.87 Cr (~$6.5M) | ~$28M | ~$232K/$1M |
| 2 | Mihup | ₹20.2 Cr (~$2.4M) | ~$10.8M | ~$222K/$1M |
| 3 | Navana.ai | ₹2.13 Cr (~$251K) | ~$0.8M | ~$314K/$1M |
| 4 | Stimuler | ₹3.16 Cr (~$380K) | ~$5.75M | ~$66K/$1M |
| 5 | Fundamento | ₹4.13 Cr (~$495K) | ~$5.4M | ~$92K/$1M |
| 6 | GreyLabs (MCA) | ₹3.81 Cr (~$450K) | ~$10.2M | ~$44K/$1M |
| 7 | Bolna | ~$700K ARR | ~$6.3M | ~$111K/$1M |
| 8 | Convin (MCA est.) | Unavailable | ~$8.94M | — |
| 9 | Nurix | ₹5.35 Cr (~$640K) | ~$25M+ | ~$26K/$1M |
| 10 | SpeakX (MCA) | ₹9.63 Cr (~$1.15M) | ~$28M+ | ~$41K/$1M |
| 11 | Smallest.ai | ₹93.2L (~$110K) | ~$8.26M | ~$13K/$1M |
| 12 | Sarvam | ₹29.1 Cr (~$3.5M) | ~$391M | ~$9K/$1M |
| 13 | Krutrim (adj.) | ~₹10 Cr adj. (~$1.2M) | ~$280M | ~$4K/$1M |
| 14 | Arrowhead | ₹71.2L (~$85K) | ~$3M | ~$28K/$1M |
| 15 | Pype AI | ₹3.35L (~$4K) | ~$1.2M | ~$3K/$1M |
| — | Vobiz, Ringg, Soket | Not disclosed | — | — |

**Note:** Navana, Gnani, and Mihup are the three most capital-efficient companies. Sarvam and Krutrim are intentionally capital-heavy for frontier model development — comparing them on efficiency alone is misleading.

### 3.5 Moat Scores Ranked

| Rank | Company | Moat Score | Primary Moat Type |
|---|---|---|---|
| 1 | Sarvam AI | 4/5 | Data flywheel + government mandate + scale |
| 1 | CoRover.ai | 4/5 | Government deployments + 12B+ interaction data |
| 3 | Gnani.ai | 3.5/5 | 1M hrs proprietary ASR data + profitability |
| 3 | GreyLabs AI | 3.5/5 | Cogno alumni pedigree + BFSI domain data |
| 5 | Arrowhead | 3/5 | BFSI vertical focus (unverified technical depth) |
| 5 | Convin.ai | 3/5 | G2 #1 badge + named enterprise customers |
| 5 | Krutrim | 3/5 | GPU cloud infra + dataset (models paused) |
| 5 | Mihup | 3/5 | 1M Tata Motors vehicles (physical deployment) |
| 5 | Soket | 3/5 | 44.4M HF downloads + IndiaAI Mission compute |
| 10 | Bolna AI | 2.5/5 | 639 GitHub stars + OSS developer community |
| 10 | Navana.ai | 2.5/5 | NeurIPS dataset + Bajaj Finance production |
| 10 | Smallest.ai | 2.5/5 | arXiv paper + hardware co-design |
| 10 | SpeakX | 2.5/5 | 10M+ downloads + EBITDA positive |
| 10 | Stimuler | 2.5/5 | 85% international revenue diversification |
| 15 | Fundamento | 2/5 | IIFL distribution + Dialecto ASR |
| 15 | Nurix AI | 2/5 | Enterprise customer credibility only |
| 15 | Pype AI | 2/5 | Healthcare vertical + OSS tools |
| 15 | Ringg AI | 2/5 | HF Space of the Week validation |
| 15 | Vobiz.ai | 2/5 | Telephony infra layer positioning |

---

## 4. Investment Landscape Summary

### 4.1 Total Capital Deployed
- **Approximate total (all 19 companies):** ~$856M+
- **Top 2 companies (Sarvam + Krutrim):** ~$671M = 78% of total cohort capital
- **Excluding top 2:** ~$185M across 17 companies (median ~$10M per company)

### 4.2 Round Size Distribution

| Stage | Companies | Count |
|---|---|---|
| Pre-Seed | Pype AI | 1 |
| Seed | Vobiz, Bolna, Ringg, Smallest, Arrowhead, Soket | 6 |
| Pre-Series A | Navana, Fundamento, Stimuler | 3 |
| Series A | Gnani (prior), Nurix, GreyLabs, Mihup, CoRover, Convin | 6 |
| Series B | Gnani (current) | 1 |
| Pre-Series B | SpeakX | 1 |
| Growth / Unicorn | Krutrim | 1 |
| Closing Large Round | Sarvam | 1 |

**Median round size (excluding Sarvam + Krutrim):** ~$5.5–6.5M

### 4.3 Most Active Investors (2+ portfolio companies in cohort)

| Investor | Portfolio Companies | Notes |
|---|---|---|
| General Catalyst | Nurix AI, Bolna AI | Two competing orchestration platforms |
| Lightspeed (India) | Sarvam AI, Stimuler, Soket | Spread across full-stack, EdTech, OSS lab |
| Elevation Capital | SpeakX, GreyLabs AI | Two back-to-back Oct 2025 voice AI bets |
| Kunal Shah (CRED) | Arrowhead, Ringg AI | Angel in two BFSI voice platforms |

### 4.4 Notable Co-investors / Strategic

- **NVIDIA:** Sarvam AI (Series B lead signal — GPU + model validation)
- **Amazon:** Sarvam AI (Series B — AWS India distribution)
- **HDFC Bank:** CoRover.ai (strategic, Aug 2025 — private sector banking validation)
- **Ashish Kacholia + Madhusudan Kela:** Mihup (market operator credibility for IPO path)
- **IIFL Fintech Fund:** Fundamento (NBFC distribution access)
- **The Players Fund (KL Rahul, Ben Stokes):** Fundamento (celebrity diversification)
- **Piper Serica VC Fund:** Vobiz (India-focused micro-fund, infra conviction)
- **YC (F25):** Bolna (global developer community signal)

### 4.5 Funding Velocity (2025–2026 rounds)

| Period | Companies Raising |
|---|---|
| May 2026 | Vobiz ($1M) |
| Apr 2026 | Sarvam (~$350M closing), Stimuler ($3.75M) |
| Mar 2026 | Gnani ($10M), Nurix (~$16M), Soket ($2.2M) |
| Jan 2026 | Bolna ($6.3M), Ringg ($5.5M), Arrowhead ($3M) |
| Nov 2025 | Pype ($1.2M) |
| Oct 2025 | Smallest ($8.26M), SpeakX ($16M), GreyLabs (~$10.2M), Fundamento ($1.9M) |
| Sep 2024 | CoRover ($4M) |
| Aug 2024 | Convin ($6.5M) |
| Sep–Nov 2024 | Mihup ($10.8M) |
| Jul 2025 | Navana (₹7 Cr) |
| Jan 2024 | Krutrim ($50M unicorn) |

**Observation:** Q4 2025 and Q1 2026 were the hottest funding quarters for India voice AI — 10 of 19 companies raised between Oct 2025 and Mar 2026.

---

## 5. Gaps — Biggest Information Gap Per Company

| Company | Biggest Gap |
|---|---|
| **Sarvam AI** | Actual customer-specific revenue breakdown (Bhashini vs. enterprise vs. IndiaAI Mission contract value); FY2026 MCA not yet filed |
| **Krutrim** | Real third-party (non-Ola) revenue for FY2026; model roadmap post-pivot (Krutrim-3 timeline, chip program status) |
| **Gnani.ai** | Inya VoiceOS 5B benchmark comparisons vs. Sarvam-m / OpenAI Realtime; exact Bhashini API volumes |
| **Nurix AI** | Customer names and NuPlay platform demo — no verifiable product artifact exists publicly |
| **Ringg AI** | Parrot STT V1 benchmark methodology (15% WER on what test set?); actual customer deployments in MENA |
| **Bolna AI** | Enterprise vs. self-serve revenue split; churn rate on $700K ARR; path to profitability given MIT license |
| **Arrowhead** | Working GitHub/HuggingFace presence — zero verifiable technical assets; co-founder departure impact on product |
| **Pype AI** | Hospital customer count and go-live deployments; whether 20+ language claim is operational or aspirational |
| **Smallest.ai** | HuggingFace model weights for Pulse/Lightning/Electron — no models published; Lightning TTS benchmark vs. Sarvam Bulbul |
| **GreyLabs AI** | Revenue source reconciliation: $11M Latka vs ₹3.81 Cr MCA — need FY2026 MCA or audited accounts |
| **SpeakX** | ARR methodology ($7.5M claimed vs ₹9.63 Cr MCA) — is this monthly ARR × 12 or TTM? Retention rate on 10M downloads |
| **Fundamento** | Dialecto ASR benchmark data; evidence for 30+ language claim; RBI compliance status for automated collections calls |
| **Stimuler** | Hume AI EVI contract terms (exclusivity, pricing, API limits); Indonesia vs. India revenue breakdown |
| **Mihup** | 120+ language claim evidence; Qualcomm NPU deployment timeline; IPO readiness (DRHP filing date) |
| **CoRover.ai** | Revenue reconciliation $10.5M Latka vs ₹12 Cr MCA; HDFC Bank strategic investment amount; BharatGPT 3B commercial license terms |
| **Convin.ai** | $22.7M revenue claim source and methodology — implausible vs. total funding; FY2025 MCA filing (not found in dossier) |
| **Navana.ai** | RESPIN-S1.0 WER benchmarks by language; Ujjivan SFB deployment status; TTS roadmap (currently ASR-only) |
| **Vobiz.ai** | Any disclosed customer or revenue — no commercial traction evidence exists publicly; team size and technical team composition |
| **Soket AI Labs** | TensorStudio ARR; Project EKA 120B timeline and compute allocation plan; DHRITH ASR benchmark vs. Sarvam Saaras |

---

*End of comparison matrix. All figures sourced from individual company dossiers as of their respective collection dates. MCA = Ministry of Corporate Affairs annual filings (most reliable). GetLatka = self-reported, treat as ARR upper bound. Stars/downloads as of dossier collection date. For live data, verify via company websites, MCA portal, HuggingFace, and GitHub.*
