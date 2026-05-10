# Ringg AI

**Website:** https://ringg.ai  •  **HQ:** Bengaluru (Koramangala), Karnataka, India  •  **Founded:** October 2023  •  **Stage:** Series A
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): A no-code, multilingual voice-agent orchestration platform that lets Indian enterprises deploy AI-powered inbound and outbound calling agents in 20+ languages — with all the plumbing (STT, LLM, TTS, telephony) bundled into one stack — at $0.06–$0.10/min.
- Total funding to date: ~$6.5M USD (seed $1M + Series A $5.5M; pre-Series A round not confirmed separately)
- Last round: $5.5M Series A, January 2026, led by Arkam Ventures
- Headcount: ~18 employees (PitchBook, as of early 2026); 5 listed as HuggingFace org members
- Revenue / ARR: Not publicly disclosed. Traction proxy: 1.5M customer conversations/month (claimed, January 2026); 24,576 assistants deployed in 2025 (self-reported).

## 2. Funding History
| Date | Round | Amount (USD) | Amount (INR) | Lead | Other Investors | Source |
|------|-------|-------------|-------------|------|-----------------|--------|
| May 29, 2025 | Seed | $1M | ~₹8.3 Cr | Capital 2B | Not named (angel round; 22 investors total per Tracxn) | YourStory, TechScoopIndia |
| January 2026 (announced Jan 23, 2026) | Series A | $5.5M | ~₹48 Cr | Arkam Ventures | Groww Founder Fund, Kunal Shah (CRED founder), White Venture Capital, Capital 2B (existing) | Inc42, Entrackr, BW Disrupt, company blog |

**Notes:**
- Tracxn reports 22 total investors (6 institutional including Mehta Group, 16 angel). The institutional investors beyond Arkam, Capital 2B, and White Venture Capital are not all individually named in public sources as of this writing.
- Post-money valuation: Not publicly disclosed.
- Pre-Series A round: Some sources list a third unnamed round; not independently confirmed — treat the $6.5M total as approximate.

## 3. Product & Customers

### Products
Ringg AI (brand name) is built by legal entity **Stoic AI Pvt Ltd**. There is a second brand, **Desi Vocal**, under the same entity — its product focus is not publicly detailed in available sources.

Core platform: **Voice Agent Orchestration** — a single-stack (Brain/LLM + Ears/STT + Voice/TTS + Phone Line/Telephony) that processes listening, thinking, and speaking in one unified "Flash Engine" stream rather than daisy-chaining external APIs.

Key capabilities:
- **No-code Visual Agent Builder**: drag-and-drop workflow designer for creating conversation flows without code
- **Outbound Auto-Dialer**: bulk campaigns via CSV upload; up to 1,000 calls/minute, 10,000+ concurrent calls
- **Inbound Call Handling**: IVR replacement, transfer with context
- **Web Call Integration**: embeddable JS widget for voice/chat in browsers
- **REST API + SDKs**: JavaScript, Python, PHP, Go, Java; base URL `https://prod-api.ringg.ai/ca/api/v0`; auth via `X-API-KEY`
- **Context Graphs**: unified framework supporting both voice and text agents from a single graph structure
- **RAG Knowledge Base**: document-grounded responses during live calls (files up to 25 MB)
- **Function Calling**: mid-call API triggers for CRM updates, SMS, email, appointment booking
- **Warm Transfer**: full transcript passed to human agent
- **Campaign Analytics**: call dispositions, transcripts, recordings, memory tracking
- **Webhooks**: `call_started`, `call_completed`, `all_processing_completed`
- **Proprietary Models** (in-house, launched Nov–Apr 2025–2026):
  - *Ringg Parrot STT V1*: Hindi-English code-mixed ASR; built on NVIDIA NeMo Parakeet architecture; 15.00% Median WER (claimed best-in-class for Hindi ASR vs. IndicWav2Vec at 19.35%); 0.013 RTF on T4 GPU (~77x faster than real-time); trained on 40% telephony, 30% rural community, 30% mixed data
  - *Ringg Squirrel TTS V1.0*: in-house TTS with 38 Indian voices; featured on HuggingFace Spaces of the Week; supports Hindi and English; voice cloning and domain fine-tuning options mentioned (details sparse)
  - *Transcript-Analytics-SLM 0.5B & 1.5B*: small language models for post-call transcript analytics (fine-tuned on conversation data)
  - *Transcript-Analytics-Qwen3.5-0.8B & 2B*: fine-tuned Qwen-based image-text-to-text models for transcript analytics
