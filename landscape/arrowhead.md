# Arrowhead

**Website:** https://arrowhead.ai  •  **HQ:** Bengaluru (Indiranagar), Karnataka, India  •  **Founded:** 2022 (incorporated Apr 20, 2023)  •  **Stage:** Seed
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): A verticalized voice-AI platform that deploys human-sounding, compliance-aware sales agents for India's BFSI sector — handling up to 20-minute calls in 10+ languages without customers detecting automation.
- Total funding to date: ~$3.32 M across at least 2 rounds (pre-seed ~$320 K + seed $3 M)
- Last round: $3 M seed, January 7 2026, led by Stellaris Venture Partners
- Headcount: Not publicly disclosed; Tracxn lists company as early-stage; LinkedIn page at https://in.linkedin.com/company/arrowheadapp shows presence but live count not captured (as of 2026-05-10)
- Revenue / ARR: ₹71.2 L (~$85 K USD) as of FY 2024-25 (March 31 2025, MCA filing via Tracxn); 5× ARR growth August–October 2025 (claimed); 1,441% 1-year revenue CAGR (Tracxn/MCA data)

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| ~Jul 2023 (approx.) | Pre-Seed | ~$320 K (≈ ₹2.7 Cr) | Campus Fund (India) | Undisclosed angels | Tracxn; Wellfound |
| Jan 7 2026 | Seed | $3 M (≈ ₹25 Cr) | Stellaris Venture Partners | Kunal Shah (CRED founder); Madhusudanan R (M2P co-founder); Keyur Rajiv Kashikar (Turtlemint exec); Pramod Mohandas (Kissht exec); Shadab Shamim (Kissht exec); other angels | Inc42; Business Standard; Entrepreneur India |

**Notes:**
- Tracxn lists $3.32 M total across 4 rounds; the breakdown of rounds 3 and 4 (if distinct from the two above) is not publicly confirmed.
- Valuation at seed: Not disclosed.
- All angel investors in the seed round are also customers of the platform (investor-customer overlap).
- Vardhan Dharnidharka (Principal, Stellaris) quoted the BFSI voice AI market at $3 B in India, with <$50 M penetrated.

## 3. Product & Customers

### Products
**Core product: AI Voice Calling Agent (outbound + inbound)**
- End-to-end automated phone sales/service conversations with no human in the loop by default
- Proprietary orchestration layer enabling multi-turn dialogues up to 20 minutes
- Handles interruptions, pauses, objections naturally
- Live in-call actions: payment link dispatch, real-time data pulls from CRM, human transfer escalation
- Language switching mid-call (real-time)
- 1-minute lead-to-call initiation time
- Compliance-aware dynamic scripting with regulatory guardrails (BFSI-focused)
- SOC 2 compliant; NIST-aligned; BFSI-grade information security

**Use-case verticals within BFSI:**
- Lending: loan sales, EMI collections, KYC follow-up
- Insurance: health, life, motor sales and renewals
- Securities: mutual fund and fixed-deposit sales
- Customer support: inbound query handling and routing

**Roadmap (12–18 month horizon, claimed January 2026):**
- Emotion-aware voice agents
- Omnichannel expansion (chat, messaging, phone)
- Large-scale concurrent call infrastructure (thousands of simultaneous calls)
- BFSI-specific fine-tuned conversation models

### Pricing
- Custom enterprise pricing only; no public tiers or per-minute rates disclosed.
- Website states "pricing built for your scale" with no one-size-fits-all model.
- Customers contact sales or start a pilot to receive a quote.
- Source: https://arrowhead.ai/pricing (verified fetch, May 2026)

### Languages & Voices
- 10+ languages: English, Hindi, Tamil, Telugu, Malayalam, Kannada, Bengali, Malay (Malaysia)
- Mid-call language switching capability (verified claimed feature)
- New languages deployable in under 3 weeks (claimed)
- Specific voice count / voice-cloning catalog: Not publicly disclosed
- Indic language coverage: 7 confirmed Indian languages; Malay for Southeast Asia

