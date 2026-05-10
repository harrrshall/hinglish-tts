# GreyLabs AI

**Website:** https://greylabs.ai  •  **HQ:** Mumbai, India (Powai, Maharashtra)  •  **Founded:** October 2023  •  **Stage:** Series A
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): Verticalized agentic Voice AI and speech analytics platform purpose-built for India's BFSI contact centers — converts raw call recordings into compliance checks, sales intelligence, and autonomous customer interactions.
- Total funding to date: ~$11.7M (₹~97.5 Cr) across three rounds
- Last round: ₹85 Cr (~$10.2M), Series A, October 6 2025, lead: Elevation Capital
- Headcount: ~49–71 (Tracxn reports 71 as of March 31 2026; Latka/PitchBook report 44–49 in mid-2025; company stated "80+" in October 2025 press releases — figures conflict, see note)
- Revenue / ARR: ₹3.81 Cr (~$450K) FY2025 per Tracxn MCA filing. Latka claims "$11M revenue" for 2025 — treat as unverified/self-reported. ARR target of $1M for Voice AI Agents product by March 2026 mentioned in Inc42 pre-Series A exclusive.

> **Headcount note:** Official press releases at Series A say "80+ team," Tracxn MCA-sourced figure is 71 (March 2026), PitchBook/Latka show 44–49 (mid-2025). The 80+ figure is likely a post-Series A hiring-plan statement rather than a verified current count.

## 2. Funding History
| Date | Round | Amount (USD) | Amount (INR) | Lead | Other Investors | Source |
|------|-------|-------------|-------------|------|-----------------|--------|
| May 17, 2024 | Seed Round 1 | ~$1.5M | ~₹12.5 Cr | Matrix Partners India (now Z47) | Vasant Sridhar (OfBusiness), Narasimha Reddy (MoEngage), Nitin Gupta (Uni Cards), Anil Goteti (Scapia Cards), other angels | IBSIntelligence, Entrackr (Jun 2024) |
| Jul 10, 2024 | Seed Round 2 | Not disclosed | Not disclosed | Not disclosed | Not disclosed | Tracxn (reports two seed tranches) |
| Oct 6, 2025 | Series A | ~$10.2M | ₹85 Cr | Elevation Capital | Z47 (existing), undisclosed angels | Entrackr, Z47 press release, Elevation Capital blog |

**Post-money valuation (Series A):** Tracxn shows ₹430 Cr (~$51.8M) as of August 2025; Latka reports $33M — figures conflict. Neither is independently verified. Valuation not officially disclosed.

**Founder equity:** 67.48% of equity (per Tracxn, citing MCA data — source: Tracxn, verified as of 2026).

## 3. Product & Customers
### Products
GreyLabs AI offers a three-product suite targeting BFSI contact center operations:

1. **Voice AI Agents (Agentic Voice AI Platform)** — Flagship product launched ~H2 2025. Autonomous AI agents that conduct outbound/inbound calls for: telesales, customer service, collections, loan/insurance renewals, and PIVC (Post-Issuance Verification Calls — an RBI-mandated verification step for credit cards). Multilingual, compliant, tuned for India. Positioned as the "full call automation" play.

2. **Speech Analytics** — The original product (launched at seed stage). Analyzes 100% of recorded call center conversations using STT + LLMs fine-tuned for BFSI. Key use cases: agent QA automation (replacing the industry-standard ~1% manual audit), compliance monitoring (detecting CVV disclosures, abusive language, mis-selling), lead scoring, churn prediction, cross-sell opportunity identification. Integrates with dialing systems (Cisco, Avaya/Aspect) and CRMs. Charges on a per-minute basis for call processing.

3. **Email Analytics** — AI-driven sentiment, intent, and compliance monitoring across email communications; ensures timely follow-ups and tracks task completion.

### Pricing
- Speech Analytics billed per processed call-minute (verified from Inc42 article, June 2024)
- Voice AI Agents pricing not publicly disclosed; likely per-minute or per-call enterprise contract
- No self-serve or published pricing tiers found on website or G2/Capterra

