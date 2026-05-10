# Krutrim

**Website:** https://olakrutrim.com  •  **HQ:** Bangalore (Koramangala), Karnataka, India  •  **Founded:** April 2023  •  **Stage:** Growth (post-unicorn, profitable as of FY26)
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch: India's first AI unicorn — a full-stack Indic AI company building multilingual LLMs, voice/vision models, and a sovereign GPU cloud, all optimized for India's 22 official languages.
- Total funding to date: ~$280M+ (equity + debt), plus $230M founder injection (Feb 2025)
- Last round: $230M personal investment by Bhavish Aggarwal via family office, Feb 2025; committed $1.2B total by end of 2026
- Headcount: ~549 (as of Aug 31, 2025, per Tracxn/reports); down from ~600+ in linguistics team alone in early 2025 after 200+ layoffs across 2025
- Revenue / ARR: FY26 ~₹300 crore (~$36M), 3x YoY growth; first net profit (>10% margin). FY25: ₹101.7 crore, ~90% from Ola group entities (related-party revenue)

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| Oct 2023 | Debt | $24M | Matrix Partners India | — | Entrackr, YourStory |
| Jan 2024 | Series A (equity) | $50M | Matrix Partners India | — | TechCrunch, Bloomberg, Inc42 |
| Feb 2025 | Founder injection (equity + debt) | $230M | Bhavish Aggarwal (family office) | — | TechCrunch |
| Ongoing | Internal / Ola group | Not separately disclosed | Ola group | Ola Electric, ANI Technologies | Business Standard |

**Post-money valuation (Jan 2024):** $1B — India's first AI unicorn and 2024's first unicorn overall (achieved in ~40 days, fastest in Indian history).

**Note:** Krutrim pledged a total of $1.2B investment commitment by end-of-2026 (announced Feb 4, 2025). As of May 2026 the company states it is "financially self-sustaining" with no immediate external funding need.

**Bhavish's other unicorns:** Ola Consumer (Ola Cabs) and Ola Electric — Matrix Partners India backed all three.

## 3. Product & Customers

### Products
| Product | Description | Status (May 2026) |
|---------|-------------|-------------------|
| **Krutrim-2 (LLM)** | 12B-param multilingual LLM, Mistral-NeMo base, 22 Indian languages + English, 128K context, open-sourced Feb 2025 | Active; Krutrim-3 development stalled |
| **Krutrim-1 (LLM)** | 7B-param foundational model, trained Oct–Nov 2023 on 2T tokens, 10 Indic languages | Active (open-sourced) |
| **Chitrarth** | Vision-Language Model (VLM), 8B params, built on Krutrim-1, 10 Indic languages + English, image/document understanding | Active |
| **Chitrapathak-1 / -2** | Newer VLMs (8B / 4B params), updated Mar 2026 | Active |
| **Chitranuvad** | Image-to-text translation model | Active |
| **Dhwani** | India's first Speech Language Model (SLM); speech-to-text + translation between Indic languages and English | Active (open-sourced) |
| **Vyakyarth** | 0.3B multilingual sentence-embedding model for Indic languages; search and RAG use cases | Active |
| **Krutrim Translate** | Text-to-text translation; 10 Indic languages + English | Active |
| **Krutrim Cloud** | Full-stack AI cloud: GPU VMs (A100, H100), object/block storage, DBaaS, Kubernetes, LLM inference APIs, IAM, multi-region (Bangalore + Hyderabad) | Primary revenue driver |
| **Krutrim AI Studio** | API gateway for hosted models (own + third-party, e.g. DeepSeek R1) | Active |
| **BharatBench** | Open Indic evaluation framework (multilingual, multimodal, multitask) | Active |
| **Kruti AI assistant** | Agentic consumer assistant (cab booking, bill payments, food ordering, image generation) | **SHUT DOWN April 2026** |
| **BharatSah'AI'yak** | Acquired from Samagra (Jun 2025); vernacular RAG-based chatbots for government and public sector | Active |

**Key pivot (late 2025 / 2026):** Krutrim paused chip design (Bodhi/Sarv/Ojas chips) and foundation model work (Krutrim-3), shut down the Kruti consumer app, and concentrated entirely on the Krutrim Cloud enterprise business.

### Pricing
- **Krutrim Cloud GPU:** A100 and H100 on-demand and reserved; claimed "50% less expensive" vs global hyperscalers; exact per-hour INR rates not publicly listed — contact sales. No data-transfer fees.
- **LLM API (DeepSeek R1 on Krutrim Cloud):** Promotional rate ₹1/million tokens (Feb 2025); regular rate not published.
- **Own LLM APIs:** Pricing not publicly listed (available on request / via AI Studio).
- **Free tier:** Cloud free trial available with no credit card required (as of early 2025).
- **INR-denominated billing** — differentiator vs AWS/GCP/Azure for Indian enterprises.