### Named Customers (verified from press coverage)
| Customer | Segment | Noted Outcome |
|----------|---------|---------------|
| Bank of Baroda Cards | Banking | Named client |
| Aditya Birla Capital | NBFC/Insurance | Named client |
| Paytm | Fintech | 45% higher conversion, 15× customer volume (VP testimonial) |
| Tata 1mg | Healthtech | Named client |
| upGrad | EdTech | Named client |
| Kissht | Fintech/Lending | Named client (exec also angel investor) |
| Turtlemint | InsurTech | Named client (exec also angel investor) |
| InsuranceDekho | InsurTech | Named client |
| Equentis | Wealth/Securities | Named client |
| Mudra Fincorp | NBFC | Named client |

**Total: 50+ customers** across India and Southeast Asia (Malaysia) as of January 2026.
**100% POC-to-production conversion rate** (claimed).

### Integrations / SDKs
**Dialers:** Ameyo, Ozonetel, Exotel, Tata Teleservices
**CRMs / Marketing:** Salesforce, Leadsquared, Clevertap, Zendesk
**Custom integrations:** Available for proprietary systems
**Deployment options:** India data center, Singapore data center, on-premise
**API/SDK documentation:** Not publicly available; no developer docs portal found.

## 4. Technical Architecture

### Model approach
- Proprietary orchestration layer (Arrowhead-built) managing multi-turn dialogue state
- Fine-tuned LLM(s) for BFSI conversation flows — underlying base model(s) not disclosed
- Sub-500 ms end-to-end latency infrastructure (claimed; not independently benchmarked)
- Handles hallucination-free conversations up to 20 minutes (claimed)
- Pipeline presumed: STT → LLM dialogue manager → TTS with compliance guardrails; specifics not published

### Training data
- Not publicly disclosed
- BFSI conversation corpus implied (call recordings from enterprise deployments)
- No published datasets or model cards found on HuggingFace or arXiv

### Latency profile
- Claimed: sub-500 ms end-to-end response latency (source: Outlook Business, Startuptalky)
- TTFB / RTF / streaming specifics: Not publicly published
- No independent benchmark or engineering blog post found as of May 2026

### Voice cloning
- Not explicitly offered as a standalone product
- Voice persona customization implied (customers provide call recordings for bot training)
- Setup requires: call flow documentation + call recordings; bot live in <2 weeks
- Voice cloning specs (sample length, speaker similarity scores): Not publicly disclosed

### Prosody / emotion control
- Emotion-aware voice agents listed as 12–18 month roadmap item (not yet shipped as of Jan 2026)
- Current system simulates "authentic human emotion and tone" (marketing claim); technical implementation not detailed

### Indic language strategy
- 7 Indian languages confirmed: Hindi, English, Tamil, Telugu, Malayalam, Kannada, Bengali
- Mid-call code-switching supported (e.g., Hindi↔English)
- No explicit Bhashini, AI4Bharat, or IndicVoices integration mentioned
- No ONDC or government tender exposure found
- Proprietary fine-tuning approach implied; no academic collaboration noted

### Inference stack
- Cloud-hosted (India DC, Singapore DC); on-premise available
- Dialer integrations suggest telephony-native delivery (not browser/WebRTC first)
- Specific inference framework (vLLM, TensorRT, etc.): Not disclosed
- Model sizes: Not disclosed

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Stellaris VP Podcast: Arrowhead — Verticalized Voice AI for BFSI in India | Podcast | Jan 2026 | https://www.stellarisvp.com/podcast/arrowhead-verticalized-voice-ai-for-bfsi-in-india-stellaris-vp-ft-devyani-vengad-vardhan |
| YourStory: Arrowhead's aim is sharp and clear | Feature article | Feb 2026 | https://yourstory.com/2026/02/arrowhead-building-conversational-ai-that-impacts-business-outcomes |
| Zero Shot Podcast: Voice AI startups are drawing in VC cheques fast | Podcast | Feb 2026 | https://podcasts.apple.com/in/podcast/voice-ai-startups-are-drawing-in-vc-cheques-fast-will/id1841604201?i=1000750224104 |

