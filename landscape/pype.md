# Pype AI

**Website:** https://pypeai.com  •  **HQ:** Bengaluru, Karnataka, India  •  **Founded:** 2024  •  **Stage:** Pre-Seed
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): Specialty-trained AI voice agents that act as a 24/7 front desk for hospitals and clinics, automating patient scheduling, follow-ups, and care coordination across voice and WhatsApp.
- Total funding to date: $1.2M (USD)
- Last round: $1.2M Pre-Seed, November 18, 2025, led by Kalaari Capital
- Headcount: ~13 employees (as of Mar 2026; per Tracxn); 8 per PitchBook — data inconsistent. Delta vs 6mo ago: not publicly available.
- Revenue / ARR: ₹3.35L annually (as of Mar 31, 2025; per Tracxn — very early/pilot revenue, likely not meaningful ARR)

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| Nov 18, 2025 | Pre-Seed | $1.2M (~₹10.1Cr at ~84 INR/USD) | Kalaari Capital | Wyser Capital, Tenity | Entrackr, MediaBrief, IndianStartupNews [1][2][3] |

**Notes:**
- Only one confirmed round as of May 2026.
- Tracxn lists the round date as "Jan 31, 2025" which conflicts with all press coverage citing Nov 18, 2025 — the Nov 18 date is likely accurate (press date verified).
- Post-money valuation not publicly disclosed.
- INR equivalent is approximate; article sources did not state INR figure directly.

**Investor profiles:**
- **Kalaari Capital** — Bengaluru-based early-stage VC; contact at Pype deal was Jayraj Bharat Patel (AVP). Portfolio includes Dream11, Myntra, Cure.fit.
- **Wyser Capital** — AI-focused Indian micro-VC founded by Suresh Vaswani, Supria Dhanda, and Satyakam Mohanty; first close of maiden fund at ~₹48Cr (targeting ₹120Cr); focus: Enterprise AI and Agentic AI.
- **Tenity** — Swiss-based fintech/tech VC with global early-stage program (formerly F10 accelerator).

## 3. Product & Customers
### Products
Pype AI ships two distinct products:

**1. Healthcare Voice Agent Platform (core commercial product)**
- Specialty-trained AI voice agents serving as an autonomous hospital front desk
- Automates: appointment scheduling, rescheduling, confirmations, pre-procedure preparation reminders, post-discharge follow-ups, chronic care check-ins, medication adherence monitoring, lab result communication, billing reminders
- 10+ pre-built clinical workflows
- Channels: Voice calls + WhatsApp
- Escalation logic: automatically routes complex/emergency cases to clinical staff
- Deployment: 2-week go-live; self-hosted VPC option; cloud option
- Compliance: HIPAA-certified, SOC 2 certified (claimed on website; not independently verified)
- Security: End-to-end encryption, role-based access control, audit-ready infrastructure
- Performance claims (self-reported): 85%+ patient queries handled autonomously; 60% reduction in no-shows; 28% reduction in readmissions; sub-second response latency; 2M+ calls handled

**2. Whispey (open-source observability platform)**
- URL: https://github.com/PYPE-AI-MAIN/whispey
- Open-source voice AI observability and analytics tool, originally built for LiveKit voice agents
- 40+ compliance, safety, and performance evaluations for clinical environments
- Features: Real-time monitoring dashboard, cost tracking across STT/TTS/LLM providers, latency breakdowns (VAD → STT → LLM → TTS), agent performance metrics, campaign tracking, downloadable recordings and transcripts, multi-project support, self-hostable
- Tech stack: Next.js 14, React, Tailwind CSS, Supabase (PostgreSQL + real-time), Clerk.dev auth, Python SDK
- Latest release: v3.0.0 (September 1, 2025) — OpenTelemetry integrated
- 65 stars, 20 forks on GitHub (as of May 2026)
- Also has enterprise version: `whispey-enterprise` (private/closed repo)

**3. Agensight (open-source experimentation studio)**
- URL: https://github.com/Pype-ai/agensight
- Open-source experimentation and observability studio for conversational AI agents
- Works with any agentic framework (LangGraph, AutoGen, etc.) and any modality (voice, image, text)
- Enables session-level tracing of agentic workflows with minimal code changes
- 17 stars, 3 forks; Python; MIT license; last commit June 16, 2025

