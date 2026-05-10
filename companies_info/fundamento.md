# Fundamento

**Website:** https://fundamento.ai  •  **HQ:** New Delhi, India (SF registered address for US entity)  •  **Founded:** 2020  •  **Stage:** Pre-Series A
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): Agentic AI voice platform purpose-built for India's lending and BFSI contact centers, automating the full borrower lifecycle from lead qualification through debt collections in 30+ languages.
- Total funding to date: ~$3.46M USD (claimed: $3.67M across 8 rounds per Tracxn, including non-cash grants)
- Last round: $1.9M pre-Series A, October 18 2025, led by IIFL Fintech Fund
- Headcount: 52 (as of March 31 2026 per Tracxn); Crunchbase lists 11–50 range; LinkedIn not directly verified
- Revenue / ARR: ₹4.13 Cr (~$495K) annual revenue as of FY March 2025 (source: Tracxn financial data); FY2023 showed 235% YoY revenue growth (per Skillr Talent MCA filing)

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| Nov 26, 2020 | Pre-Seed / Seed | ~$1.2M (as Skillr) | Binny Bansal (Flipkart co-founder) | Caesar Sengupta (ex-Google VP / Arta Finance co-founder), Kunal Shah (CRED founder), Arun Seth (NASSCOM Chairman), Amrish Rau (Pine Labs CEO), Let's Venture, Gaurav Girotra (GM SEA, Tinder/Match Group), Karan Khara (Meta), Pushpendra Singh (Meta), Bryan Tan (Meta) | Entrepreneur India, Business Standard (Dec 17 2021 announcement) |
| Dec 8, 2023 | Grant | $100K (est.) | Google for Startups Women Founders Fund APAC | — | Crunchbase, Tracxn |
| Aug 2024 | Seed | Undisclosed | Epic Angels | — | Tracxn |
| Mar 31, 2024 | Angel | Undisclosed | Undisclosed angels | — | Tracxn |
| Oct 18, 2025 | Pre-Series A (labelled "Seed" by Crunchbase) | $1.9M (₹~16 Cr) | IIFL Fintech Fund | The Players Fund (backed by cricketers KL Rahul & Ben Stokes), Venture Catalysts, Lead Invest, Epic Angels, additional angel investors | Entrackr, Indian Startup News, CEO's of Bharat |

**Notes:**
- The $1.56M "seed" figure cited by some sources appears to aggregate pre-seed + Google grant, not a single round.
- Tracxn reports $3.67M across 8 rounds including very small/undisclosed tranches; the three cleanly verifiable cash rounds total ~$3.1M.
- No Y Combinator involvement found; the initial research prompt mentioned YC but no evidence was found across Crunchbase, YC company directory, or any news sources.
- Post-money valuation: Not publicly available (Tracxn masks it).

## 3. Product & Customers
### Products
Fundamento operates a single unified **AI Voice Agent Platform** marketed under the Fundamento brand, with the following layers:

- **Agentic AI Voice Bot** — end-to-end telephony automation for the lending lifecycle (lead qualification → loan discovery → EMI reminders → collections). Claimed 24/7, zero wait time, no human required for standard flows.
- **Dialecto** — proprietary speech recognition module handling regional Indian accents and noisy telephony environments (claimed; no published benchmarks found).
- **Hybrid Workflows** — rule-based escalation overrides and hot-transfer to live agents; configurable LLM selection ("bring your own LLM" architecture per product page).
- **Analytics Dashboard** — real-time conversation-level KPIs: repayment rates, conversion, drop-offs, fraud/delinquency signals, borrower sentiment.
- **Multi-agent Orchestration** — autonomous coordination across voice, chat, and back-office APIs (positioned as "agentic AI" capability added ~2024–2025).

Earlier (2021–2022) the company operated as **Skillr** — an HR-tech behavioral skills assessment and upskilling SaaS. The pivot to voice AI contact centers happened in early 2023 and the Fundamento brand was adopted mid-2023.

### Pricing
Not publicly disclosed. Enterprise custom pricing model inferred from product positioning. No pricing page on website (verified 2026-05-10). Industry comparables for similar platforms range from per-minute ($0.05–$0.15/min) to outcome-based models.