No arXiv papers, engineering blog, or technical writeups found as of May 2026.

## 5. Open Source Footprint

### GitHub
- https://github.com/arrowhead-ai — **404 Not Found** (verified fetch, May 2026)
- No other GitHub org URL found in public sources.

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| None found | — | — | — | — | No public repos identified |

### Hugging Face
- https://huggingface.co/arrowhead-ai — **404 Not Found** (verified fetch, May 2026)

| Model | Downloads | Likes | License |
|-------|-----------|-------|---------|
| None found | — | — | — |

### Top contributors
Not applicable — no open-source footprint found.

**Summary:** Arrowhead has zero public open-source presence. It is a fully proprietary, closed-source platform. No community ecosystem exists around the codebase.

## 6. Team

### Founders
| Name | Role | Background | Notes |
|------|------|-----------|-------|
| Devyani Gupta | CEO & Co-founder | Wharton (Statistics, Univ. of Pennsylvania); former BCG Consultant and Associate; Millward Brown; Teach for the Philippines; Kenanga Investment | Currently listed as CEO on website and LinkedIn |
| Vengadanathan Srinivasan | CTO & Co-founder | Prior experience at AWS, Rippling, Uber, Airbnb — described as "Staff Eng with get-shit-done attitude" | Currently listed as CTO |
| Lalit Gupta | Co-founder & COO | Background not publicly detailed | Listed by Tracxn as co-founder; role as COO per some sources |
| Chinmay Shah | Former Co-founder & CTO | Ex-Arrowhead (departed, date unknown); currently Applied AI @ Salient (AI agent reliability) | Departed from Arrowhead; LinkedIn profile at https://www.linkedin.com/in/chinmayshah99/ shows Salient affiliation |

### Key technical hires
Not publicly disclosed beyond founders. Engineering, data science, and customer success hiring ongoing per seed round press release.

### Recent joiners (last 12mo)
Not publicly tracked. Post-seed hiring planned across engineering, data science, customer success, and sales (stated January 2026).

### Notable departures (last 12mo)
- **Chinmay Shah** (former co-founder, role: CTO): Departed Arrowhead (exact date not confirmed publicly); now at Salient in an applied AI role. This is a notable co-founder departure.

### Open roles signal
- No public careers page found (arrowhead.ai/careers returned 404).
- Uplers lists "Arrowhead Jobs & Careers — Open Positions — Mar 2026" suggesting active hiring.
- Roles expected: engineering, data science, customer success, sales (per seed announcement).

### Advisors / Board
- Stellaris Venture Partners (Vardhan Dharnidharka, Principal) — board observer likely given seed lead
- No formal advisory board publicly listed

## 7. Moat & Defensibility

- **Data moat:** Moderate. 50+ BFSI enterprise customers generating proprietary Indian telephony conversation data across lending, insurance, and securities — difficult to replicate quickly. Quality and volume of labeled BFSI call data is a genuine advantage if curated well. Score: 3/5
- **Model moat:** Low–moderate. Fine-tuned on BFSI-specific conversation flows; emotion-aware models on roadmap. However, base model(s) are likely off-the-shelf LLMs. No published model research or patents. Competitors (Gnani, Sarvam) also have Indic data advantages. Score: 2/5
- **Distribution moat:** High for current wedge. Deep BFSI relationships; angel investors who are also customers create referral loops in a relationship-driven sector. Presence in Southeast Asia (Malaysia) adds defensibility. 100% POC-to-production rate suggests strong stickiness. Score: 4/5
- **Brand / community moat:** Low. No open-source community, no developer ecosystem, no brand recognition outside BFSI enterprise circles. Score: 1/5
- **Regulatory moat:** Low currently. SOC 2 and NIST compliance is table stakes. DPDP Act compliance not explicitly claimed. No Bhashini, ONDC, or government-tender engagement found. TRAI DND scrubbing / DLT compliance not publicly documented. Score: 2/5
- **Replication cost (well-funded $10M competitor):** Moderate. A $10M competitor with existing LLM infrastructure could replicate the technical stack in 6–9 months. The harder moat is the 50+ BFSI customer relationships and the BFSI conversation training data corpus. Estimated 12–18 months to meaningfully replicate full go-to-market + data flywheel.
- **Moat strength: 3/5** — Strong distribution wedge in a relationship-driven vertical offsets thin technical moat; data flywheel is real but early-stage.