### Pricing
- Pricing not publicly listed; custom enterprise contracts
- Model likely: per-call or per-seat subscription, scaled by call volume and EHR integration depth
- No free tier confirmed; no publicly stated per-unit price
- (Note: The Capterra reviews for "Pype" starting at $2,500 refer to a different, unrelated construction software company also named Pype)

### Languages & Voices
- 20+ languages supported (claimed on website; specific languages not fully enumerated publicly)
- Initial focus: Indian English accent
- Expanded to Hindi and Kannada via collaborations with Sarvam AI and Krutrim (claimed; sourced from arabfounders.net — not independently verified by Pype)
- No published voice count or speaker diversity metrics
- No Bhashini API integration confirmed; no AI4Bharat dataset attribution found

### Named Customers
The following names appear on pypeai.com as healthcare partners (verified via website fetch):
- Sparsh (hospital/clinic chain)
- MACS
- HCG Hospital (Dr. Vishal Rao, Head of Oncology, provided testimonial)
- Cloud9

Additional: "~15 hospitals in India" broadly cited; US clinic chain onboarding underway as of Nov 2025. No named US customers disclosed.

### Integrations / SDKs
- **EHR/EMR:** Epic, Cerner, Meditech, Zocdoc
- **Telephony:** Twilio, AWS Connect
- **Messaging:** WhatsApp
- **CRM:** HubSpot, Zoho CRM
- **Calendar:** Google Calendar, Calendly
- **Collaboration:** Microsoft Teams, Slack
- **LLM backends:** Azure OpenAI, AWS Bedrock, custom fine-tuned models (plug-in architecture)
- Total: 30+ tool integrations claimed

## 4. Technical Architecture
### Model approach
- Pype does not build or own a proprietary LLM or TTS model
- Uses a composable, provider-agnostic voice agent pipeline built on **Pipecat** (open-source Python framework for real-time voice AI)
- Supports plugging in Azure OpenAI, AWS Bedrock, or custom fine-tuned models as the LLM backbone
- Healthcare-specific fine-tuning applied on top of commodity LLMs using "medical-grade conversation datasets"
- Architecture confirmed by Ashish Tripathy's August 2025 session at DataHack Summit: "Building a Scalable Healthcare Voice AI Contact Center with Pipecat"

### Training data
- "Medical conversational datasets" (described broadly; no public dataset card)
- Fine-tuning for Indian English, Hindi, Kannada accents and clinical vocabulary
- Collaborations with Sarvam AI and Krutrim cited for regional language capabilities (claimed; not press-verified)
- No arXiv publications; no HuggingFace datasets released

### Latency profile
- Sub-second response latency claimed (self-reported)
- Whispey tracks the full VAD → STT → LLM → TTS pipeline breakdown per call
- No third-party TTFB or RTF benchmarks published

### Voice cloning
- No explicit voice cloning product documented
- "Human-like voice" claimed; voice customization likely via TTS provider selection (ElevenLabs, Cartesia, or Deepgram TTS integrations common in Pipecat ecosystem)
- No proprietary voice cloning capability confirmed

### Prosody / emotion control
- Dynamic voice personality switching demonstrated at DataHack Summit 2025: configuring separate TTS voices for "Front Desk" and "Supervisor" personas, switching based on sentiment analysis
- Interruption handling and latency management covered in technical session
- No published emotion control API

### Indic language strategy
- Indic language support described as expansion from Indian English base
- Hindi and Kannada added via third-party model collaborations (Sarvam AI, Krutrim)
- No AI4Bharat lineage or Bhashini API integration documented
- No IndicTTS or IndicConformer usage confirmed
- 20+ languages claimed on website — specific list not published
- Indic support appears to be through STT/TTS provider selection, not proprietary models