### Languages & Voices
- **LLM text:** 22 Indian languages (verified supported languages include Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati, Kannada, Malayalam, Odia, Assamese, Punjabi) + English
- **VLM (Chitrarth):** 10 Indic languages + English
- **ASR/STT (Dhwani):** Indic-to-English and inter-Indic translation; specific language count not publicly detailed
- **TTS:** Not separately released as of May 2026 (Dhwani focuses on ASR/SLM, not TTS synthesis specifically)
- **Embedding (Vyakyarth):** Indic language corpus

### Named Customers
| Customer / Deployment | Sector | Notes |
|----------------------|--------|-------|
| Government of Uttar Pradesh / Prayagraj Mela Authority | Government | Kumbh Sah'AI'yak chatbot for Maha Kumbh 2025, powered by Krutrim LLM + Bhashini translation; PM Modi launched Dec 13, 2024 |
| Odisha State Government (AMA Krushi) | AgriTech / Govt | Voice-enabled agriculture chatbot in local languages (via BharatSah'AI'yak) |
| 25+ enterprise customers (claimed) | Telecom, BFSI, Healthcare | Named customers not disclosed; stated in TechCrunch May 2026 report |
| Ola Electric | Internal (related-party) | ₹26.16 crore in FY25 |
| ANI Technologies (Ola Cabs) | Internal (related-party) | ₹64.63 crore in FY25 |

**Note:** In FY25, ~90% of ₹101.7 crore revenue came from Ola group entities. FY26 mix not disclosed.

### Integrations / SDKs
- Python SDK: `krutrim-cloud-python` (GitHub, 12 stars)
- Go SDK: `krutrim-go-sdk` (GitHub)
- Terraform provider: `terraform-provider-krutrim` (GitHub)
- AWS-compatible APIs (S3-compatible object storage etc.)
- Python, Node.js, Go, Java, Rust client support
- Models on HuggingFace (`krutrim-ai-labs` org)

## 4. Technical Architecture

### Model approach
- **Krutrim-1:** Dense transformer, 7B params, SentencePiece BPE tokenizer trained from scratch for Indic + English. Trained Oct–Nov 2023 on 2T tokens (web, books, code, Indic data). Claimed largest Indic training corpus at time of release.
- **Krutrim-2:** Dense transformer, 12B params, built on **Mistral-NeMo** architecture. 40 layers, Group Query Attention (GQA), RoPE positional embeddings, 131K vocabulary. Trained Dec 2024 – Jan 2025. Multi-stage training (varying data mix, context size, batch size). Post-training: SFT (instruction following) → DPO → RLVR. 128K token context window.
- **Chitrarth:** VLM, 8B, image-text-to-text, Krutrim-1 as base LLM. Trained on multilingual image-text data.
- **Dhwani:** Speech Language Model built on Krutrim-1; open-sourced STT/translation capabilities.
- **Vyakyarth:** 0.3B sentence embedding model.
- **Krutrim Translate:** Fine-tuned translation model, 10 Indic + English.

### Training data
- Krutrim-1: **2 trillion tokens** — web scraping + deduplication + quality filtering. Claims largest known Indic dataset distribution. Indic languages represent <1% of Common Crawl, so proprietary Indic data sourcing is a key differentiator.
- Krutrim-2: "Hundreds of billions of tokens" of Indic content + English web + code + math + synthetically generated data.
- Sourcing: Web crawl, books, code repositories, licensed/proprietary Indic content; exact data sourcing contracts not disclosed.

### Latency profile
- Not publicly benchmarked with TTFB / RTF numbers as of May 2026.
- Cloud inference: streaming APIs available via Krutrim AI Studio.
- DeepSeek R1 671B deployed on H100s (Jan/Feb 2025) — claimed world-first deployment of this model size.

### Voice cloning
- Not publicly announced as of May 2026. Dhwani covers ASR/STT; TTS voice cloning not released.

### Prosody / emotion control
- Not publicly documented. Dhwani supports speech translation but detailed prosody/emotion control features not confirmed.