## 8. Risks & Problems

### Technical complaints
- No Reddit, Hacker News, GitHub issues, or X complaints found specifically about arrowhead.ai product quality (may reflect small user base or B2B confidentiality).
- Industry-wide concern about voice AI detection: if TRAI or RBI mandates bot-disclosure during calls, Arrowhead's "customers don't know it's a bot" value proposition faces direct regulatory risk.
- 20-minute hallucination-free claim is extraordinary; no independent audit or benchmark published.

### Pricing pain points
- Custom enterprise pricing with no public rates creates friction for SMB/mid-market sales; compared to competitors like Bolna.ai (~₹5.52/min) or Caller Digital (₹8–₹25/call), Arrowhead appears positioned as premium BFSI enterprise.
- No self-serve or freemium tier; all deals require sales contact.

### Safety / misuse
- Core use case (AI posing as human on outbound sales calls) raises potential regulatory exposure under emerging bot-disclosure norms.
- TRAI in India has not mandated bot identification on calls as of May 2026, but regulatory trajectory globally (EU AI Act) and in India (DPDP rules) could restrict undisclosed AI calling.
- Insurance and loan sales conversations handled by AI without disclosure could create mis-selling liability for enterprise customers.

### Legal / regulatory
- No litigation found.
- DPDP Act (India, 2023) compliance not explicitly claimed — telephony data of consumers is sensitive personal data; call recording storage in India DC or Singapore DC raises consent and localization questions.
- RBI and IRDAI (insurance regulator) have not yet issued specific guidance on AI-only customer sales calls; regulatory ambiguity is a tail risk.

### Churn signals
- No public churn data.
- Co-founder departure (Chinmay Shah) is a yellow flag for a company of this age and stage.
- Revenue of ₹71.2 L (~$85 K) as of March 2025 is very early; 5× ARR growth Aug–Oct 2025 suggests acceleration but the base was small.

## 9. Competitive Position

- **Direct competitors (India BFSI voice AI):**
  - Gnani.ai — much larger (30M conversations/day, 14M hours training data, HDFC Bank, Airtel); enterprise-only (6-figure minimums); 8–16 week deployment
  - Sarvam AI — foundational model layer; not a direct application competitor but could enable others
  - Smallest.ai — TTS/voice infrastructure focus; sub-100ms latency; no BFSI application layer
  - Bolna.ai — developer-focused; $6.3M seed from General Catalyst; no BFSI compliance depth
  - Caller Digital — ₹8–₹25/call; NDND/DLT compliance built-in; India-focused; similar wedge
  - Vaani AI — voice infrastructure for India
  - Krutrim (Ola) — general Indic AI; not direct BFSI voice agent competitor
  - Global: ElevenLabs ($3B+ valuation), Deepgram, Bland.ai — not Indic-native, no BFSI compliance

- **Where it's winning:**
  - Deep BFSI vertical focus with compliance-aware scripting that generalist platforms lack
  - Customer-investors creating low-friction enterprise referrals in India's relationship-driven financial sector
  - Malaysia beachhead in Southeast Asia — rare among Indian voice AI startups
  - 100% POC-to-production rate and <2-week deployment speed reduce sales friction

- **Where it's losing:**
  - Scale: Gnani processes 30M conversations daily vs. Arrowhead's undisclosed but likely much smaller volume
  - Developer mindshare: zero open-source presence, no APIs for self-serve; losing to Bolna.ai and Smallest.ai in developer community
  - Brand: minimal content, no engineering blog, no conference presence found
  - Pricing transparency: losing SMB/mid-market deals to competitors with public pricing

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| Jan 7 2026 | $3M seed round announced, led by Stellaris; Kunal Shah, M2P's Madhusudanan R as angels | Inc42, Business Standard, Entrepreneur India |
| Jan 7 2026 | Stellaris VP podcast: "Verticalized Voice AI for BFSI in India" featuring Devyani, Vengad, Vardhan | stellarisvp.com, YouTube |
| Feb 2026 | YourStory feature: "Arrowhead's aim is sharp and clear" — in-depth profile | YourStory |
| Feb 17 2026 | Zero Shot podcast: Devyani describes voice AI as "a land grab market" | Apple Podcasts |
| Mar 2026 | Uplers lists open positions for Arrowhead — active hiring signal | Uplers |