### Languages & Voices
- Confirmed support: English, Hindi, Hinglish (verified from seed-stage coverage, June 2024)
- Claimed: "Multiple Indian languages and dialects" (mentioned in all Series A press releases — exact language count not publicly disclosed)
- No specific voice cloning or voice library count publicly documented
- No Bhashini integration verified (searched explicitly — no evidence found as of May 2026)

### Named Customers
The following are publicly named in press releases and media (verified across multiple sources):
- RBL Bank
- AU Small Finance Bank
- IDFC FIRST Bank
- Axis Finance
- SBI Life Insurance
- Piramal Finance
- ICICI Prudential Life Insurance
- Motilal Oswal Financial Services
- Fibe (formerly EarlySalary)
- Groww

**Total claimed client count:** 50+ BFSI institutions (as of Series A, Oct 2025). 7 clients at seed (June 2024). "10 large enterprise clients" per Inc42 deep-dive (mid-2024). Growth to 50+ by Oct 2025 is consistent across sources.

**Target:** Scale to 300+ institutions.

**Interactions processed:** "Hundreds of millions of conversations" in 18 months (claimed, Oct 2025 — not independently verified).

### Integrations / SDKs
- Dialing system integrations: Cisco, Avaya/Aspect (mentioned in Inc42 feature)
- CRM integrations: mentioned as available, specific vendors not named publicly
- Neysa NeysaVelocis AI cloud: infrastructure partnership announced October 15 2025
- No public SDK, API documentation, or developer portal found

## 4. Technical Architecture
### Model approach
- Proprietary STT (Speech-to-Text) engine described as achieving "near-human accuracy" for BFSI-specific audio (claimed)
- LLMs fine-tuned specifically for BFSI vocabulary, compliance requirements, and Indian language patterns
- "Compliance controls integrated at the model layer" (domain-specific guardrails, not a bolt-on)
- Agentic Voice AI platform capable of autonomous multi-turn conversations (not just scripted IVR)
- Positioning: "We are not in the business of Maruti Suzuki. We are in the business of Airbus" — bespoke, deeply integrated, not a commodity API (Aman Goel quote, Elevation Capital Day One Podcast)

### Training data
- Not publicly disclosed
- Inferred: proprietary BFSI call recordings from 50+ client institutions provide significant domain-specific training signal (data flywheel moat)
- No public dataset contributions, arXiv papers, or Hugging Face datasets found

### Latency profile
- Not publicly disclosed (no TTFB, RTF, or streaming latency benchmarks published)
- Real-time capability implied by live voice agent product; latency specifics not available

### Voice cloning
- Not publicly discussed; product focus is on autonomous agents, not voice cloning as a standalone feature
- Agents likely use synthesized voices rather than cloned customer voices

### Prosody / emotion control
- Speech analytics product includes sentiment detection and emotion analysis (negative sentiment flagging for collections compliance)
- Agent-side prosody/emotion control not publicly documented

### Indic language strategy
- Current confirmed: English, Hindi, Hinglish
- Claimed: additional Indian languages (unspecified)
- No Bhashini or AI4Bharat integration announced
- Strategy appears to be proprietary model fine-tuning on BFSI call data rather than leveraging public Indic models
- Multilingual capability positioned as core BFSI differentiator for India's linguistically diverse customer base