### Indic language strategy
- Custom SentencePiece BPE tokenizer trained from scratch (existing tokenizers have high token-to-word ratio for Indic scripts, hurting efficiency).
- Multi-script support (Devanagari, Tamil script, Telugu script, etc.).
- Code-mixing support (Hinglish, etc.).
- Coverage claimed for 22 official Indian languages; benchmarks published for 11 (Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Oriya, Punjabi, Tamil, Telugu).
- BharatBench: Krutrim's own Indic evaluation framework (multimodal, multilingual, multitask).
- VoiceAgentBench: Benchmark for voice agents in English and 6 Indic languages (published Oct 2025, arXiv 2510.07978).

### Inference stack
- NVIDIA A100 and H100 GPU clusters (multi-region: Bangalore + Hyderabad).
- India's first GB200 cluster (announced in partnership with Nvidia, target March 2025).
- Scale-up target: 1 GW data-center capacity by 2028 (from ~20 MW in 2024).
- AWS-compatible APIs; own managed inference pipeline.

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Krutrim LLM: Multilingual Foundational Model for over a Billion People | arXiv paper | Feb 2025 | https://arxiv.org/abs/2502.09642 |
| Krutrim LLM: A Novel Tokenization Strategy for Multilingual Indic Languages with Petabyte-Scale Data Processing | arXiv paper | Jul 2024 | https://arxiv.org/abs/2407.12481 |
| VoiceAgentBench: Are Voice Assistants ready for agentic tasks? | arXiv paper | Oct 2025 | https://arxiv.org/abs/2510.07978 |
| MUTANT | ACL 2026 paper | 2026 | https://github.com/ola-krutrim/MUTANT |
| Krutrim-2: A Best-in-Class LLM for Indic Languages | Blog | Feb 2025 | https://tech.olakrutrim.com/krutrim-2-a-best-in-class-large-language-model-for-indic-languages/ |
| BharatBench: Making AI Understand India | Blog | Feb 2025 | https://tech.olakrutrim.com/bharat-bench/ |

## 5. Open Source Footprint

### GitHub
**Org:** https://github.com/ola-krutrim (self-described "India's Frontier AI Research Lab")

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| Dhwani | 19 | 5 | — | Active 2025 | Speech Language Model code |
| Krutrim-2-12B | 18 | 6 | Krutrim Community License | Active 2025 | 12B LLM weights/code |
| ai-cloud | 14 | 4 | — | Active | Cloud platform SDK/tools |
| Chitrarth | 13 | 2 | — | Active 2025 | VLM ("Bridging Vision and Language for a Billion People") |
| krutrim-cloud-python | 12 | 1 | — | Active | Official Python SDK for Krutrim Cloud API |
| Krutrim-1-7B | 11 | 1 | — | Active | Original 7B LLM |
| IndicEvalHarness | 5 | 1 | — | Active | Indic evaluation framework |
| VoiceAgentBench | 3 | 1 | — | Active | Voice agent benchmark, 6 Indic languages |
| ForgeLM | 2 | 0 | — | Active | Jupyter Notebook (LM fine-tuning utilities) |
| MUTANT | 1 | 0 | — | Active | ACL 2026 research code |
| terraform-provider-krutrim | 0 | 0 | — | Active | Terraform provider for Krutrim Cloud |
| krutrim-go-sdk | 0 | 0 | Go | Active | Go SDK |
| Krutrim-client-python | — | 1 | — | — | Python client SDK |
| Chitranuvad | 0 | 0 | — | — | Image-text translation model |
| Chitrapathak | 0 | 0 | — | — | Newer VLM |
| IndicVisionBench | 0 | 0 | — | — | Vision benchmark for Indic languages |

**Overall signal:** Low community traction (most repos <20 stars), consistent with an early-stage research org rather than a broad developer platform. No viral OSS project.

### Hugging Face
**Org:** https://huggingface.co/krutrim-ai-labs

| Model | Downloads | Likes | License | Notes |
|-------|-----------|-------|---------|-------|
| Vyakyarth (0.3B embedding) | 4,160 | 15 | — | Highest model downloads |
| Chitrapathak-2 (4B VLM) | 424 | 1 | — | Newer VLM |
| MUTANT_data (dataset) | 449K | 220 | — | Highest dataset downloads; ACL 2026 |
| BhashaKritika (dataset) | 16.2M | 1,330 | — | Largest dataset by downloads |
| VoiceAgentBench (dataset) | 5,390 | 766 | — | Strong benchmark interest |
| IndicVisionBench (dataset) | 7,270 | 76 | — | Vision benchmark |
| Krutrim-2-instruct | 47 | 36 | Krutrim Community License | Most liked model |
| Chitrarth (8B VLM) | 137 | 18 | — | |
| Krutrim-1-instruct (7B) | 51 | 15 | — | |
| Dhwani (STT) | 15 | — | — | Low downloads |
| Krutrim-Translate | 7 | — | — | Very low traction |