### Languages & Voices
- **Claimed:** 30+ languages
- **Verified in sources:** Hindi, English, and other major Indian languages implied by BFSI deployments; specific language list not published on website.
- No published voice/speaker count or TTS model specifications found.
- Code-switching (Hinglish) support implied by BFSI use cases.

### Named Customers
| Customer | Relationship | Evidence |
|----------|-------------|---------|
| Hero FinCorp | Active client (NBFC) | APAC News Network, Nov 2024 announcement |
| IIFL (NBFC/fintech) | Active client AND investor (IIFL Fintech Fund) | Multiple news sources |
| Paisabazaar | Active client (fintech marketplace) | Multiple sources (also mentioned as early customer 2023) |
| Indiamart | Early customer (B2B marketplace) | Inc42 "30 Startups to Watch" 2023 |
| Disney+ Hotstar | Early customer | Inc42 "30 Startups to Watch" 2023 |

**Notes:** Indiamart and Disney+ Hotstar appear to be from the Skillr/pre-pivot era (2022–2023 agent assist use case). Current BFSI focus customers are Hero FinCorp, IIFL, Paisabazaar. No published case study URLs found.

### Integrations / SDKs
- **Telephony:** Enterprise SIP trunks and dialer support
- **CRM:** CRM tools (unnamed; generic mention on website)
- **LOS:** Loan origination systems
- **CPaaS:** CPaaS platforms (unnamed)
- **Back-office:** REST APIs for real-time data exchange
- No public SDK, developer docs, or API reference found.
- **Strategic partnerships:** Align AI (analytics/LLM evaluation, announced July 4 2024; both Google for Startups alumni)

## 4. Technical Architecture
### Model approach
- **Flexible/agnostic LLM backend:** Product page explicitly states "select from a range of LLMs to ensure smarter, more accurate responses" — implying BYOLLM or a multi-model router.
- **Vertical fine-tuning claimed:** "Domain-specific vertical models" for BFSI/lending (claimed in Oct 2025 funding release; no model cards or benchmarks published).
- **Multi-agent orchestration:** Multiple specialized agents coordinating across borrower interaction workflows.
- **Enterprise AI safeguards:** Rule-based overrides described as eliminating hallucinations in compliance-critical flows.

### Training data
Not publicly disclosed. Given the BFSI focus and Hindi/regional language support, likely uses a mix of:
- Proprietary contact center call recordings from enterprise clients
- Public Indic ASR datasets (AI4Bharat IndicConformer, IndicVoices) — unconfirmed
No published training data card or dataset disclosures found.

### Latency profile
Not publicly disclosed. No TTFB, RTF, or streaming latency benchmarks published. Platform marketed as "real-time" and suitable for live telephony.

### Voice cloning
No voice cloning feature mentioned in product materials. Not positioned as a TTS or voice synthesis company.

### Prosody / emotion control
- Sentiment-aware responses: "detects and adapts to borrower emotions" (product page, claimed)
- Multi-turn context retention described
- No technical detail on prosody control, SSML support, or emotion classification methods

### Indic language strategy
- 30+ language claim covers major Indian scheduled languages
- **Dialecto** is described as handling regional accents and noisy environments — suggests custom ASR layer, possibly fine-tuned on top of Whisper or AI4Bharat models (unconfirmed)
- No Bhashini, AI4Bharat, or ONDC integration publicly announced
- No government-tender or regulatory framework (RBI NBFC guidelines) compliance documentation found publicly

### Inference stack
- Deployment options: On-premises, hybrid, private cloud (all three offered)
- No mention of on-device / edge inference
- High enterprise concurrency claimed (no numbers)
- SOC II and ISO 27001 certified (claimed on website; no certificate links)

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| "Harnessing the Power of Behavioral Skills: Hello Fundamento!" | Blog (Medium) | ~2023 | https://medium.com/skillr-ai/harnessing-the-power-of-behavioral-skills-hello-fundamento-9bc1337df160 |
| Ankit Durga at YourStory TechSparks 2023 | Video talk | Sep 2023 | https://www.youtube.com/watch?v=gGb0cRxPuR0 |
| "Fundamento AI Announces Global Strategic Partnership with Align AI" | Press release | Jul 4, 2024 | https://www.cioandleader.com/fundamento-ai-announces-global-strategic-partnership-with-align-ai-to-revolutionize-contact-center-automation/ |
| "Fundamento Welcomes Vickram Saigal as Co-Founder" | Press release | Nov 23, 2024 | https://www.apnnews.com/fundamento-welcomes-vickram-saigal-as-co-founder-to-drive-product-and-technology-innovation/ |