### Inference stack
- Cloud-based (inferred from Neysa partnership — uses Neysa's India-based AI Acceleration Cloud for regulatory data-localization compliance)
- RBI, SEBI, IRDA data-localization requirements met via India-based infrastructure
- On-device: no evidence
- No public information on model sizes, GPU stack, or inference framework

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| GreyLabs AI Blog | Company blog | Active | https://www.greylabs.ai/blog |
| "Building Voice AI For India's Banks" | Elevation Capital podcast/essay | Oct 2025 | https://www.elevationcapital.com/perspectives/greylabs-ai-building-voice-ai-for-india-banks |
| "A Billion Conversations" (podcast episode) | Podcast | Oct 2025 | https://www.youtube.com/watch?v=Tcwr7D3C3H0 |
| "Meet the Founders of GreyLabs AI" (Pranay Desai / Z47) | Podcast/video | Jun 2024 | https://www.youtube.com/watch?v=7G9A_SSTr20 |
| AI Impact Summit Delhi (Aman Goel panel) | Public appearance | Feb 2026 | https://www.youtube.com/watch?v=3vFpZeoWM58 |

No arXiv preprints, academic papers, or technical engineering blog posts found as of May 2026.

## 5. Open Source Footprint
### GitHub
No GitHub organization for GreyLabs AI found. Search of `site:github.com GreyLabs` returned no matching organization. **No public open-source repositories confirmed.**

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| — | — | — | — | — | No public repos found |

### Hugging Face
No Hugging Face organization or model card for GreyLabs AI found. **No public HF presence confirmed.**

| Model | Downloads | Likes | License |
|-------|-----------|-------|---------|
| — | — | — | — |

### Top contributors
Not applicable — no public open-source activity found.

## 6. Team
### Founders
| Name | Role | Background |
|------|------|------------|
| Aman Goel | Co-Founder & CEO | B.Tech CS, IIT Bombay. Co-founded Cogno AI in 2017, bootstrapped to $1M+ ARR, acquired by Exotel in 2021 (multi-million dollar deal). Worked at Exotel ~2 years post-acquisition. LinkedIn: @goel-aman |
| Harshita Srivastava | Co-Founder & CPO (Chief Product Officer) | B.Tech/M.Tech, IIT Kanpur. Previously at Citi, Cogno AI, Exotel. Skills: ML, Python, Django, C++. Life partner of Aman Goel (co-founders are also a personal couple). LinkedIn: @harshita-srivastava-78961285 |
| Shreyas Patel | Co-Founder & CTO | Studied at Ahmedabad University. Leads Technology and Information Security. LinkedIn: @sg-patel |
| Debabrata Basak | Co-Founder | Previously co-founded Cogno AI. Role at GreyLabs not publicly specified. |
| Raj Sanghavi | Co-Founder | Previously co-founded Cogno AI. LinkedIn: @rajsanghavi. Role not specified. |
| Shivam Gupta | Co-Founder | Previously co-founded Cogno AI. Role not specified. |

**Note on Cogno AI provenance:** Tracxn and early Inc42 articles list Aman Goel and Harshita Srivastava as the two initial co-founders (Oct 2023). Basak, Sanghavi, Gupta, and Patel joined later and are described as the Cogno AI alumni. The six are collectively referred to as co-founders in all Series A materials.

### Key technical hires
Not publicly disclosed beyond founders. No named VP Engineering, Head of AI Research, or other senior technical hires identified in public sources.

### Recent joiners (last 12mo)
- Specific named hires not publicly disclosed
- Company actively hiring per Wellfound/Instahyre job boards (as of research date)
- Plans to expand teams in Bengaluru (engineering/R&D) and Delhi (sales/client support) post-Series A

### Notable departures (last 12mo)
None identified in public sources.

### Open roles signal
- Job listings active on Wellfound and Instahyre (as of May 2026)
- Categories inferred from expansion plans: ML engineers, BFSI sales, customer success
- Aman Goel reportedly personally interviews all hires including interns (per Elevation Capital podcast)

## 7. Moat & Defensibility

- **Data moat:** Strong. 50+ BFSI institutions feeding proprietary call recordings creates a domain-specific training corpus unavailable to general-purpose competitors. Each new client strengthens STT accuracy and LLM fine-tuning for Indian financial services language. Data flywheel is the primary moat.

- **Model moat:** Moderate. STT + LLM fine-tuned on BFSI-specific data has meaningful lead over generic models (Whisper, etc.) on Indian-accented financial vocabulary, agent scripts, regulatory terminology. Not insurmountable for a well-funded competitor, but requires 12–24 months of BFSI-specific data to replicate meaningfully.

- **Distribution moat:** Growing. 50+ enterprise BFSI relationships with marquee names (SBI Life, ICICI Pru, AU Bank) create reference customers that lower sales friction for the next 250 targets. Integration depth with Cisco/Avaya dialers and CRMs creates switching costs. BFSI procurement cycles are long (6–18 months), making churn structurally lower.

- **Brand / community moat:** Early. Growing presence in BFSI AI conversation (Aman Goel speaking at summits, Elevation Capital backing adds credibility). No developer community, open-source presence, or Bhashini/AI4Bharat affiliation found.

- **Regulatory moat:** Moderate. Compliance built into the model layer for RBI/SEBI/IRDA requirements (PIVC automation, collections compliance, data localization via India-based infrastructure) creates genuine switching costs for regulated BFSI clients. New entrants must invest heavily in regulatory fit. No DPDPA or MeitY certification publicly claimed.

- **Replication cost (6-month, $10M competitor):** A $10M competitor could replicate the product architecture but would lack the proprietary BFSI call data, the Cogno AI institutional relationships, and the regulatory depth. Estimated 18–24 months and $15–20M to reach parity on data and customer trust. Technical product could be cloned faster (~6 months for MVP), but go-to-market and data moat would lag.

- **Moat strength: 3.5/5** — Strong data flywheel and BFSI regulatory fit create real defensibility, but the company is pre-scale ($450K FY25 ARR per MCA filings), and both Uniphore (well-funded, global) and potential Sarvam expansion into BFSI represent credible threats.

## 8. Risks & Problems
### Technical complaints
- No public customer complaints on Reddit, Hacker News, or GitHub found (too early-stage and enterprise B2B for consumer review presence)
- No G2 or Capterra product review pages found with substantive ratings
- Employee reviews: 5/5 Glassdoor rating based on 16 reviews — very small sample, likely founder-influenced
- Indic language coverage beyond Hindi/English unverified; "multilingual" claim is not backed by a specific language list

### Pricing pain points
- Per-minute billing for speech analytics can create budget unpredictability for large call centers with high volumes
- Enterprise-only model (no self-serve) limits SME/MSME reach
- No public pricing transparency — likely requires long sales cycles

### Safety / misuse
- Autonomous voice agents conducting collections calls raise consumer protection concerns (RBI collections guidelines, TRAI telemarketing rules)
- PIVC automation could be misused if identity verification guardrails fail
- No public AI safety or responsible-use policy found on website

### Legal / regulatory
- Data localization mandatory for BFSI — addressed via Neysa partnership (India-based infra), but dependent on third-party
- DPDPA (Digital Personal Data Protection Act, India 2023) compliance requirements for call recording and processing not publicly documented
- No litigation, IP disputes, or regulatory actions found

### Churn signals
- No churn signals found in public sources
- Inc42 pre-Series A report mentioned two M&A offers received (April 2025) — could indicate founders tested exits, though they proceeded with the funding round instead

## 9. Competitive Position
- **Direct competitors:**
  - India-focused: Gnani.ai (Bengaluru, voice AI + STT for Indian languages, BFSI focus), Mihup (speech analytics, India), Contiinex (India BFSI), Reverie Language Technologies (Indic NLP/ASR)
  - Global with India presence: Uniphore (Series E, $600M+ raised, global conversational AI), Observe.AI (US, contact center AI), NICE CXone (enterprise), Verint, Invoca
  - Horizontal AI risks: Sarvam AI (foundation model approach, could enter verticalized BFSI analytics)

- **Where it's winning:**
  - Deep BFSI-specific verticalization beats horizontal players in regulatory fit and PIVC/collections compliance
  - Founder-market fit (Cogno AI alumni) provides trust and faster enterprise sales than pure-tech new entrants
  - India-first data localization and RBI/SEBI/IRDA compliance built-in from day one

- **Where it's losing / vulnerable:**
  - Uniphore has significantly more capital, global customer references, and a longer technology runway
  - Latent risk from Sarvam AI or AI4Bharat-backed players building BFSI-ready Indic language models as a public good
  - No open-source or developer community presence means no bottom-up GTM channel
  - MCA-reported FY25 ARR of ~₹3.81 Cr ($450K) is materially smaller than some competitor claims suggest — scale is still very early

## 10. News & Momentum (last 12 months)
| Date | Event | Source |
|------|-------|--------|
| Jun 18 2024 | Seed round closed: >$1.5M led by Matrix Partners India (Z47) | Entrackr, IBSIntelligence |
| Aug 2024 | YourStory deep-dive: "GreyLabs AI bets on GenAI to tune into customer conversations" | YourStory |
| Apr 2025 | Two M&A acquisition offers received (details undisclosed; company proceeded with fundraise) | Latka |
| Jul 4 2025 | Series A closes internally (Tracxn date); announced publicly Oct 6 2025 | Tracxn |
| Oct 6 2025 | Series A announced: ₹85 Cr led by Elevation Capital; 50+ BFSI clients; "hundreds of millions of conversations" | Entrackr, Z47, Inc42, Entrepreneur, SiliconIndia |
| Oct 6 2025 | Elevation Capital publishes investment thesis blog post + Day One Podcast episode with Aman Goel | Elevation Capital |
| Oct 15 2025 | Strategic partnership with Neysa (AI cloud infra) announced; joint BFSI voice compliance solution | Tribune India, Elets BFSI |
| Feb 2026 | Aman Goel speaks at AI Impact Summit Delhi on AI's impact on jobs | YouTube/N18S |

**Velocity verdict:** Accelerating. Company went from 7 clients at seed (June 2024) to 50+ at Series A (October 2025) in 16 months — roughly 7x client growth. Landed marquee BFSI names (SBI Life, ICICI Pru, Motilal Oswal) within 18 months of founding. Series A at 18 months is fast for enterprise B2B. However, the revenue base (₹3.81 Cr FY25) is still pre-product-market-fit scale — the Series A is essentially a bet on the Voice AI Agents product category that launched in late 2025. The next 12 months (FY26) will be the real proof point.

## 11. Bull Case / Bear Case
**Bull:** Founding team has a rare combination of domain expertise (Cogno AI exit, 2 years inside Exotel), existing BFSI relationships, and technical depth. BFSI is the highest-compliance vertical in India, creating natural lock-in once integrated. India's BFSI sector is digitizing rapidly with 1.4 billion potential end-customers. Data flywheel from 50+ institutions processing hundreds of millions of calls compounds their STT/LLM accuracy advantage every month. Elevation Capital + Z47 backing provides smart money with BFSI network. If Voice AI Agents reaches $10M ARR by FY27, the company is on a trajectory to be the de facto BFSI voice infrastructure in India.

**Bear:** FY25 revenue of $450K is tiny for a company claiming to process hundreds of millions of conversations — raises questions about conversion rates from analytics to paid contracts, or pricing adequacy. Latka's "$11M revenue" claim is likely aspirational or based on unverified self-reporting. Uniphore ($600M raised) can accelerate India-specific BFSI products with far greater capital. Sarvam AI or an AI4Bharat-backed initiative could open-source competitive Indic voice models, eroding the STT moat. Regulatory risk: if RBI tightens AI-in-collections rules (a live policy area), the core collections-call automation use case faces restriction. Six co-founders with overlapping network from Cogno AI raises governance and dilution risks at later stages.

## 12. What I Couldn't Find
- Post-money valuation at Series A (not officially disclosed; third-party estimates conflict: $33M Latka vs ₹430 Cr/$51.8M Tracxn)
- Exact headcount (4 different figures in circulation: 49, 71, 80+, 44)
- Specific Indic languages supported beyond Hindi/English/Hinglish
- Latency metrics (TTFB, RTF) for Voice AI Agents
- Voice cloning capabilities or TTS voice count
- Detailed pricing structure for Voice AI Agents
- Any arXiv/academic publications
- GitHub or Hugging Face presence (none found)
- Bhashini / AI4Bharat / ONDC integration (none found)
- DPDPA compliance certification or security audits
- Specific CRM or telephony integration list beyond Cisco/Avaya mention
- Board composition or formal advisors beyond investors
- Details on Seed Round 2 (July 2024) — amount and investors not disclosed

## Sources
1. https://entrackr.com/news/greylabs-ai-raises-rs-85-cr-led-by-elevation-to-launch-voice-ai-agents-for-bfsi-10532249
2. https://z47.com/news/greylabs-ai-raises-85-crores-series-a-to-redefine-voice-ai-in-indias-bfsi-sector
3. https://z47.com/news/greylabs-ai-raises-over-1-5m-led-by-matrix-partners-india
4. https://z47.com/zerotoinfinity/meet-the-founders-of-greylabs-ai
5. https://www.elevationcapital.com/perspectives/greylabs-ai-building-voice-ai-for-india-banks
6. https://ibsintelligence.com/ibsi-news/greylabs-ai-raises-over-1-5m-in-seed-round-led-by-matrix-partners-india/
7. https://inc42.com/buzz/greylabs-ai-nets-inr-85-cr-to-automate-customer-care-centres/
8. https://inc42.com/startups/why-this-ai-startup-is-the-secret-weapon-for-next-level-customer-insights/
9. https://inc42.com/buzz/greylabs-ai-to-raise-funding-from-elevation-z47-partners/
10. https://tracxn.com/d/companies/greylabs/__5fLG9ro-_L1FISIyUzQKZIT6rnGh071t9ZzZTBxs4BM
11. https://thetechportal.com/2025/10/06/greylabs-ai-gets-10-2mn-in-latest-fundraise-to-scale-voice-ai-for-banking-and-finance/
12. https://bfsi.eletsonline.com/greylabs-ai-secures-series-a-funding-to-accelerate-ai-led-bfsi-transformation/
13. https://bfsi.eletsonline.com/neysa-partners-with-greylabs-ai-to-deliver-enterprise-scale-voice-insights-for-bfsi/
14. https://www.tribuneindia.com/news/business/neysa-and-greylabs-ai-collaborate-to-bring-complete-voice-coverage-compliance-insight-and-conversion-at-enterprise-scale
15. https://apacnewsnetwork.com/2025/10/greylabs-ai-raises-rs-85-cr-in-series-a-funding-to-enhance-ai-led-bfsi-capabilities/
16. https://www.siliconindia.com/startup/startup-funding/greylabs-ai-raises-rs-85-crore-to-scale-voice-ai-in-bfsi-nwid-51490.html
17. https://indianstartupnews.com/funding/speech-analytics-platform-greylabs-raises-seed-funding-led-by-matrix-partners-india-others-4766882
18. https://getlatka.com/companies/greylabs.ai
19. https://www.amangoel.in/2022/12/my-journey-of-building-cogno-ai-right.html
20. https://in.linkedin.com/in/goel-aman (Aman Goel LinkedIn)
21. https://www.linkedin.com/in/harshita-srivastava-78961285/ (Harshita Srivastava LinkedIn)
22. https://www.linkedin.com/in/sg-patel/ (Shreyas Patel LinkedIn)
23. https://www.linkedin.com/in/rajsanghavi/ (Raj Sanghavi LinkedIn)
24. https://www.youtube.com/watch?v=7G9A_SSTr20 (Founder Moments / Z47 podcast)
25. https://www.youtube.com/watch?v=Tcwr7D3C3H0 (A Billion Conversations podcast)
26. https://www.youtube.com/watch?v=3vFpZeoWM58 (AI Impact Summit Delhi, Feb 2026)
27. https://yourstory.com/ai-story/greylabs-ai-raises-rs-85-crore-to-scale-its-voice-agentic-platform-bfsi
28. https://yourstory.com/companies/greylabs-ai
29. https://www.menlotimes.com/post/mumbai-based-greylabs-ai-is-innovating-bfsi-services-through-agentic-voice-ai
30. https://techstory.in/greylabs-ai-raises-%E2%82%B985-crore-to-supercharge-voice-ai-in-bfsi/
31. https://www.entrepreneur.com/en-in/news-and-trends/greylabs-ai-secures-inr-85-cr-to-strengthen-voice-ai/497955
32. https://pitchbook.com/profiles/company/606289-33
33. https://www.cbinsights.com/company/greylabs-ai
34. https://greylabs.ai/about
35. https://www.greylabs.ai/blog
36. https://www.greylabs.ai/products/speech-analytics
37. https://www.greylabs.ai/privacy-policy
38. https://www.glassdoor.co.in/Reviews/GreyLabs-AI-Reviews-E9832631.htm
39. https://wellfound.com/company/greylabs-ai
40. https://www.instahyre.com/jobs-at-greylabs-ai/
41. https://startupstorymedia.com/insights-greylabs-ai-raises-over-1-5-million-in-seed-funding-led-by-matrix-partners-india/
42. https://incubees.com/speech-analytics-startup-greylabs-ai-raised-over-1-5-m-from-matrix/