**Overall HF signal:** Datasets (especially BhashaKritika at 16.2M downloads and MUTANT_data at 449K) attract far more interest than model weights. Model downloads are low (Krutrim-2-instruct: 47), suggesting limited community adoption of the models themselves.

### Top contributors
- **Chandra Khatri** — Founding Head of AI; co-authored technical reports
- **Aditya Kallappa** — Lead author on Krutrim LLM arXiv paper (arXiv 2502.09642); 12 co-authors listed
- Core team of ~12 researchers visible in academic output; individual contributor GitHub activity not publicly prominent

## 6. Team

### Founders
| Name | Role | Background |
|------|------|------------|
| **Bhavish Aggarwal** | Founder & CEO | B.Tech Computer Engineering, IIT Bombay (2008); AIR 23 JEE; research intern then assistant researcher at Microsoft Research India (2008–2010, filed 2 patents, 3 journal papers); Co-founder & CEO Ola Cabs (2010); Founder Ola Electric (2017, IPO 2024); Founder Krutrim (2023). Time 100 (2018). Net worth ~$2.3B. |
| **Krishnamurthy Venugopala Tenneti** | Co-founder | Board member of ANI Technologies (Ola Cabs parent). Less operationally visible than Aggarwal. |

### Key technical hires
| Name | Title | Background |
|------|-------|------------|
| **Chandra Khatri** | Founding Head of AI | Prior: Co-founder Got-It AI (enterprise LLM/hallucination detection); Uber AI, Amazon Lab126, eBay, Oracle; Georgia Tech; BITS Pilani. LinkedIn: linkedin.com/in/ckhatri |
| **Raguraman Barathalw** | CTO & VP Engineering | Details limited in public sources |
| **Sunit S** | SVP Product | Hired ~2024–2025; background in product management |

### Recent joiners (last 12mo)
- Krutrim AI Labs (Feb 2025 launch) triggered a hiring push in the US (Palo Alto, SF), Singapore, and Bengaluru for GenAI research engineers, distributed training specialists, speech/audio research scientists, AI alignment/RL engineers, and cloud platform engineers.
- Samagra's core AI team onboarded as part of the BharatSah'AI'yak acquisition (Jun 2025).