- **On-premises deployment**: planned/in-progress for compliance-sensitive enterprises (announced as a use of Series A capital)

Use-case verticals: Lead Generation, Loan Collection, Last-Mile Delivery, Appointment Booking, Recruitment/Hiring, Customer Support.

### Pricing
*(Verified from ringg.ai/pricing, May 2026)*

| Plan | Price/Min | Concurrent Calls (included) | Bulk Call Limit | Custom Number |
|------|-----------|----------------------------|-----------------|---------------|
| Flexible Usage | $0.10/connected call minute | 2 free; up to 50 (extra $10/channel/mo) | 100 calls | $6/month |
| Enterprise | $0.06/connected call minute | 2 free; up to 100 | 10,000 calls | $6/month |

- Analytics dashboard: free on all plans
- All-inclusive model: STT + LLM + TTS + orchestration + RAG + function calling + auto-dialer + no-code builder bundled; telephony add-on separate ($6/mo per number)
- Ringg claims competitors' modular stack costs $0.15–$0.30/min when combining separate API fees

### Languages & Voices
- **Claimed total**: 20+ languages (homepage), 18+ (Series A announcement)
- **Indian languages (verified listed)**: Hindi, Hinglish, Tamil, Telugu, Marathi, Malayalam, Kannada, Bengali, Gujarati (9 languages)
- **International**: Indian English, Gulf Arabic (UAE/Saudi optimized), Modern Standard Arabic, Spanish, French, German, Bahasa (Indonesian/Malay)
- **Regional accents**: 16+ claimed
- **Code-switching**: Hinglish, Marathinglish, Arabic-English (GCC) supported without context loss
- **Voices**: Squirrel TTS ships 38 Indian voices; broader voice library not enumerated publicly
- **Voice cloning**: mentioned as a feature; specs (audio length required, turnaround) not publicly documented

### Named Customers
All customer claims sourced from Ringg AI's own website and press materials unless noted:

| Customer | Sector | Use Case | Claimed Metric | Source |
|----------|--------|----------|----------------|--------|
| CRED | Fintech | EMI recovery, collections | Not specified | Inc42, Entrackr |
| PharmEasy | Healthcare / Pharma | Order confirmations, prescription follow-ups, delivery coordination | Not specified | Entrackr |
| Shiprocket | Logistics | Delivery updates, coordination | Not specified | Entrackr |
| Flipkart | E-commerce | Not specified | Not specified | Entrackr |
| Shell | Energy | Not specified | Not specified | Entrackr |
| Practo | Healthcare | Appointment booking | 30,000+ appts/month, 85% first-call resolution, 70% cost reduction (self-reported, no independent case study found) | Ringg website |
| Roombae | Real estate | Inbound lead qualification | 80% boost in lead engagement (self-reported) | Ringg website |
| PharmaGrowth | Healthcare | Outbound confirmations | 43% increase in call confirmations in 2 weeks (self-reported) | Ringg website |
| Tabby | BNPL / Fintech (UAE/SA) | Onboarding, payment reminders | Not specified | Ringg Series A blog |
| Noon | E-commerce (MENA) | Delivery coordination, returns | Not specified | Ringg Series A blog |