**Velocity verdict:** Moderate-High. The $3M seed closed in January 2026 with marquee BFSI angels who are also customers — a strong signal. 5× ARR growth Aug–Oct 2025 and 100% POC conversion are credible early traction markers, though from a very small absolute base (₹71.2L ARR as of March 2025). Press coverage has been solid for a seed-stage company but concentrated around the funding announcement. No product launches, partnership announcements, or regulatory wins in the past 12 months beyond the seed round itself. The co-founder departure (Chinmay Shah) is an unresolved question mark. Overall trajectory is upward but the company is still in early innings of proving scale.

## 11. Bull Case / Bear Case

**Bull:**
- Vertical AI for BFSI is a large, defensible wedge: $3B market, <$50M penetrated; Arrowhead is one of the first movers with enterprise-grade deployments.
- Customer-investor flywheel (CRED's Kunal Shah, M2P's Madhusudanan R) provides warm intros across India's densely networked fintech ecosystem.
- 100% POC-to-production rate and <2-week deployment suggest strong product-market fit.
- 5× ARR growth over just 3 months (Aug–Oct 2025) could sustain if the BFSI adoption cycle accelerates.
- Southeast Asia expansion (Malaysia) diversifies revenue and de-risks India regulatory concentration.
- Emotion-aware agents + omnichannel roadmap could deepen the moat if executed before larger players focus here.

**Bear:**
- Revenue base is tiny (~$85K ARR as of March 2025); the company needs to scale dramatically before the seed runway runs out.
- Co-founder departure (Chinmay Shah — formerly CTO) at an early stage is a structural risk.
- Regulatory risk is high: TRAI or RBI mandating bot-disclosure on outbound sales calls would force a pivot in the core value proposition.
- Gnani.ai already serves many of the same BFSI enterprise customers at far greater scale — Arrowhead's moat may be thinner than it appears.
- Zero open-source footprint means no community flywheel; fully dependent on top-down enterprise sales, which is slow and expensive.
- Underlying LLM and TTS models are likely off-the-shelf; no proprietary model research means any incumbent (Google, OpenAI, Sarvam) could bundle competitive capabilities.
- Pricing opacity (no public rates) slows mid-market adoption.

## 12. What I Couldn't Find
- Exact pre-seed round date and full list of pre-seed investors beyond "Campus Fund"
- Specific per-minute or per-call pricing (confirmed custom enterprise model, no public rates)
- Headcount number (current or 6-months ago); LinkedIn company page exists but live employee count not captured
- Underlying LLM model family or TTS model used
- Audio codec / tokenizer details
- TTFB, RTF, or streaming latency benchmarks from any independent source
- Voice cloning sample requirements and speaker-similarity specs
- Any arXiv papers, patents, or engineering blog posts from Arrowhead team
- GitHub or HuggingFace presence (both 404)
- Exact departure date and circumstances of co-founder Chinmay Shah
- Post-money valuation at seed round
- DPDP Act compliance posture
- Bhashini, ONDC, or government-tender engagement (none found)
- G2 / Capterra reviews (no profile found on either platform as of May 2026)
- Number of voices or voice personas in the platform catalog
- Detailed customer case study links beyond summary stats in press coverage