### Inference stack
- Pipecat framework for real-time voice pipeline orchestration
- LiveKit for WebRTC transport (confirmed by Whispey's explicit LiveKit compatibility)
- STT: provider-agnostic (Deepgram, Whisper-compatible services likely)
- LLM: Azure OpenAI, AWS Bedrock, or custom models
- TTS: provider-agnostic
- Supabase for real-time data and analytics backend (confirmed via Whispey tech stack)
- Deployment: VPC (self-hosted) or cloud; containerized (mentioned in DataHack Summit talk)

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| "Building a Scalable Healthcare Voice AI Contact Center with Pipecat" | Conference talk (DataHack Summit 2025) | Aug 2025 | https://www.analyticsvidhya.com/datahacksummit-2025/sessions/building-a-scalable-healthcare-voice-ai-contact-center-with-pipecat |
| Why We Invested in Pype AI | Investor blog | Nov 2025 | https://kalaari.com/why-we-invested-in-pype-ai/ |
| Show HN: Whispey – Open-source observability for LiveKit voice agents | HN post | ~Aug 2025 | https://news.ycombinator.com/item?id=44866675 |
| Open-Source Observability for LiveKit Voice Agents | LinkedIn post (Dhruv Mehra) | ~Aug 2025 | https://www.linkedin.com/posts/dhruv-mehra_opensource-livekit-voiceai-activity-7360710673388945411-0KBM |

No arXiv papers published. Company plans to publish clinical AI research on treatment adherence (announced Nov 2025; not yet published as of May 2026).

## 5. Open Source Footprint
### GitHub
Two separate organizations found:

**Org 1:** https://github.com/Pype-ai (commercial/product org)
| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| agensight | 17 | 3 | MIT | Jun 16, 2025 | Experimentation studio for conv. AI agents |
| agensight-example-langgraph-chatbot | 0 | 0 | — | Jun 4, 2025 | LangGraph chatbot example |
| agensight_mcpserver | 4 | 0 | — | May 14, 2025 | MCP server for Agensight |

**Org 2:** https://github.com/PYPE-AI-MAIN (open-source/community org)
| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| whispey | 65 | 20 | MIT | May 8, 2026 | Flagship OSS: voice AI observability |
| whispey-enterprise | 0 | 0 | — | Sep 12, 2025 | Enterprise version (closed-source) |
| whispey-examples | 3 | 0 | — | Sep 4, 2025 | LiveKit agent examples |
| agensight | 3 | 0 | — | May 14, 2025 | Mirror/fork of main org |
| agensight_mcpserver | 2 | 0 | — | May 14, 2025 | MCP server mirror |
| pypeprompts | 0 | 0 | — | Apr 23, 2025 | Prompt management utility |
| motherhood-multi-agent | 0 | 0 | — | Mar 2, 2026 | Multi-agent experiment |
| slack-agents | 0 | 0 | — | Jan 14, 2025 | Slack integration for agents |
| invoice-manager | 0 | 0 | — | Mar 19, 2025 | Utility tool |

**Total community signal:** Modest. Whispey (65 stars) is the strongest signal. No repo has broken 100 stars.

### Hugging Face
| Model | Downloads | Likes | License |
|-------|-----------|-------|---------|
| (none) | — | — | — |

Organization registered at https://huggingface.co/pype-ai with 0 public models, 0 datasets, 0 spaces. One team member listed: Adarsh Singh.

### Top contributors
- No public contributor list available on GitHub org pages. Whispey has an active contribution guide (CODE_OF_CONDUCT.md present). Community contributions encouraged but small.

## 6. Team
### Founders
**Dhruv Mehra — Co-founder & CEO**
- Former Meta Technical Principal; worked on products serving 100M+ daily users
- Previously: heymax.ai, WNS Global Services, Mu Sigma Inc.
- Education: Dr. B.R. Ambedkar NIT Jalandhar
- AI Tinkerers Bangalore presenter (September 2024 — at that point Pype was pitching as LLM observability/prompt monitoring, not yet the healthcare pivot)
- LinkedIn: https://www.linkedin.com/in/dhruv-mehra/

**Ashish Tripathy — Co-founder & CTO**
- 12+ years in Data, ML, AI
- Former: LinkedIn (ML for fraud detection), SAP (disinformation prevention, multi-agent framework design)
- Patents: User behavior profiling, large-scale duplicate-content detection on social media
- DataHack Summit 2025 speaker (August 2025)
- LinkedIn: https://in.linkedin.com/in/ashish-tripathy-70a30863

### Key technical hires
- Adarsh Singh (confirmed HuggingFace org member; role not specified)
- No other key technical hires publicly named

### Recent joiners (last 12mo)
- Not publicly available. Company headcount grew from ~8 (PitchBook) to ~13 (Tracxn) between early 2025 and Mar 2026, suggesting ~5 hires.

### Notable departures (last 12mo)
- Not publicly available

### Open roles signal
- No public job board or careers page identified from web search
- Likely hiring via LinkedIn and Indian startup platforms (AngelList, Wellfound)

## 7. Moat & Defensibility
- **Data moat:** Weak-to-moderate. Accumulating clinical call recordings and patient interaction data across 15+ Indian hospitals. Data annotated with clinical feedback via Whispey's in-call clinician feedback loop — proprietary dataset building mechanism is a genuine differentiator. However, dataset scale is small at current stage. No published dataset.
- **Model moat:** Weak. No proprietary foundation model. Relies on commodity LLMs (Azure OpenAI, AWS Bedrock) + Pipecat orchestration. Healthcare fine-tuning is claimed but not peer-reviewed. Edge: domain vocabulary, specialty-specific workflow training.
- **Distribution moat:** Moderate (India). 15+ hospital pilots creates reference customer network in Indian healthcare. Kalaari Capital network provides warm intros to Indian health systems. US entry underway but no named customers yet. No Bhashini, ONDC, or government tender exposure confirmed.
- **Brand / community moat:** Early. Whispey's HN Show HN post (Aug 2025) and DataHack Summit presence signal developer community visibility. Agensight has limited traction (17 stars). Not yet a category-defining brand.
- **Regulatory moat:** Weak. Claims HIPAA and SOC 2 compliance, which is table stakes for US market entry but provides credibility for Indian hospital procurement (where HIPAA is aspirational). No Indian government certifications (DISHA, MeitY) mentioned.
- **Replication cost (6mo, $10M competitor):** A well-funded competitor (e.g., US player like Assort Health or Syllable expanding to India) could replicate the core voice agent stack in ~3-4 months using Pipecat + commodity LLMs + Sarvam STT/TTS. The meaningful barriers are: (a) EMR integration work (3-6 months for Epic/Cerner/Meditech), (b) clinical workflow knowledge, (c) existing hospital relationships. A $10M competitor could close this gap in 6 months.
- **Moat strength: 2/5** — Early-stage Indian healthcare foothold with a clever open-source community strategy (Whispey), but no proprietary AI stack and limited scale; moat is primarily relationship-based at this point.

## 8. Risks & Problems
### Technical complaints
- No Reddit, HN, or GitHub issue complaints found (too early-stage and low public usage to generate complaint volume)
- HN Show HN post for Whispey (Aug 2025) at https://news.ycombinator.com/item?id=44866675 — content not retrievable (429 rate limit). Tone of reception unknown.
- Reliance on third-party LLM providers creates vendor dependency and latency/cost risk
- LiveKit dependency means Whispey is narrowly scoped (only works with LiveKit agents), which limits TAM for the OSS tool

### Pricing pain points
- No public pricing; enterprise sales cycle may be a barrier for smaller clinics
- Indian hospital chains have tight budgets; value-based pricing or per-call models may face pushback

### Safety / misuse
- Clinical AI safety is existential risk: misrouted urgent calls, missed escalations, or incorrect treatment instructions could cause patient harm
- 40+ Whispey evaluations address compliance/safety but are self-assessed
- HIPAA compliance in India is aspirational (India has no HIPAA equivalent); actual data governance regime unclear
- AI nurse framing (CTO's stated vision) may attract regulatory scrutiny in medical AI contexts

### Legal / regulatory
- Governing law: Delaware (per Terms of Service) — US legal framework despite India operations. Suggests US entity structure.
- Legal entity associated with "SINGULARITY CORP PRIVATE LIMITED" per Tracxn; registered at Jaipur address (409, Acacia Apartment, Siddharth Nagar H Block, Jagatpura, Jaipur, Rajasthan 302017) — conflicts with Bengaluru HQ claim. Could reflect founders' home address used for incorporation.
- CIN: Not publicly found (MCA search not performed directly)
- No litigation or IP disputes found

### Churn signals
- No churn data available; company is pre-revenue-scale
- Pilot-to-production conversion rate unknown
- US expansion announced but no US customers named 6 months after funding

## 9. Competitive Position
- **Direct competitors:**
  - *India-focused:* Sarvam AI (Sarvam SEWA for healthcare workflows), Gnani.ai (voice AI platform), Eka Care (patient engagement), Haptik (conversational AI — Reliance-backed)
  - *US-focused but expanding to India:* Syllable ($85.6M raised), Assort Health ($102M raised), Orbita ($16.3M raised), Infinitus Systems, Parakeet Health
  - *Global voice AI platforms:* Vapi, Bland AI, Retell AI, Twilio AI
  - Tracxn places Pype 8th of 26 active competitors by funding; Syllable and Assort Health are 10-80x better funded

- **Where it's winning:**
  - Indian hospital market: price sensitivity, local language support, EMR integration with Indian-used systems, rapid 2-week deployment
  - Developer mindshare: Whispey is the strongest OSS signal in clinical voice observability
  - Speed: <1 year from founding to 15 hospital deployments, funded by top-tier Indian VC

- **Where it's losing:**
  - Scale: Massively outgunned by US competitors on capital ($1.2M vs $85-102M)
  - Model ownership: No proprietary AI — relies on commodity stack
  - US market: No named US customers despite announced expansion
  - Enterprise features: US health systems require deep Epic/Cerner certification, not just API integration

## 10. News & Momentum (last 12 months)
| Date | Event | Source |
|------|-------|--------|
| Sep 2024 | Dhruv Mehra presents Pype (LLM monitoring tool) at AI Tinkerers Bangalore | LinkedIn [4] |
| ~Jul 2025 | Whispey open-sourced and posted to Hacker News ("Show HN") — 2 separate HN threads | HN [5][6] |
| Aug 2025 | Ashish Tripathy speaks at DataHack Summit 2025 on "Building a Scalable Healthcare Voice AI Contact Center with Pipecat" | Analytics Vidhya [7] |
| Sep 1, 2025 | Whispey v3.0.0 released with OpenTelemetry integration | GitHub [8] |
| Nov 18, 2025 | $1.2M pre-seed funding announced; led by Kalaari Capital with Wyser Capital and Tenity | Entrackr, MediaBrief, IndianStartupNews [1][2][3] |
| Nov 2025 | Kalaari Capital publishes investment thesis blog post for Pype AI | Kalaari [9] |
| Mar 2026 | Headcount reaches ~13 per Tracxn tracking | Tracxn [10] |
| May 2026 | Whispey last commit (active maintenance) | GitHub [8] |

**Velocity verdict:** Moderate and accelerating. The company pivoted cleanly from LLM observability to healthcare voice AI in 2024, shipped a fundable product, raised institutional capital within ~12 months of founding, and has deployed across 15 hospitals with self-reported strong metrics. OSS community building (Whispey) provides developer credibility. However, no US customers yet and no follow-on funding announced — the mid-2026 hospital expansion targets will be a key validation milestone.

## 11. Bull Case / Bear Case
**Bull:**
India's healthcare system is severely understaffed, with hospital admin costs high and IVR systems universally hated. Pype's 2-week deployment promise, HIPAA/SOC2 posture, and EMR integrations lower the sales barrier significantly. Kalaari Capital's healthcare network could accelerate India growth. The Whispey open-source strategy creates a developer-to-enterprise funnel — the same playbook that worked for Grafana, Langfuse, etc. If the company captures even 1% of India's 50,000+ private hospitals, that is a large market at meaningful ARPU. The US market opportunity is 10-50x larger and data from Indian deployments de-risks the model.

**Bear:**
The core product is commodity-stackable: Pipecat + Azure OpenAI + Deepgram + Twilio is something any well-funded team can replicate in 3 months. The $1.2M pre-seed will not fund serious US expansion (sales cycles alone can cost $500K+/year). Assort Health ($102M) and Syllable ($85M) have insurmountable capital advantages in the US and are beginning India expansion. If Sarvam AI or Haptik builds a healthcare vertical with native Indic model advantage, Pype's language differentiation evaporates. The "15 hospitals" footprint is impressive for stage but tiny in a market of 50,000+ facilities — if customer acquisition speed does not accelerate post-funding, the company could stall at pilot scale.

## 12. What I Couldn't Find
- MCA CIN number (Ministry of Corporate Affairs registration for Singularity Corp Private Limited)
- INR equivalent of $1.2M stated explicitly in any source
- Named US customers (despite announcement of US expansion Nov 2025)
- Specific list of all 20+ supported languages
- Pricing tiers or per-call rates
- Advisor or board member names beyond the two founders
- Any G2 or Capterra reviews for Pype AI's healthcare product (not to be confused with the construction software "Pype" on Capterra)
- Churn rate or NPS data
- Published arXiv or peer-reviewed research
- Actual headcount breakdown (engineering vs. sales)
- Any regulatory certifications from Indian government bodies (MeitY, NHA, ABDM)
- Bhashini API integration or AI4Bharat collaboration (absence likely — not confirmed absent)
- Details of HN reception for Whispey (page rate-limited during research)
- Post-money valuation from pre-seed round

## Sources
1. https://entrackr.com/snippets/pype-ai-raises-12-mn-in-pre-seed-round-led-by-kalaari-capital-10783582
2. https://mediabrief.com/pype-ai-raises-1-2-million-pre-seed-funding-to-build-ai-front-desk-for-hospitals-and-clinics/
3. https://indianstartupnews.com/funding/pype-ai-an-indian-startup-building-ai-voice-agents-for-hospitals-raises-12-million-in-funding-10784409
4. https://www.linkedin.com/posts/dhruv-mehra_what-a-friday-at-ai-tinkerers-presenting-activity-7241338215389880320-sUgk
5. https://news.ycombinator.com/item?id=44866675
6. https://news.ycombinator.com/item?id=44873366
7. https://www.analyticsvidhya.com/datahacksummit-2025/sessions/building-a-scalable-healthcare-voice-ai-contact-center-with-pipecat
8. https://github.com/PYPE-AI-MAIN/whispey
9. https://kalaari.com/why-we-invested-in-pype-ai/
10. https://tracxn.com/d/companies/pype/__dzlS2H3tljf30HaASBM64pLgR0V5TM3LJWYnfXVYA68
11. https://pypeai.com
12. https://github.com/Pype-ai
13. https://github.com/PYPE-AI-MAIN
14. https://huggingface.co/pype-ai
15. https://arabfounders.net/en/pype-ai-raises-1-2m-pre-seed-us-expansion/
16. https://www.entrepreneur.com/en-in/news-and-trends/pype-ai-secures-usd-12-mn-in-pre-seed-funding/499701
17. https://www.analyticsvidhya.com/datahacksummit-2025/speakers/ashish-tripathy
18. https://pitchbook.com/profiles/company/756744-67
19. https://www.marcamoney.com/pype-ai-raises-1-2-million-in-pre-seed-funding-led-by-kalaari-capital/
20. https://www.siliconindia.com/startup/startup-funding/pype-ai-raises-12-million-to-expand-ai-front-desk-for-hospitals-nwid-52149.html
21. https://www.digitalhealthnews.com/bengaluru-based-pype-ai-secures-1-2-mn-pre-seed-round-led-by-kalaari-capital
22. https://yourstory.com/2025/11/ai-focused-wyser-capital-marks-close-maiden-fund
23. https://startupnews.fyi/2025/11/18/pype-ai-raises-1-2-mn-in-pre-seed-round-led-by-kalaari-capital/
24. https://www.thesaasnews.com/news/pype-ai-raises-1-2-million-in-funding
25. https://in.linkedin.com/in/ashish-tripathy-70a30863
26. https://www.linkedin.com/in/dhruv-mehra/
27. https://pypeai.com/terms-of-service
28. https://www.zoominfo.com/c/pype-ai/5000218667