**Caution**: CRED, Flipkart, PharmEasy, Shiprocket, Shell mentioned only in investor announcement press coverage — no independent case study links or customer confirmations found for those. Practo, Roombae, PharmaGrowth metrics are self-reported on Ringg's website only.

Geography: 20+ enterprise customers across India, US, Saudi Arabia (claimed as of January 2026).

### Integrations / SDKs
**Telephony**: Exotel (India, DND compliance), Twilio (100+ countries), Plivo, custom SIP endpoints
**CRM**: Salesforce Agentforce, HubSpot, Zoho CRM, LeadSquared, Freshworks, Zendesk, ServiceNow
**Automation**: Zapier (5,000+ app connections), Make.com
**E-commerce**: Shopify
**Scheduling**: Calendly, Google Calendar
**Storage**: Google Drive
**Other**: Google Sheets, Typeform, QuickBooks, Sendbird Calls, WhatsApp (sync)
**SDKs**: JavaScript, Python, PHP, Go, Java (REST API)

## 4. Technical Architecture

### Model approach
Integrated "single-pass" pipeline rather than waterfall STT → LLM → TTS. Ringg brands this the **Flash Engine**. All three components process in a unified stream. Proprietary in-house models (Parrot STT, Squirrel TTS) replace third-party API calls for core speech processing. LLM layer not publicly named — likely using a hosted or fine-tuned model; Series A stated goal is to further reduce third-party API dependency and build proprietary models.

Transcript analytics handled by fine-tuned small language models (Qwen-based 0.5B–2B parameter range), suggesting on-device or low-cost inference for post-call processing.

### Training data
- Parrot STT: multi-domain Hindi; 40% telephony recordings, 30% rural community voices, 30% mixed (HuggingFace Shrutilipi dataset, narration audio, TTS-generated content)
- ASR Benchmarking Dataset: published on HuggingFace; 10K samples; 6 subsets (CommonVoice, Fleurs, IndicTTS, Kathbath, Kathbath-Noisy, MUCS); benchmarks Ringg vs. ElevenLabs, Deepgram, Sarvam on Hindi
- Squirrel TTS and SLM training data: not publicly described

### Latency profile
- Homepage claims: <330ms global latency
- Other self-reported: sub-400ms
- Parrot STT inference: 72.77ms for 5.58s audio on T4 GPU (0.013 RTF, ~77x faster than real-time)
- Comparison framing: competitors using chained APIs reported at 800ms–1.5s
- TTFB and streaming specifics: not published

### Voice cloning
- Offered as a feature (mentioned in documentation/blogs)
- 38 Indian voices in Squirrel TTS V1.0
- Domain fine-tuning mentioned
- Technical specs (minimum audio, cloning time, supported languages for cloning): not publicly documented

### Prosody / emotion control
- Platform handles barge-in (user interruption mid-sentence) and turn detection (end-of-speech vs. pause)
- Emotion/prosody control beyond barge-in not specifically documented in public sources

### Indic language strategy
- Proprietary in-house STT (Parrot) and TTS (Squirrel) tuned specifically for Hindi and code-mixed Hindi-English
- Benchmarking dataset released publicly to establish performance claims vs. Sarvam, Deepgram, ElevenLabs
- Dial-up: code-switching (Hinglish, Marathinglish) without context loss
- Rural accent coverage: 30% of STT training data from rural community voices
- Devanagari script support for CRM data capture
- No publicly disclosed partnership with Bhashini or AI4Bharat as of this writing