## Sources
1. https://arrowhead.ai/ — official website (fetched May 2026)
2. https://arrowhead.ai/about-us — about page (fetched May 2026)
3. https://arrowhead.ai/pricing — pricing page (fetched May 2026)
4. https://inc42.com/buzz/arrowhead-raises-3-mn-to-scale-voice-ai-for-bfsi-sales/ — Inc42 seed round article, Jan 2026
5. https://www.business-standard.com/companies/start-ups/arrowhead-raises-3-mn-to-expand-human-like-voice-ai-for-financial-sales-126010600930_1.html — Business Standard, Jan 2026
6. https://www.entrepreneur.com/en-in/news-and-trends/voice-ai-startup-arrowhead-bags-usd-3-mn-funding-led-by/501668 — Entrepreneur India, Jan 2026
7. https://www.bwdisrupt.com/article/voice-ai-startup-arrowhead-raises-3-mn-seed-round-led-by-stellaris-cred-s-kunal-shah-joins-as-angel-586864 — BW Disrupt, Jan 2026
8. https://www.outlookbusiness.com/corporate/voice-ai-start-up-arrowhead-raises-3m-led-by-stellaris-to-automate-bfsi-sales — Outlook Business, Jan 2026
9. https://www.indianstartuptimes.com/investment/arrowhead-secures-3-million-seed-funding-to-scale-human-like-voice-ai-for-financial-sales/ — Indian Startup Times
10. https://startuptalky.com/news/arrowhead-raises-3m-led-by-stellaris-to-build-human-like-voice-ai-for-bfsi/ — Startuptalky (fetched May 2026)
11. https://www.stellarisvp.com/podcast/arrowhead-verticalized-voice-ai-for-bfsi-in-india-stellaris-vp-ft-devyani-vengad-vardhan — Stellaris VP podcast (fetched May 2026)
12. https://www.youtube.com/watch?v=FMDKsZwe2Yg — YouTube: Stellaris VP podcast video, Jan 2026
13. https://yourstory.com/2026/02/arrowhead-building-conversational-ai-that-impacts-business-outcomes — YourStory feature, Feb 2026 (403 on fetch; content via search snippet)
14. https://podcasts.apple.com/in/podcast/voice-ai-startups-are-drawing-in-vc-cheques-fast-will/id1841604201?i=1000750224104 — Zero Shot podcast, Feb 2026
15. https://tracxn.com/d/companies/arrowhead/__KjshHats-4Ax5h9wiRF-l_Y0jJXHlJxoLif6NfuoDJw — Tracxn company profile (fetched May 2026)
16. https://tracxn.com/d/legal-entities/india/ah-live-private-limited/__I8D7640S2DoJmG7st-IDUfshEYhtoQqltTmeSzyTeq0 — Tracxn legal entity page for AH LIVE PRIVATE LIMITED (fetched May 2026)
17. https://www.crunchbase.com/organization/arrowhead-ddc0 — Crunchbase profile (403 on fetch; data via search)
18. https://in.linkedin.com/company/arrowheadapp — LinkedIn company page
19. https://www.linkedin.com/in/devyani-gupta-57644ba8/ — Devyani Gupta LinkedIn
20. https://www.linkedin.com/in/vengadanathan-srinivasan-82564b33/ — Vengadanathan Srinivasan LinkedIn
21. https://www.linkedin.com/in/chinmayshah99/ — Chinmay Shah LinkedIn (former co-founder; now Salient)
22. https://news.aibase.com/news/24377 — AIBase news (fetched May 2026)
23. https://www.voiceaispace.com/tool/arrowhead — Voice AI Space directory (fetched May 2026)
24. https://www.caller.digital/blog/best-ai-calling-platform-india-2026-comparison — Caller Digital competitive comparison (fetched May 2026)
25. https://www.entrepreneurindia.com/blog/en/news/voice-ai-startup-arrowhead-bags-usd-3-mn-funding-led-by-stellaris-venture-partners.58648 — Entrepreneur India (via search)
26. https://wellfound.com/company/arrowhead-team/funding — Wellfound funding page (via search)
27. https://pitchbook.com/profiles/company/542344-60 — PitchBook profile (paywalled)
28. https://www.zoominfo.com/p/Devyani-Gupta/5262146664 — ZoomInfo (contact data for Devyani Gupta)
29. https://inc42.com/features/india-talks-the-ai-walk/ — Inc42 India voice AI landscape feature