### Notable departures (last 12mo)
- ~12+ senior executives departed in 2024 (reported by Outlook Business).
- 20+ exits in FY25 alone.
- Linguistics team reduced from ~600 to ~400 via layoffs.
- Chief reasons cited: frequent strategy pivots (Aggarwal's "Perplexity-like" direction shift mid-2024), unrealistic deadlines, and leadership churn at VP/director level.

### Open roles signal
- As of early 2026, roles shifted to cloud infrastructure, enterprise sales, and DevRel — consistent with cloud pivot.
- Foundation model research hiring largely paused post-restructuring.

## 7. Moat & Defensibility

- **Data moat:** Krutrim built the largest known Indic language training corpus (~2T tokens), with proprietary web-crawled and curated Indic data — a structural advantage given Indic languages represent <1% of Common Crawl. Ola's ride-hailing data (voice commands, routing, payments in Indian contexts) is a secondary asset but not confirmed as training data. BhashaKritika dataset (16.2M HF downloads) signals unique data creation capability. **Rating: 3.5/5** — strong for Indic LLM training, but replicable by a well-funded team over 12–18 months.

- **Model moat:** Krutrim-2 (12B, Mistral-NeMo base) is competitive but not clearly differentiated from Sarvam, AI4Bharat's IndicTrans2/Dhruva, or fine-tuned international models. Krutrim-3 is stalled. BharatBench, VoiceAgentBench, and academic output (ACL 2026) demonstrate research credibility. **Rating: 2.5/5** — decent but not frontier; pivot away from model work weakens this further.

- **Distribution moat:** Ola ecosystem (Ola Cabs, Ola Electric) provides a captive early customer base and brand familiarity with enterprise India. Kumbh Mela government deployment (PM Modi-launched) establishes public sector credibility. BharatSah'AI'yak acquisition brings government AI pipeline. 25+ enterprise cloud customers (telecom, BFSI, healthcare) in early 2026. INR billing + India-residency data sovereignty differentiates from AWS/GCP for regulated sectors. **Rating: 3.5/5** — real but still nascent; 90% related-party revenue in FY25 shows external distribution is underdeveloped.

- **Brand / community moat:** "India's first AI unicorn" narrative is powerful in domestic media and government circles. Bhavish Aggarwal's personal brand is high-profile but polarising (see risks). GitHub/HF community engagement is low. Kruti app shutdown hurt consumer brand. **Rating: 2/5** — brand recognition but not community loyalty.

- **Regulatory moat:** India's data localisation push (DPDP Act 2023, rules 2025) and sovereign AI preferences favour domestic cloud providers. Government selection of Sarvam AI for the IndiaAI Mission sovereign LLM (April 2025) is a setback — Krutrim was **not** selected. However, Krutrim's public sector deployments (Kumbh, Odisha agriculture) and BharatSah'AI'yak acquisition keep it in the government AI vendor ecosystem. **Rating: 2.5/5** — favourable macro but lost the key government contract to Sarvam.

- **Replication cost (6mo, $10M competitor):** A well-capitalised team ($10M) could NOT replicate Krutrim Cloud's full-stack GPU infrastructure in 6 months (hardware lead times, DC build-out). A 12B-param Indic-optimised LLM (Krutrim-2 equivalent) is replicable by a larger team ($50M+, 12–18 months) given Mistral-NeMo is open. Core differentiation is the proprietary Indic data corpus + cloud infrastructure + government relationships — these take 18–24 months minimum to build. **Estimated replication cost: $75–150M, 18+ months.**

- **Moat strength: 3/5** — Krutrim has a real but fragile moat anchored in Indic data, early-mover brand, and infrastructure investment; the cloud pivot is the right move but the model moat is eroding as global labs improve Indic support.

## 8. Risks & Problems

### Technical complaints
- **Censorship / bias (Feb 2024):** Users reported the Krutrim chatbot applied a double standard — diplomatic about social issues in Muslim communities but blunt/critical for Hindu communities. Widely covered on Twitter/X and Indian media. Source: OpIndia, ITVoice.
- **Factual hallucinations (beta, 2024):** Multiple reports of incorrect historical answers, confusion about the chatbot's origin, short effective context window. Source: ITVoice.
- **Kruti app failure:** Kruti AI assistant (agentic) reached <500K downloads before being pulled from app stores in April 2026 without announcement. Compared to ChatGPT's 110M India users and Sarvam's Indus app crossing 50K downloads in one week. Source: MediaNama, SensorTower data cited in reports.
- **Krutrim-3 stalled:** Development halted as part of late-2025 restructuring. Source: MediaNama, LetsDatScience.
- **Low HF/GitHub community adoption:** Krutrim-2-instruct has only 47 downloads on HuggingFace as of May 2026.

### Pricing pain points
- Cloud pricing not publicly listed (requires sales contact for most tiers).
- LLM API pricing structure opaque vs Sarvam (which publishes ₹15/10K chars for TTS, ₹30/hr for STT).
- DeepSeek R1 at ₹1/M tokens was a Feb 2025 promo — standard rates unclear.

### Safety / misuse
- Political bias allegations in early chatbot (see above).
- No public AI safety policy, red-teaming reports, or responsible disclosure program as of May 2026.
- DPDP Act 2023 compliance: Krutrim processes personal data for government deployments (Kumbh chatbot) — DPDP Rules 2025 compliance status not publicly disclosed.

### Legal / regulatory
- **Engineer suicide case (May 2025):** Nikhil Somwanshi (25, IISc grad, joined Krutrim <1 year prior) found dead in Agara Lake, Bengaluru, on May 18, 2025. A Reddit post alleged toxic work culture, excessive workload after team members quit, and verbal abuse by a US-based manager. Bengaluru police filed FIR; manager summoned for questioning. Second case: Bhavish Aggarwal named in a police probe after a 38-year-old Ola Electric employee found dead, with note alleging management harassment (Oct 2025). These incidents generated sustained negative press and workforce morale impact. Source: Business Standard, Storyboard18, The Federal.
- **Related-party governance concern:** Board has no independent directors. 90% FY25 revenue from Ola group. Questions raised by analysts about director conflicts (same directors on Ola Electric and ANI Technologies boards). Source: NewsBytesApp.
- **DPDP Act / AI regulation:** No known active regulatory action against Krutrim specifically, but as a large data processor operating government chatbots, exposure to DPDP Rules 2025 is material.
- **No known IP litigation** as of May 2026.

### Churn signals
- ~12 senior executives departed in 2024; 20+ exits in FY25.
- Multiple layoff waves: 100+ Jun–Jul 2025, 50 more Oct/Nov 2025 (total ~200+ employees cut).
- Linguistics team cut from ~600 to ~400.
- Kruti consumer app shut down without warning.
- Last X (Twitter) post by Krutrim official account: December 2024 — social media silence of 5+ months.
- Krutrim missed the India AI Impact Summit (Feb 2026) entirely — competitor Sarvam launched Sarvam-105B at the event; Krutrim had no presence. Source: BusinessToday.

## 9. Competitive Position

- **Direct competitors:**
  - *India, LLM:* Sarvam AI (government-selected sovereign LLM; 4,000 H100 GPUs; selected for IndiaAI Mission Apr 2025), AI4Bharat / IIT Madras (IndicTrans2, Dhruva, open research)
  - *India, Cloud:* Yotta Infrastructure, NxtGen, E2E Networks, Tata Communications, Reliance Jio (committed $120B AI investment Feb 2026)
  - *Global:* OpenAI (GPT-4o, 110M India users), Google Gemini, Meta Llama 3 (free, strong Indic support), Mistral, Anthropic

- **Where it's winning:**
  - Indic language data corpus — remains deepest proprietary dataset for 22 Indian languages
  - Government public-sector AI deployments (Kumbh chatbot; Odisha agriculture bot) — credibility with state governments
  - INR-billed sovereign GPU cloud with India data residency — traction with compliance-sensitive enterprise customers
  - First-mover brand as "India's AI unicorn" — still resonates in Indian enterprise sales
  - Academic research output (VoiceAgentBench, BharatBench, ACL 2026 MUTANT) — growing research credibility

- **Where it's losing:**
  - Government sovereign LLM contract: Sarvam AI won the IndiaAI Mission contract (Apr 2025); Krutrim not selected
  - Consumer AI: Kruti app shut down, <500K users vs ChatGPT's 110M India users
  - Developer community: Low GitHub/HF adoption; Sarvam's Indus app crossed 50K downloads in one week
  - Model frontier: Krutrim-3 stalled; Sarvam launched 105B param model; global labs rapidly improving Indic support
  - Chip ambitions: Bodhi/Sarv/Ojas chip program paused — surrender of a long-term differentiator

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| Jun 2025 | Launched Kruti agentic AI assistant app | Medianama, YourStory |
| Jun 2025 | Acquired BharatSah'AI'yak from Samagra for government AI expansion | Business Standard, Entrackr |
| Jul–Aug 2025 | First wave of 100+ layoffs, primarily linguistics team | Business Standard, Outlook Business |
| Oct 2025 | Second layoff wave, 50 more roles cut; total ~200+ | Angelone/Inc42 |
| Oct 2025 | VoiceAgentBench paper published (arXiv 2510.07978) | arXiv |
| Oct 2025 | Bhavish Aggarwal named in police probe re: Ola Electric employee death | Business Standard |
| Late 2025 | Business restructuring: paused chip design + AI model work; reallocated capital to cloud | TechCrunch, Medianama |
| Dec 2025 | Official Krutrim X account goes silent (last post Dec 2024) | Observed |
| Dec 2024 | PM Modi launches Kumbh Sah'AI'yak app, powered by Krutrim | Business Standard |
| Feb 4, 2025 | Krutrim AI Lab launch; Krutrim-2 (12B), Chitrarth, Dhwani, Vyakyarth open-sourced; $230M investment + $1.2B commitment; Nvidia GB200 cluster announced | BusinessWire, TechCrunch |
| Feb 11, 2025 | DeepSeek R1 671B deployed on Krutrim Cloud H100s; ₹1/M tokens promo pricing | Business Standard, LatestLY |
| May 2025 | Nikhil Somwanshi (IISc engineer) found dead; toxic culture allegations; police FIR | Business Standard, Storyboard18 |
| Feb 2026 | India AI Impact Summit — Krutrim absent; Sarvam launches Sarvam-105B | BusinessToday |
| Apr 2026 | Kruti AI assistant pulled from app stores without announcement | Medianama, Entrackr |
| May 2026 | Reports confirm: cloud pivot, chip pause, model pause; FY26 revenue ₹300 crore, first profit >10% margin; 25+ enterprise cloud customers | TechCrunch, Business Standard, Entrackr |

**Velocity verdict: Decelerating on model/product ambition; stabilizing on cloud revenue.** The strategic pivot to cloud is pragmatic and financially validated (first profit, 3x revenue), but the narrative arc has shifted from "India's AI champion building frontier models" to "India's AI-first cloud provider." Competitor Sarvam is filling the frontier-model narrative vacuum. Krutrim's velocity in model development is clearly slowing; cloud business velocity is solid but not explosive.

## 11. Bull Case / Bear Case

**Bull:**
- India's cloud market is enormous and growing; Krutrim's INR-billed, data-sovereign GPU cloud is well-positioned for BFSI, healthcare, and government workloads that cannot use foreign clouds.
- First profitable quarter in FY26 with 3x revenue growth proves the cloud business model is working.
- 25+ enterprise customers with GPU capacity "mostly committed" — real revenue traction.
- Indic AI data moat (BhashaKritika, 2T-token corpus) is hard to replicate and could be monetised as training-data-as-a-service.
- Government AI deployments (Kumbh, agriculture) create public-sector beachhead; BharatSah'AI'yak acquisition deepens this.
- If global AI competition intensifies and India mandates data localisation more strictly, Krutrim benefits disproportionately.
- Bhavish Aggarwal has built two unicorns before; personal $230M commitment signals high conviction.

**Bear:**
- 90% of FY25 revenue was related-party (Ola group); true third-party cloud ARR in FY26 is unknown.
- Sarvam AI won the IndiaAI Mission sovereign LLM contract — the most important government AI deal in India's history — and Krutrim was not selected.
- Chip design program (Bodhi/Sarv/Ojas) paused indefinitely — lost potential long-term cost and sovereignty advantage.
- Krutrim-3 stalled; model capability will fall further behind frontier (Sarvam-105B, GPT-5, Gemini 2.x) while Krutrim focuses on cloud infrastructure.
- Workplace culture crisis (two engineer deaths, police probes, high attrition) is a real talent-risk and brand-risk in a tight AI talent market.
- Bhavish Aggarwal's reputation is now multi-front: Ola Electric share price down ~42.8% YTD (as of mid-2025), pledging OLA Electric shares to fund Krutrim, personal governance questions.
- No independent board directors — governance risk if fundraising from institutional investors resumes.
- Reliance Jio's $120B AI commitment (Feb 2026) will bring massive GPU capacity and distribution to the market, potentially crowding out Krutrim Cloud's positioning.

## 12. What I Couldn't Find
- Exact per-GPU-hour pricing for Krutrim Cloud A100/H100 (not publicly listed; requires sales contact)
- Exact per-million-token pricing for Krutrim's own LLM APIs (Krutrim-2, Dhwani, etc.)
- Current LinkedIn headcount (exact, as of May 2026) vs 6 months ago — 549 figure is from Aug 31, 2025
- Full investor list for the $50M Series A (only Matrix Partners India confirmed; other investors not named in public filings)
- Financial terms of BharatSah'AI'yak acquisition (not disclosed)
- Details on whether the Nvidia GB200 cluster actually went live by March 2025 as announced
- Voice cloning or TTS product specs (Krutrim has not released a TTS model publicly)
- Krutrim-3 technical specs (development stalled)
- Named customers with case study links for the 25 enterprise cloud customers
- CIN/MCA details for the main operational entity (KRUTRIM SI DESIGNS PRIVATE LIMITED, CIN U62099KA2023PTC171879, incorporated Apr 5, 2023) — full MCA filings not verified
- Board composition and independent director details
- Exact data partnership agreements for the 2T token training corpus

## Sources
1. https://techcrunch.com/2026/05/05/indias-first-genai-unicorn-shifts-to-cloud-services-as-ai-model-ambitions-face-reality/
2. https://techcrunch.com/2024/01/26/ola-founder-ai-startup-krutrim-unicorn-in-50m-funding/
3. https://techcrunch.com/2025/02/04/softbank-backed-billionaire-to-invest-230m-in-indian-ai-startup-krutrim/
4. https://www.business-standard.com/companies/start-ups/bhavish-aggarwal-s-ai-startup-krutrim-turns-unicorn-after-raising-50-mn-124012600652_1.html
5. https://www.business-standard.com/companies/start-ups/krutrim-reports-first-profit-triples-revenue-as-it-pivots-to-ai-cloud-126050401703_1.html
6. https://inc42.com/buzz/indias-fastest-unicorn-krutrim-ai-becomes-bhavish-aggarwals-3rd-unicorn-2024s-and-indias-1st-ai-unicorn/
7. https://www.medianama.com/2026/05/223-krutrim-ai-cloud-chip-ai-model-work/
8. https://www.medianama.com/2026/04/223-olas-krutrim-shuts-down-agentic-ai-assistant-kruti/
9. https://entrackr.com/news/krutrim-pivots-to-ai-cloud-clocks-rs-300-cr-revenue-in-fy26-11800907
10. https://entrackr.com/2024/01/bhavish-aggarwals-ai-startup-krutrim-turns-unicorn/
11. https://www.outlookbusiness.com/magazine/ola-ai-unicorn-krutrim-faces-crisis-amid-leadership-strain
12. https://arxiv.org/abs/2502.09642
13. https://arxiv.org/abs/2407.12481
14. https://arxiv.org/abs/2510.07978
15. https://tech.olakrutrim.com/krutrim-2-a-best-in-class-large-language-model-for-indic-languages/
16. https://huggingface.co/krutrim-ai-labs
17. https://github.com/ola-krutrim
18. https://www.businesswire.com/news/home/20250204723028/en/Krutrim-Launches-Indias-First-Frontier-Research-AI-Lab-to-Democratise-AI-Innovation-Commits-Investment-of-$1.2-Billion-by-Next-Year
19. https://www.business-standard.com/india-news/ai-firm-krutrim-to-power-kumbh-sahayak-app-for-maha-kumbh-mela-2025-124121300961_1.html
20. https://www.business-standard.com/technology/tech-news/krutrim-acquires-bharatsahaiyak-to-expand-ai-in-public-sector-125062000442_1.html
21. https://www.business-standard.com/companies/news/ola-krutrim-engineer-suicide-workplace-culture-allegations-125051800559_1.html
22. https://www.business-standard.com/companies/news/ola-krutrim-ai-layoffs-kukri-linguistics-team-bhavish-aggarwal-125072800163_1.html
23. https://www.business-standard.com/companies/news/ola-electric-ceo-named-police-probe-engineer-death-bengaluru-125102000717_1.html
24. https://www.outlookbusiness.com/start-up/news/bhavish-aggarwals-krutrim-lays-off-over-100-employees-amid-slow-traction-funding-delays
25. https://www.newsbytesapp.com/news/business/ola-group-finances-ai-start-up-krutrim-raises-governance-concerns/story
26. https://www.itvoice.in/olas-krutrim-ai-faces-backlash-over-censorship-and-performance-issues
27. https://yourstory.com/2025/02/ola-krutrim-launches-krutrim-ai-lab-invests-rs-2000-cr
28. https://yourstory.com/2024/01/bhavish-agarwals-krutrim-raises-50m-from-martix-fastest-unircorn
29. https://ai-labs.olakrutrim.com/models/Krutrim-LLM-2
30. https://www.bloomberg.com/news/articles/2024-01-26/ola-founder-s-krutrim-becomes-first-1-billion-indian-ai-startup
31. https://www.indiafilings.com/search/krutrim-ai-private-limited-cin-U62013KA2025PTC203329
32. https://tracxn.com/d/companies/krutrim/__JfsrVc2TQCqAdHXKzx6bPk4-PyEcEhpIY5dCtwz3_ds
33. https://www.latestly.com/socially/technology/ola-ceo-bhavish-aggarwal-announces-deployment-of-deepseek-r1-on-krutrim-cloud-making-accessible-to-indian-developers-for-inr-1-per-million-tokens-6635327.html
34. https://restofworld.org/2026/india-frugal-ai-sarvam-krutrim-sovereign/
35. https://www.businesstoday.in/technology/story/what-a-miss-olas-krutrim-fails-to-hail-a-ride-at-indias-biggest-ai-summit-517900-2026-02-25
36. https://www.storyboard18.com/how-it-works/krutrim-employee-found-dead-in-bengaluru-lake-company-issues-statement-66314.htm
37. https://www.caproasia.com/2024/02/01/india-artificial-intelligence-startup-krutrim-founded-by-ola-electric-ceo-bhavish-aggarwal-raised-50-million-at-1-billion-valuation-in-1st-funding-round-led-by-venture-capital-matrix-partners-kruti/
38. https://www.olakrutrim.com/
39. https://www.olakrutrim.com/gpu-services
40. https://en.wikipedia.org/wiki/Bhavish_Aggarwal
41. https://theorg.com/org/krutrim/org-chart/chandra-khatri
42. https://www.linkedin.com/in/ckhatri
43. https://yourstory.com/2024/08/ola-krutrim-to-launch-indias-first-ai-chips-by-2026
44. https://analyticsindiamag.com/ai-news-updates/krutrim-will-power-kumbh-sahayak-app-for-maha-kumbh-2025/
45. https://inc42.com/buzz/krutrim-buys-bharatsahaiyak-to-expand-ai-footprint-across-public-sector/
46. https://github.com/ola-krutrim/IndicEvalHarness
47. https://github.com/ola-krutrim/VoiceAgentBench
48. https://github.com/ola-krutrim/MUTANT
49. https://huggingface.co/krutrim-ai-labs/Krutrim-2-instruct
50. https://x.com/bhash/status/1886687710363955492