### Inference stack
- Cloud-based (primary)
- On-premises: announced as in-development/planned for compliance-sensitive BFSI customers
- GPU infrastructure: Series A capital earmarked for GPU cluster build-out
- NVIDIA NeMo used for ASR model training
- HuggingFace for model/dataset hosting and community distribution

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Ringg Parrot STT V1 (HF Space) | Model demo + benchmark | ~Apr 2026 | https://huggingface.co/spaces/RinggAI/STT |
| Ringg Squirrel TTS V1.0 (HF Space) | Model demo | Nov 21, 2025 | https://huggingface.co/spaces/RinggAI/Ringg-TTS-v1.0 |
| ASR-Benchmarking-Dataset | Dataset | ~Apr 2026 | https://huggingface.co/datasets/RinggAI/ASR-Benchmarking-Dataset |
| Ringg AI Series A Announcement | Company blog | Jan 23, 2026 | https://www.ringg.ai/blogs/ringg-ai-announcing-our-5-5-millon-usd-series-a |
| Best Voice AI Agents for Indian Languages in 2026 | SEO blog | 2026 | https://www.ringg.ai/blogs/best-voice-ai-agents-for-indian-languages |
| Best AI Calling Agents 2026 | SEO blog | 2026 | https://www.ringg.ai/blogs/best-ai-calling-agents |

No arXiv papers from Ringg AI found. No conference talks found. Engineering blog not present beyond company announcements.

## 5. Open Source Footprint

### GitHub
No public GitHub org or repositories found for Ringg AI / Stoic AI as of May 2026. Searches returned no results. The codebase appears entirely proprietary / closed-source.

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| (None found) | — | — | — | — | No public repos verified |