No arXiv papers, HuggingFace model cards, or engineering blog posts found.

## 5. Open Source Footprint
### GitHub
| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| — | — | — | — | — | No GitHub organization found for "fundamentoai" or "fundamento-ai" (verified via GitHub API 2026-05-10) |

### Hugging Face
| Model | Downloads | Likes | License |
|-------|-----------|-------|---------|
| — | — | — | — |

No HuggingFace presence found for Fundamento.

### Top contributors
No public open-source contributions identified.

**Summary:** Fundamento has no open-source footprint. It is a closed-source enterprise SaaS. No community signals found on GitHub, HuggingFace, or developer forums.

## 6. Team
### Founders
| Name | Title | Background |
|------|-------|-----------|
| **Ankit Durga** | Co-Founder & CEO | Alumnus of Harvard Executive Program (Strategic Nonprofit Management), INK Fellow. Ex-Ernst & Young (Risk Advisory). Founded Skillr (Fundamento's predecessor) and Leap Skills Academy (trained 200K+ young Indians in behavioral skills). Shaheed Sukhdev College of Business Studies, Delhi University. ~10+ years in skilling sector before pivoting to AI. |
| **Megha Aggarwal** | Co-Founder | Ex-Investment Banking Analyst/Associate at Morgan Stanley, New York (2005–2009). Skill Development Expert with Asian Development Bank and Ministry of HRD (2009–2013). Founded and served as CEO of LEAP Skills Academy (trained 50,000+ young Indians). Second-time founder with Ankit Durga. |
| **Vickram Saigal** | Co-Founder & Head of Product/Technology | Joined as Co-Founder November 23, 2024 (company's 4th anniversary). MBA from University of Chicago Booth School of Business. Ex-Adobe (SF), SaaS Labs (New Delhi), Bain & Company, Gates Foundation, IDEO.org, Upaya Social Ventures. Product strategy and innovation specialist. |

### Key technical hires
| Name | Title | Notes |
|------|-------|-------|
| Khushil Khatri | Engineering Manager | Per company page |
| Snehal Agrawal | Engineering Manager | Per company page |
| Geetika Khanna | Product Manager | Per company page |

### Recent joiners (last 12mo)
- **Vickram Saigal** — Co-Founder (joined November 2024, announced publicly)
- **Anand Kartikeyan** — President, Sales (Bengaluru-based; role confirmed via ZoomInfo/LinkedIn, timing of join unclear)
- **Eshani Jain** — VP Customer Success (timing unclear)
- **Iknoor Kaur** — VP Solutioning (timing unclear)
- **Prapurna Sharma** — Chief of Staff (also listed as primary contact on website)

### Notable departures (last 12mo)
Not publicly available. No departure news found.

### Open roles signal
No careers page found at fundamento.ai/careers (404). A Customer Success Associate role for New Delhi was posted on Foundit.in (date unclear). Company at 52 headcount is in a moderate hiring phase; open roles in engineering and customer success expected given $1.9M raise (Oct 2025).

## 7. Moat & Defensibility
- **Data moat:** Moderate. Proprietary call recordings from BFSI enterprise deployments (Hero FinCorp, IIFL, Paisabazaar) with lending-domain annotations create a feedback loop. However, with only ~$3.5M raised and 52 employees, data volume is limited compared to players like Uniphore or Skit.ai. The RBI-compliance and NBFC-specific conversation patterns are a genuine differentiator for India.
- **Model moat:** Weak–Moderate. Dialecto (accent-robust ASR) and claimed domain-specific vertical models are proprietary, but no published benchmarks exist. LLM-agnostic architecture means core AI is not proprietary. Competitors can build similar fine-tunes with comparable BFSI data.
- **Distribution moat:** Moderate. IIFL is simultaneously an investor AND customer — classic strategic alignment. Hero FinCorp, Paisabazaar relationships provide reference leverage for NBFC/fintech sales. Align AI partnership adds LLM evaluation differentiation. No telco, Bhashini, ONDC, or government-tender integrations found.
- **Brand / community moat:** Low. No developer community, no open source, minimal press coverage outside funding news. Nasscom AI Gamechangers recognition (2023–2024) and Asia Stevie Silver Award (2024, "Powering Contact Centers of the Future") provide modest credibility. YourStory TechSparks 2023 speaker slot raised profile modestly.
- **Regulatory moat:** Low–Moderate. RBI-compliant AI for collections is a genuine barrier (consent management, do-not-disturb compliance, time-of-call restrictions for debt collection). SOC II + ISO 27001 certifications help enterprise procurement. Not yet verifiably integrated with Bhashini or DPDP (India's new data protection law) compliance frameworks.
- **Replication cost (6mo, $10M competitor):** A well-funded competitor with access to Indic ASR (via AI4Bharat/Sarvam) and a modern LLM stack could replicate the product layer in ~6 months for ~$2–3M. The remaining moat is customer relationships and BFSI-specific training data — replicable but time-consuming. Estimate: ~12–18 months to reach parity with Fundamento's current deployment depth.
- **Moat strength: 2/5** — Narrow, domain-specific distribution moat in India BFSI lending collections, but limited by small scale, no open-source community, no published model benchmarks, and well-funded competitors.

## 8. Risks & Problems
### Technical complaints
No public technical complaints found on Reddit, Hacker News, Twitter/X, or GitHub Issues (as of 2026-05-10). This is likely due to low public profile rather than absence of issues. The absence of public benchmarks for Dialecto or multilingual accuracy makes independent validation impossible.

### Pricing pain points
Pricing not publicly disclosed; no public complaints. Enterprise-only model with no self-serve tier creates a long sales cycle risk for a seed-stage company.

### Safety / misuse
- Debt collections automation carries inherent risk of perceived harassment if agents are poorly calibrated for tone/compliance.
- RBI regulations on AI-driven collections communications are evolving; mis-steps could trigger regulatory scrutiny.
- No published red-teaming or AI safety documentation found.
- "Eliminating hallucinations" through rule-based overrides is claimed but not independently verified.

### Legal / regulatory
- **DPDP Act (India's Digital Personal Data Protection Act 2023):** Collection and processing of borrower voice data requires consent frameworks. Fundamento's on-prem/hybrid deployment option partly mitigates this, but compliance posture not publicly documented.
- **RBI Fair Practices Code for NBFCs:** AI agents making collections calls must comply with timing restrictions and consent requirements. No public documentation of RBI-specific compliance stack.
- No litigation found.

### Churn signals
- The pivot from HR-tech (Skillr) to voice AI in 2023 means early customers like Indiamart and Disney+ Hotstar likely churned when the product pivoted. Core BFSI customers (Hero FinCorp, IIFL, Paisabazaar) appear to be retained as of 2025 funding announcement.
- Revenue of ₹4.13 Cr (~$495K) on $3.5M+ total raised implies high burn relative to revenue; not yet profitable.

## 9. Competitive Position
- **Direct competitors:**
  - *Gnani.ai* (Bengaluru; BFSI-focused voice AI, multilingual, telco+BFSI, more established)
  - *Skit.ai* (rebranded Observe.AI India, BFSI collections specialist)
  - *Uniphore* ($985M raised, $2.5B valuation; global conversational AI giant)
  - *Haptik* (Reliance-backed, conversational AI)
  - *Yellow.ai* (Series C, omnichannel conversational AI)
  - *Convin.ai*, *SquadStack*, *Mihup.ai* (India-focused contact center AI)
  - *Sarvam AI* (Bengaluru; sovereign Indic AI with TTS/ASR stack; could commoditize Fundamento's language layer)
  - *Smallest.ai*, *Bolna AI* (lower-cost voice agent builders targeting similar market)

- **Where it's winning:**
  - Lending-specific depth: Collections + origination + upselling in one platform tailored for NBFC/bank workflows
  - Flexible deployment (on-prem/hybrid) which matters for data-sensitive BFSI clients
  - Strategic investor-customer overlap (IIFL) that accelerates enterprise land-and-expand
  - Founder credibility in India skilling/BFSI sector enabling trust-based enterprise sales

- **Where it's losing:**
  - Scale: 52 employees vs Uniphore (1000+), Yellow.ai (500+)
  - Funding: $3.5M total vs competitors with $50M–$985M raised
  - Open ecosystem: No developer platform, no API marketplace, no community
  - Geographic: Pure India play (US/APAC expansion is aspirational, not yet demonstrated)
  - Model benchmarks: No published accuracy/latency claims that can be cited in enterprise procurement

## 10. News & Momentum (last 12 months)
| Date | Event | Source |
|------|-------|--------|
| Jul 4, 2024 | Strategic partnership with Align AI for contact center analytics | CIO & Leader |
| Nov 23, 2024 | Vickram Saigal joins as Co-Founder (CPO equivalent) | APN News, APAC News Network |
| Oct 18, 2025 | $1.9M pre-Series A led by IIFL Fintech Fund; The Players Fund (KL Rahul/Ben Stokes), Venture Catalysts, Lead Invest, Epic Angels | Entrackr, Indian Startup News, Entrepreneur India, CEO's of Bharat, MarcaMoney, multiple |
| 2023–2024 | Nasscom AI Gamechangers Award (Innovator Startup category) | Nasscom website |
| May 24, 2024 | Silver Stevie Award (Asia-Pacific) — "Powering Contact Centers of the Future" | Stevie Awards website |

**Velocity verdict:** Slow but positive. One meaningful funding event in the last 12 months plus one senior co-founder hire signals steady progress, not hypergrowth. The $1.9M raise is modest for the market; the involvement of IIFL as lead investor (who is also a customer) is the most strategically significant signal. Press coverage is clustered around funding announcements with minimal organic thought-leadership.

## 11. Bull Case / Bear Case
**Bull:**
India's NBFC/lending sector is under-automated; millions of collections and EMI-reminder calls happen daily through human agents. Fundamento has 4+ years of domain expertise, live enterprise deployments, an investor-customer flywheel with IIFL, and a flexible deployment model that works for data-paranoid banks. If they close 2–3 more marquee BFSI logos and raise a proper Series A ($8–15M), they can build a defensible niche as the go-to AI collections layer for Indian lending. The 30+ language claim and on-prem option are genuine enterprise differentiators in a regulated market. India's BFSI AI market is projected to grow 10X+ by 2033.

**Bear:**
$495K revenue and $3.5M raised after 5 years suggests the pivot from HR-tech to voice AI has been slow to scale. Sarvam AI's TTS/ASR stack commoditizes the Indic language layer; Gnani.ai and Skit.ai are larger and more established in the same market. IIFL's dual role as investor and customer creates governance concerns. The absence of a developer platform, open API, or benchmark data makes enterprise procurement harder. A larger player (Uniphore, Yellow.ai, or a Sarvam-backed startup) could out-resource Fundamento in 18 months. International expansion (US, APAC) with $1.9M is aspirational at best.

## 12. What I Couldn't Find
- Exact CIN for the US entity (Indian entities confirmed: SKILLR TECHNOLOGIES PVT LTD — U80903DL2020PTC370929, and SKILLR TALENT PVT LTD — U72501DL2021PTC391513)
- Specific language list (which 30+ languages are supported, and with what quality)
- Published latency benchmarks (TTFB, RTF, streaming performance)
- Dialecto technical specifications or published accuracy
- Headcount 6 months ago (to compute delta) — LinkedIn gating prevents verification
- Any ARR/MRR breakdowns or named customer contract values
- GitHub, HuggingFace, or any public technical repository
- Bhashini, AI4Bharat, ONDC, or govt-tender integration — none found
- Y Combinator connection — claimed in research brief but no evidence found across any source
- Full investor list for the Aug 2024 seed round and Mar 2024 angel round
- Pricing page or any publicly stated pricing
- G2/Capterra reviews (403 access errors; no reviews surfaced in search)
- Any published safety, red-teaming, or compliance documentation

## Sources
1. https://fundamento.ai/ — Official homepage (fetched 2026-05-10)
2. https://fundamento.ai/company-page/ — Company/About page (fetched 2026-05-10)
3. https://fundamento.ai/product-page/ — Product details (fetched 2026-05-10)
4. https://indianstartupnews.com/funding/agentic-ai-platform-fundamento-raises-19-million-in-funding-led-by-iifl-fintech-fund-others-10575994 — Oct 2025 funding news
5. https://entrackr.com/snippets/fundamento-raises-19-mn-led-by-iifl-fintech-fund-10574244 — Entrackr funding report
6. https://tracxn.com/d/companies/fundamento/__uWz1eOFoxj0DK9MDXy6GsbGej9STjwrKAREy8pkmkZ0 — Tracxn company profile (headcount 52, revenue ₹4.13 Cr, funding history)
7. https://tracxn.com/d/companies/fundamento-ai/__uWz1eOFoxj0DK9MDXy6GsbGej9STjwrKAREy8pkmkZ0/funding-and-investors — Tracxn funding details (429 error on fetch; data extracted from search results)
8. https://ceosofbharat.com/ai-startup-fundamento-raises-1-9-million-to-transform-lending-and-collections-for-financial-services/ — Oct 2025 funding, investor list
9. https://ascendants.in/business-stories/fundamento-ai-1-9mkl-rahul-ben-stokes/ — Players Fund investment rationale
10. https://india.entrepreneur.com/news-and-trends/fundamento-secures-usd-19-mn-in-pre-series-a-funding-led/498513 — Entrepreneur India funding report
11. https://india.entrepreneur.com/finance/skillr-raises-1-2-million-in-pre-seed-round/403367 — Skillr $1.2M pre-seed Dec 2021
12. https://www.business-standard.com/article/companies/hr-tech-start-up-skillr-raises-1-2-mn-from-binny-bansal-kunal-shah-121121401022_1.html — Business Standard pre-seed (403 error; data from search results)
13. https://www.apnnews.com/fundamento-welcomes-vickram-saigal-as-co-founder-to-drive-product-and-technology-innovation/ — Vickram Saigal announcement (403 error; data from APAC News Network and search)
14. https://apacnewsnetwork.com/2024/11/vickram-saigal-joins-fundamento-as-co-founder-to-propel-tech-innovation/ — Saigal background
15. https://www.companydetails.in/company/skillr-technologies-private-limited — MCA data for Skillr Technologies (CIN U80903DL2020PTC370929)
16. https://www.thecompanycheck.com/company/skillr-talent-private-limited/U72501DL2021PTC391513 — MCA data for Skillr Talent (CIN U72501DL2021PTC391513)
17. https://www.cioandleader.com/fundamento-ai-announces-global-strategic-partnership-with-align-ai-to-revolutionize-contact-center-automation/ — Align AI partnership Jul 2024
18. https://medium.com/skillr-ai/harnessing-the-power-of-behavioral-skills-hello-fundamento-9bc1337df160 — Skillr→Fundamento rebrand story
19. https://www.crunchbase.com/organization/skillr — Crunchbase profile (403 error; data from search results)
20. https://asia.stevieawards.com/2024-stevie-winners — Stevie Award Silver 2024
21. https://nasscom.in/ai-gamechangers/ — Nasscom AI Gamechangers award reference
22. https://blog.google/around-the-globe/google-asia/new-ai-women-fund/ — Google Women Founders Fund APAC (Fundamento not named but confirmed as recipient by Tracxn/Crunchbase)
23. https://www.marcamoney.com/fundamento-raises-1-9-million-in-pre-series-a-funding-led-by-iifl-fintech-fund/ — Oct 2025 funding
24. https://startupnews.fyi/2025/10/18/fundamento-raises-1-9-mn-led-by-iifl-fintech-fund/ — Oct 2025 funding
25. https://www.youtube.com/watch?v=gGb0cRxPuR0 — Ankit Durga at YourStory TechSparks 2023
26. https://www.zoominfo.com/p/Anand-Kartikeyan/1248784532 — Anand Kartikeyan President Sales
27. https://in.linkedin.com/in/anandkartikeyan — Anand Kartikeyan LinkedIn
28. https://deccanfounders.com/2025/18/short-news/fundamento-raises-1-9m-pre-series-a-to-enhance-its-agentic-ai-for-financial-services-focusing-on-collections-upselling-and-borrower-profiling/ — Oct 2025 round detail
29. https://app.fundz.net/fundings/fundamento-funding-round-3f821c — Fundz funding record
30. https://inshorts.com/en/news/kl-rahul--ben-stokes-support-india-s-ai-fintech-rise-1760778162543 — Players Fund context