### Hugging Face
Organization: [huggingface.co/RinggAI](https://huggingface.co/RinggAI) — **verified as active**

| Asset | Type | Downloads / Likes | License | Last Updated |
|-------|------|-------------------|---------|-------------|
| Ringg Parrot STT V1 (Space) | ASR demo | — | — | ~Apr 2026 |
| Ringg Squirrel TTS V1.0 (Space) | TTS demo | 80 likes | — | Nov 21, 2025 |
| Ringg-Squirrel-Free-API | API | 8 likes | — | Nov 29, 2025 |
| Transcript-Analytics-SLM0.5b | Text Gen | 12 likes | — | Nov 27, 2025 |
| Transcript-Analytics-SLM1.5b | Text Gen | 16 likes, 5 downloads | — | Nov 27, 2025 |
| Transcript-Analytics-Qwen3.5-0.8B | Image-Text | 6 likes | — | Mar 17, 2026 |
| Transcript-Analytics-Qwen3.5-2B | Image-Text | 14 likes, 2 downloads | — | Mar 17, 2026 |
| ASR-Benchmarking-Dataset | Dataset | 435 downloads, 1 citation | — | ~Apr 2026 |

HuggingFace Squirrel TTS Space was **featured as Space of the Week** — a meaningful community signal for a startup at this stage.

### Top contributors
HF org shows 5 team members. Individual contributor handles not listed publicly. One LinkedIn profile found: "Harsh ." listed as working at Ringg AI with HF presence.

## 6. Team

### Founders
| Name | Role | Prior Experience |
|------|------|-----------------|
| Siddharth Shankar Tripathi | CEO & Co-founder | Ex-Groww (fintech unicorn), ex-Flipkart; BITS Pilani alumnus |
| Utkarsh Shukla | Co-founder & Head of AI | Ex-Blinkit (quick commerce), ex-Atlan (data catalog) |
| Kali Charan Vemuru (Kali CV) | Co-founder & Head of Engineering | Ex-Flipkart |

Board of directors per MCA filing: Siddharth Shankar Tripathi and Anuj Bhagat (Anuj Bhagat's role/background not identified in available sources).

### Key technical hires
- "Harsh ." — ML/AI role (LinkedIn, HF contributor) — full name not public
- Machine Learning Engineer role open as of May 2026 (Bengaluru, hybrid)
- 5 listed HuggingFace org members — identities not all public

### Recent joiners (last 12 months)
Not publicly available; LinkedIn headcount data paywalled. Company grew from founding team to ~18 employees between Oct 2023 and early 2026.

### Notable departures (last 12 months)
Not publicly available.

### Open roles signal (as of May 2026, from ringg.ai/careers)
- Machine Learning Engineer (Bengaluru, hybrid)
- Founders Office (Bengaluru, on-site)
- Head of Partnerships (Bengaluru, on-site)
- Head of Marketing (Bengaluru, hybrid)
- Senior Product Manager (Bengaluru, on-site)

Signal: heavy hiring in GTM (Partnerships, Marketing) and product after Series A close. US GTM Motion and Digital Marketing roles also listed on Wellfound (earlier signal).

## 7. Moat & Defensibility

- **Data moat**: Moderate. 1.5M conversations/month across 10+ Indian languages in telephony-grade audio is non-trivial training data, especially for Tier 2/3 accents and code-mixed speech. Parrot STT's 40% telephony-data training mix suggests proprietary data collection. However, this data pool is still small compared to Sarvam AI or Bhashini-backed players. Score: 2.5/5.

- **Model moat**: Nascent but real. Parrot STT (best-in-class Hindi WER per their own benchmark) and Squirrel TTS (38 Indian voices) are owned IP rather than API wrappers. Transcript-Analytics SLMs show vertical domain fine-tuning. Series A explicitly funds proprietary model R&D. Dependency on third-party LLM for reasoning layer is a gap. Score: 2.5/5.

- **Distribution moat**: Early-stage. 20+ enterprise customers across India, MENA, and nascent US presence. Groww Founder Fund and Kunal Shah (CRED) as investors provide warm introductions into fintech distribution. Salesforce Agentforce integration opens enterprise channel. Exotel partnership provides India-telephony DND-compliant reach. No telco white-label deal, no Bhashini/govt contract confirmed. Score: 2/5.

- **Brand / community moat**: Weak but growing. HuggingFace Squirrel TTS was Space of the Week; ASR benchmarking dataset has 435 downloads and 1 citation — small but shows researcher engagement. Active SEO content strategy. No developer community (no GitHub, no Discord found). Score: 1.5/5.

- **Regulatory moat**: None identified. No Bhashini empanelment, no ONDC integration, no government tender, no DPDP Act compliance certification mentioned. The planned on-prem deployment capability could become a moat for BFSI data-residency compliance once delivered. Score: 1/5.

- **Replication cost (6-month, $10M competitor)**: A well-funded team could replicate Ringg's current feature set (no-code builder, multi-API orchestration layer, CRM integrations) in 6 months for well under $5M by wrapping Sarvam STT, an open LLM, and a commercial TTS. The harder-to-replicate element is the proprietary Parrot/Squirrel model stack and the telephony-domain training data — but even that is achievable with sufficient capital. True barriers are customer relationships and fine-tuned production reliability.

- **Moat strength: 2/5** — Ringg has genuine technical differentiation in Indic speech models and a tightly integrated voice stack, but is early in customer lock-in, lacks distribution at scale, and faces well-funded Indian (Sarvam, Gnani.ai) and global (Vapi, Retell) competitors; moat is still being built.

## 8. Risks & Problems

### Technical complaints
- G2 reviews (5 reviews, 4.8 stars — very small sample): struggles with interruptions and complex multi-step conversation branching; complex call logic hits a ceiling in the no-code builder
- Single-channel: voice-only; no SMS, email, WhatsApp, or chat unification — users need separate tools for follow-ups
- Limited orchestration for multi-agent workflows vs. enterprise competitors (Nurix, Cognigy)
- Fewer than 400+ CRM/ERP integrations that enterprise players like Nurix offer

### Pricing pain points
- $0.10/min Flexible plan vs. $0.06/min Enterprise — significant per-minute gap creates friction for mid-market customers not yet at enterprise volume
- Telephony fees separate: $6/month per number + $10/channel/month for concurrency adds up at scale
- No free trial tier visible in public pricing

### Safety / misuse
- Voice cloning for non-consensual impersonation is a sector-wide risk; Ringg offers voice cloning as a feature with no public documentation of consent verification or misuse guardrails
- India has no single federal voice-cloning law (as of May 2026), but regulatory exposure is growing (DPDP Act, telecom regulations)
- Robocalling regulations: TRAI DND rules apply; Exotel integration provides some compliance coverage but large-scale outbound calling at 1,000 calls/minute warrants scrutiny
- No published acceptable-use policy or safety framework found

### Legal / regulatory
- Legal entity Stoic AI Pvt Ltd (CIN: U62090KA2023PTC180343); GST active (29ABLCS9966Q1ZT, Karnataka)
- No litigation found in public sources
- Data residency: BFSI customers in India will face RBI data localization requirements; on-prem deployment (planned) directly addresses this
- International: Middle East (UAE/Saudi) operations involve cross-border data transfer risks under PDPL (Saudi) and UAE PDPL

### Churn signals
- No public churn data
- Only 5 G2 reviews in ~18 months of operation — suggests limited SMB self-serve penetration; growth is enterprise/sales-led
- Tabbly.io published a comparison recommending Tabbly over Ringg AI — indicates competitive pressure from newer entrants

## 9. Competitive Position

**Direct competitors:**

| Company | HQ | Positioning | Est. Scale |
|---------|-----|-------------|------------|
| Sarvam AI | Bengaluru | Full-stack Indian language AI; Samvaad voice agents; Bhashini/govt exposure | Series B, ~$70M raised |
| Gnani.ai | Bengaluru | Voice AI for BFSI/contact centers; established India enterprise | Series B |
| Nurix AI | India | Enterprise voice+text omnichannel; 400+ integrations; full-service | Funded |
| Vapi | USA | API-first, 300M+ calls, developer community, global | Series A, ~$20M |
| Retell AI | USA | Voice-first, 600ms latency, strong developer tooling | Funded |
| Synthflow AI | Germany | No-code, 65M+ calls | Funded |
| Verloop.io | Bengaluru | Inbound-focused conversational AI | Series B |
| SquadStack | India | Human-in-the-loop hybrid calling | Series B |
| PolyAI | UK | Enterprise omnichannel, hospitality/retail focus | Series C |

**Where Ringg AI is winning:**
- India-first: 10 Indian languages, rural accent coverage, Hinglish code-switching — better than global players (Vapi, Retell) out-of-the-box
- Price: $0.06–$0.10/min bundled is competitive against modular stacks costing $0.15–$0.30/min
- Self-serve / no-code speed of deployment vs. full-service Nurix or Gnani.ai
- Middle East early mover: Arabic-English code-switching, GCC customer references (Tabby, Noon cited)
- Integrated proprietary speech models (Parrot STT beats IndicWav2Vec on Hindi WER)

**Where Ringg AI is losing (or lagging):**
- Omnichannel: voice-only vs. Nurix, PolyAI, Cognigy (voice + chat + email + social)
- Enterprise integrations: 400+ for Nurix vs. ~15–20 named for Ringg
- Developer ecosystem: no public GitHub, no SDK docs as rich as Vapi or Retell
- Governance / audit trails: no enterprise compliance certifications mentioned
- Government / Bhashini distribution: Sarvam AI has deeper govt/Bhashini ties
- Scale: 1.5M conversations/month vs. Vapi (300M+ calls cumulative), Synthflow (65M+ calls)

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| May 29, 2025 | $1M seed round from Capital 2B announced | YourStory, TechScoopIndia |
| Nov 21, 2025 | Ringg Squirrel TTS V1.0 launched on HuggingFace; featured as Space of the Week | HuggingFace |
| Nov 27–29, 2025 | Transcript-Analytics SLM 0.5B and 1.5B models + Squirrel Free API published on HuggingFace | HuggingFace |
| Jan 23, 2026 | $5.5M Series A announced (led by Arkam Ventures); coverage in Inc42, Entrackr, BW Disrupt, YourStory, Entrepreneur India | Multiple |
| Mar 17, 2026 | Transcript-Analytics-Qwen3.5-0.8B and 2B models published on HuggingFace | HuggingFace |
| ~Apr 2026 | Ringg Parrot STT V1 launched on HuggingFace with Hindi ASR benchmarking dataset (435 downloads) | HuggingFace |
| May 2026 (ongoing) | Active careers hiring: Head of Partnerships, Head of Marketing, Senior PM, ML Engineer | ringg.ai/careers |

**Velocity verdict:** High. Two funding rounds within 8 months (seed May 2025, Series A Jan 2026), three proprietary model launches (Squirrel TTS, Parrot STT, Transcript-Analytics SLMs), and active enterprise hiring all point to strong forward momentum. The Series A at $5.5M from Arkam Ventures — a credible India-focused fund — with Kunal Shah and Groww Founder Fund participation validates product-market fit signals. Risk is that the company is still very small (~18 people) for the scale of ambitions (100M conversations/month by 2027).

## 11. Bull Case / Bear Case

**Bull:**
India's enterprise telephony market is enormous (~$3B+ call-center industry), under-automated, and deeply multilingual — exactly Ringg's wedge. The company owns the full voice stack (STT + LLM + TTS + telephony) and is building proprietary Indic-optimized speech models that outperform open-source alternatives on Hindi WER. Investor quality is high (Arkam, Kunal Shah, Groww Founder Fund) and gives warm intros into BFSI and fintech. If they can close 2–3 tier-1 BFSI or telco distribution deals and hit 10M conversations/month, unit economics at $0.06–$0.10/min are extremely attractive.

**Bear:**
Sarvam AI is better capitalized (~$70M+ raised), has deeper Indic language breadth (22 scheduled languages vs. Ringg's ~9 Indian languages), and has Bhashini/government distribution that Ringg lacks. Global players Vapi and Retell are rapidly adding Indic language support and have far larger developer ecosystems. Ringg's 18-person team at ~1.5M conversations/month has a very long road to 100M/month — and at $0.08/min average, 100M minutes/month = ~$8M MRR, which requires enterprise deals that take 6–18 months to close. Omnichannel is the market direction; voice-only is a strategic risk.

## 12. What I Couldn't Find
- Revenue / ARR figures (not disclosed)
- Post-money valuation for either round
- Full angel investor list (22 total per Tracxn; only a few named)
- Specific Bhashini, ONDC, or government tender involvement — none found
- Anuj Bhagat (MCA board member) — role and background not identified
- Named advisors or board observers beyond investors
- GitHub org or any public code repositories
- Detailed voice cloning specifications (minimum audio duration, turnaround, language coverage)
- Squirrel TTS architecture details (base model, training data)
- LLM provider used in the Brain layer (proprietary vs. GPT-4/Claude/etc.)
- Desi Vocal product details (sister brand under Stoic AI Pvt Ltd)
- Independent verification of Practo, CRED, Flipkart customer claims
- ARR or revenue data for any period
- Headcount breakdown by function (engineering vs. GTM vs. ops)
- Headcount 6 months ago (for delta calculation) — only current ~18 estimate available

## Sources
1. https://www.ringg.ai/ (homepage, verified)
2. https://www.ringg.ai/pricing (pricing page, verified)
3. https://www.ringg.ai/careers (careers page, verified)
4. https://www.ringg.ai/blogs/ringg-ai-announcing-our-5-5-millon-usd-series-a (Series A announcement, verified)
5. https://www.ringg.ai/blogs/best-voice-ai-agents-for-indian-languages (competitive blog, verified)
6. https://www.ringg.ai/llms.txt (technical LLM context file, verified)
7. https://docs.ringg.ai/ (API documentation, verified)
8. https://huggingface.co/RinggAI (HuggingFace org, verified)
9. https://huggingface.co/spaces/RinggAI/Ringg-TTS-v1.0 (Squirrel TTS Space, verified)
10. https://huggingface.co/datasets/RinggAI/ASR-Benchmarking-Dataset (ASR benchmark dataset, verified)
11. https://inc42.com/buzz/voice-ai-startup-ringg-bags-5-5-mn-from-arkam-ventures/ (Inc42, Series A coverage)
12. https://entrackr.com/snippets/voice-ai-startup-ringg-ai-raises-55-mn-in-series-a-funding-led-by-arkam-ventures-11017504 (Entrackr, Series A)
13. https://www.bwdisrupt.com/article/ringg-ai-raises-5-5-mn-series-a-powers-1-5-mn-monthly-conversations-multilingual-agents-590045 (BW Disrupt, Series A)
14. https://www.entrepreneurindia.com/blog/en/news/voice-ai-startup-ringg-ai-secures-usd-55-mn-series-a-funding-led-by-arkam-ventures.58897 (Entrepreneur India, Series A)
15. https://startupnews.fyi/2026/01/23/voice-ai-startup-ringg-ai-raises-5-5-million-in-round-led-by-arkam-ventures/ (StartupNews.fyi, Series A)
16. https://yourstory.com/2025/05/conversational-ai-startup-ringg-ai-raises-1m-capital-2b (YourStory, seed round) [403 on fetch; data sourced from search snippet]
17. https://techscoopindia.com/ringg-ai-secures-1m-funding-from-capital-2b/ (TechScoopIndia, seed round, verified)
18. https://tracxn.com/d/companies/ringgai/__IBo2jWWzYKzVE2ps0kldh6y7cZzzKEIKjOIysuWvMZs (Tracxn company profile)
19. https://tracxn.com/d/companies/ringgai/__IBo2jWWzYKzVE2ps0kldh6y7cZzzKEIKjOIysuWvMZs/funding-and-investors (Tracxn funding history)
20. https://tracxn.com/d/legal-entities/india/stoic-ai-private-limited/__MQr4_7Q7uGoTiu36Jj2VcXTppzsYaowM0ujRcBIupLI (Stoic AI legal entity, Tracxn)
21. https://www.thecompanycheck.com/company/stoic-ai-private-limited/U62090KA2023PTC180343 (MCA registration data, verified via search)
22. https://pitchbook.com/profiles/company/596492-92 (PitchBook profile, headcount ~18)
23. https://wellfound.com/company/ringg-ai (Wellfound/AngelList profile)
24. https://wellfound.com/company/ringg-ai/funding (Wellfound funding page)
25. https://in.linkedin.com/company/ringg (LinkedIn company page)
26. https://in.linkedin.com/in/sidsst (Siddharth Shankar Tripathi LinkedIn)
27. https://in.linkedin.com/in/utkarsh-shukla-8b834b112 (Utkarsh Shukla LinkedIn)
28. https://www.g2.com/products/ringg-ai/reviews (G2 reviews, 5 reviews, 4.8 stars)
29. https://www.nurix.ai/blogs/ringg-ai-alternatives (Nurix competitive analysis, verified)
30. https://www.tabbly.io/blogs/ringg-ai-review-tabbly-alternative (Tabbly competitive review)
31. https://theaiworld.org/news/ringg-raises-55m-for-multilingual-voice-ai (The AI World, Series A)
32. https://www.siliconindia.com/startup/startup-funding/ringg-ai-raises-55-million-to-expand-multilingual-voice-ai-platform-nwid-53197.html (SiliconIndia, Series A)
33. https://community.startuptalky.com/discussions/post/we-re-thrilled-to-announce-th-vtNgFkpJA4z98ye (StartupTalky, seed announcement)
34. https://www.instagram.com/p/DTxm7RBjTtW/ (Ringg AI Instagram, founder mention)
35. https://www.ringg.ai/industries/logistics (Ringg logistics industry page)
36. https://www.ringg.ai/industries/healthcare (Ringg healthcare industry page)
37. https://www.ringg.ai/use-cases/hiring (Ringg hiring use case page)
