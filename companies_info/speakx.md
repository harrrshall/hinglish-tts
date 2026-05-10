# SpeakX

**Website:** https://speakx.ai  •  **HQ:** Gurugram (Sector 47), Haryana, India  •  **Founded:** 2020 (as Yellow Class) / rebranded to SpeakX 2023  •  **Stage:** Pre-Series B
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): AI-powered spoken English confidence app for 400M+ aspiring English speakers in India's Tier 2/3 towns, delivered at ₹299/month via Google Gemini-powered roleplay and real-time speech coaching.
- Total funding to date: ~$23.3 M (₹~209 Cr) across 3 disclosed rounds
- Last round: $16 M Pre-Series B, October 14 2025, led by WestBridge Capital
- Headcount: ~27 (per MCA filings, March 2026); ~20–22 per LinkedIn/PitchBook snapshots (mid-2025); was ~67 in 2024 before lean restructuring
- Revenue / ARR: ARR ~$7.5 M (claimed, Oct 2025); MCA shows FY2024-25 revenue ₹9.63 Cr (~$1.15 M at current rates — likely partial-year or different accounting period); EBITDA-positive since April 2025; ~$150 K/month profit; $1 M cumulative EBITDA over five months to Oct 2025

> **Conflict note:** ARR of $7.5 M and MCA revenue of ₹9.63 Cr (~$1.15 M) differ significantly. The $7.5 M figure likely reflects annualised run-rate GMV or deferred cash; the MCA number is accrual-basis revenue recognised for FY2024-25 only through a partial year. Treat $7.5 M as claimed/unaudited.

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| Nov 26, 2020 | Seed | ~$1.3 M | India Quotient | — | Crunchbase, Tracxn |
| Aug 17, 2021 | Series A | $6 M | Elevation Capital | India Quotient (follow-on), angels incl. Vidit Aatrey (Meesho), Dhruv Agarwala (PropTiger) | Entrackr, Inc42 |
| Oct 14, 2025 | Pre-Series B | $16 M (₹~142 Cr) | WestBridge Capital | Elevation Capital (existing), Goodwater Capital, Breadlake Ventures; angels: Shyamal Anadkat (OpenAI), Ronnie Screwvala (upGrad), Charles Songhurst, Ashish Jain, Siddharth Kohli | YourStory, Entrackr, Inc42, Entrepreneur India |
| **Total** | | **~$23.3 M** | | | |

**Post-money valuation:** ~$50 M (estimated from MCA CCPS filings per Inc42); one source cited $66 M — figure not confirmed by company. Pre-Series B raised at ₹26.24 Cr first tranche (42,974 CCPS).

**ESOP buyback:** $1 M buyback announced November 2025 for 15 of 20 employees (team collectively holds 6% equity).

## 3. Product & Customers

### Products
1. **SpeakX App (B2C)** — AI spoken English practice app. Core loop: 15-minute daily sessions with an AI conversation partner that gives real-time pronunciation, grammar, and fluency feedback. Features:
   - Personal AI Teacher / 24/7 AI companion
   - Interactive speaking lessons (roleplay scenarios: job interviews, workplace chats, restaurant orders, medical consultations)
   - Real-time pronunciation and grammar feedback
   - Adaptive difficulty based on proficiency assessment
   - Gamification: streaks, badges, leaderboards, daily challenges
   - Progress tracking and monitoring reports
   - Olympiads and contests
   - Bilingual interface (English explained through Hindi)
   - Five-step skill progression milestones
   - Curriculum designed in collaboration with "IIT/IIM experts" (claimed; not independently verified)
   - Available on: Google Play (`yellowclass.kids.live`), iOS App Store (App ID `6756059415`, last updated Feb 10, 2026, v5.4.3)
   - Free with in-app purchases; 148.1 MB

2. **SpeakX Business (B2B)** — Enterprise / institutional version for corporate training. Named customer: Cloudnine Hospital (nurses English communication program, Nov 2024). Also references partnerships with "local educational institutions" and "corporate training programs." No dedicated pricing page found publicly.

### Pricing
- **Free tier:** Available (limited features)
- **Monthly subscription:** ₹299/month (~$3.60 USD) — stated across multiple sources
- **Premium range:** ₹99–₹299/month per iOS App Store listing (suggesting multiple tiers or promotional pricing)
- No annual plan pricing found publicly

### Languages & Voices
- **Teaching language (UI):** Hindi (primary), with planned expansion to Telugu, Tamil, Marathi, Bengali
- **Learning target language:** English
- **Accent support:** ASR trained on voices from across Indian regions, Hinglish code-mixed inputs handled
- **Language count:** 1 target (English) as of May 2026; regional UI languages expanding
- No custom voice cloning or multi-voice selection advertised

### Named Customers
| Customer | Segment | Case | Source |
|----------|---------|------|--------|
| Cloudnine Hospital | Healthcare / BFSI | English training for nurses (Nov 2024) | APN News, BusinessReviewLive |
| "Local educational institutions" | Edtech | Unnamed | Adgully interview |
| "Corporate training programs" | Enterprise | Unnamed | Adgully interview |

### Integrations / SDKs
- Built on **Flutter** (cross-platform mobile; confirmed by GitHub org repos)
- Payment: **Razorpay** (confirmed by GitHub fork `razorpay-flutter-custom_ui_v1`)
- Analytics: **PostHog** (confirmed by GitHub fork)
- Video: **BetterPlayer** (confirmed by GitHub fork)
- Speech-to-text: `speech_to_text` Flutter package (BSD-3-Clause, GitHub)
- Cloud infrastructure: **Google Cloud Platform** (confirmed by CEO — "Google is now at cutting edge")
- AI/LLM: **Google Gemini** (primary model for most operations; CEO confirmed)
- No public API / SDK offered to third parties as of research date

## 4. Technical Architecture

### Model approach
SpeakX is a consumer-facing **application layer** built on top of third-party foundation models — not a model builder. The company deliberately chose not to train custom LLMs. Key technical choices (per CEO Arpit Mittal in Inc42 interview):
- **Primary LLM:** Google Gemini (shifted from mixed-model architecture; Gemini used for most generative operations)
- **Infrastructure:** Google Cloud Platform (GCP) — "with minimal human intervention"
- **Multi-model strategy:** Switches between models for specific use cases; Gemini used for orchestration
- **Speech recognition (ASR):** Custom-trained or fine-tuned on Indian regional accent datasets — "datasets featuring voices from across Indian regions to handle regional accents, code-mixed language (Hinglish), and dialect variations"
- **Personalization:** Adaptive engine adjusting content difficulty and feedback based on individual performance patterns
- **Automation:** Onboarding, engagement, and learning workflows fully automated (20-person team, zero human tutors)

### Training data
- ASR fine-tuned on multi-accent Indian voice data (scale not disclosed)
- No public dataset releases
- No evidence of use of Bhashini / AI4Bharat / IndicVoices datasets (not verified either way)
- Curriculum content developed with "IIT/IIM experts" (claimed)

### Latency profile
- Not publicly disclosed
- Sessions described as real-time with "instant feedback" — implies streaming ASR + LLM pipeline
- Mobile-first delivery via GCP

### Voice cloning
- No voice cloning feature advertised or described

### Prosody / emotion control
- Not described in public sources; standard LLM text-to-speech likely used for AI coach voice
- Emphasis on spoken confidence building, not expressive synthesis

### Indic language strategy
- Current: Hindi UI; English-only learning target
- Planned (post Pre-Series B): Telugu, Tamil, Marathi, Bengali UI within 12 months of Oct 2025 funding
- No Bhashini API integration found
- No AI4Bharat model usage documented
- No ONDC or government-tender exposure found

### Inference stack
- Google Cloud Platform (hosting, orchestration)
- Google Gemini API (LLM calls)
- Flutter frontend (Android + iOS)
- Flutter speech_to_text package for client-side STT
- PostHog for product analytics
- Razorpay for payments

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| "A Timely Pivot: How GenAI Allowed SpeakX To Find A New Edtech Mission" | Profile / deep-dive | 2024 | https://inc42.com/startups/a-timely-pivot-how-genai-allowed-speakx-to-find-a-new-edtech-mission/ |
| "This startup uses GenAI to help users fine-tune English…" | Feature | Feb 2025 | https://yourstory.com/2025/02/speakx-startup-genai-help-users-improve-english-skills |
| "How edtech startup SpeakX is using real-time AI to revolutionise English learning in Tier 2, 3" | Interview | 2024 | https://www.adgully.com/post/1688/how-edtech-startup-speakx-is-using-real-time-ai-to-revolutionise-english-learning-in-tier-2-3 |
| "Arpit Mittal on How SpeakX Is Cracking India's English-Speaking Puzzle with AI" | CEO interview | 2024 | https://startuptalky.com/arpit-mittal-speakx-shares-insights/ |

No arXiv papers, conference publications, or HuggingFace model releases found.

## 5. Open Source Footprint

### GitHub
**Org URL:** https://github.com/yellowclass (verified — redirects correctly, description "Personal AI Teacher", website speakx.ai)

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| yc_app_utils | 0 | ~0 | — | Nov 2024 | Archived; Dart utility lib |
| speech_to_text | — | — | BSD-3-Clause | Jan 2026 | Flutter STT plugin |
| grpcurl | — | 576 | MIT | Mar 2026 | Forked from fullstorydev; CLI for gRPC |
| figma-mcp | — | — | — | Mar 2026 | Internal design tooling |
| flutter_tflite | — | — | — | — | Forked; TensorFlow Lite Flutter plugin |
| posthog | — | 2,741 | — | Dec 2025 | Forked from PostHog |
| better_player_plus | — | 1,382 | Apache-2.0 | Sep 2025 | Forked video player |
| razorpay-flutter-custom_ui_v1 | — | 31 | MIT | Sep 2025 | Payments integration |
| in_app_purchase | — | — | BSD-3-Clause | Dec 2025 | App billing |

32 total repos; mostly forks of OSS dependencies. **No proprietary AI model repos, no dataset repos, no research code.** Organization is primarily a Flutter mobile app shop.

### Hugging Face
- **No SpeakX / Ivypods / speakx-ai presence found on Hugging Face** (verified by search; no model cards, datasets, or spaces)

### Top contributors
- **Deepank Agarwal** (CTO / Director of Engineering) — present since Yellow Class founding (2020); leads engineering team of ~17
- No named open-source contributors identified from repos

## 6. Team

### Founders
| Name | Role | Background | Education | GitHub / LinkedIn |
|------|------|-----------|-----------|-------------------|
| **Arpit Mittal** | Founder & CEO | Founded Edcited (2011, acq. by Cocubes 2015); founded Roofpik (prop-tech, acq. by Fastfox.com 2018); launched Yellow Class 2020 (pivot → SpeakX 2023). Personal struggle with English fluency shaped company mission. | B.Tech Electrical, Vellore Institute of Technology (2009) | https://www.linkedin.com/in/arpitmittal4/ |
| **Anshul Gupta** | Co-founder (departed) | Co-founded Yellow Class 2020; stepped down from CEO role when pivot to SpeakX was executed in 2023. Posted LinkedIn update after "4 yrs of founding and building Yellow Class." Background includes prior role at FastFox. | Not publicly disclosed | https://www.linkedin.com/posts/thisisanshulgupta_update-after-an-incredible-4-yrs-of-founding-activity-7093071678032744448-F-AA |

### Key technical hires
| Name | Role | Notes | LinkedIn |
|------|------|-------|---------|
| **Deepank Agarwal** | CTO / Director of Engineering | With company since Yellow Class (2020); grew from software engineer to engineering head; oversees 17-person engineering team; leads Flutter + backend + MLOps | https://www.linkedin.com/in/deepank411/ |
| **Nishtha Agarwal** | Director (Board) | Appointed Oct 26, 2023 per MCA filings; specific technical role not public | Not found |
| **Deepanshi Prabhakar** | — | Listed on LinkedIn as SpeakX.ai team member | https://www.linkedin.com/in/deepanshi-prabhakar-518505148/ |

### Recent joiners (last 12mo)
- Post Pre-Series B (Oct 2025), company stated capital will be used for "hiring senior engineering talent." Specific new hires not publicly disclosed.

### Notable departures (last 12mo)
- **Anshul Gupta** — departed 2023 (pre-12mo window); no departures found in last 12 months of research

### Open roles signal
- Company headcount was ~67 in 2024, contracted to ~20-27 by 2025-26 (likely restructuring from Yellow Class to SpeakX lean model)
- Post-funding hiring planned for engineering; no public job board scraped

## 7. Moat & Defensibility

- **Data moat:** Moderate. Claims 1 Cr+ (10M+) downloads and 1M+ monthly learners generating speech interaction data in Hinglish / Indian-accented English. This accumulation of Indian learner audio data is genuinely scarce and could be used to fine-tune ASR/LLM models. However, the company has not published or commercialised this data moat. Relies on Google's Gemini rather than building proprietary models, so data moat is currently latent, not yet crystallised.
- **Model moat:** Weak. No proprietary model. Entirely dependent on Google Gemini and Google Cloud. Any competitor can replicate the same API stack. The "SpeakX moat" here is UX/curriculum quality and brand, not model.
- **Distribution moat:** Moderate-strong. 10M+ app downloads, 4.6+ star iOS rating (196 ratings), 4.4–4.5 star Play Store rating (~58–74K ratings), strong word-of-mouth in Tier 2/3 markets. LTV/CAC ratio of 3.7x at 6 months and 1-day CAC payback (claimed) suggests strong unit economics-driven growth loop. Google Startup Accelerator selection (2024) provides Google co-marketing. CAC via Google Ads + Facebook.
- **Brand / community moat:** Building. "SpeakX" brand is associated with affordable Indian English confidence app. Viral anecdotes (Patna taxi driver +₹3K/month income) circulate in founder media. ESOP buyback signals talent retention culture.
- **Regulatory moat:** None identified. No Bhashini, ONDC, or government-tender positioning found. No regulatory certification required in consumer edtech. Lack of government integration is a gap vs. competitors who may pursue PMKVY or Bhashini channels.
- **Replication cost (6mo, $10M competitor):** A well-resourced competitor (e.g., Duolingo India team, or a new startup with $10M) could replicate the core app in ~6 months using the same Gemini API stack, Flutter, and paid UA — the core tech is commodity. What they cannot easily replicate: the 10M download base, Play Store ratings/reviews, and the trust built in Tier 2/3 word-of-mouth networks. Estimated replication of tech: $1–2M; replication of distribution: 12–18 months minimum.
- **Moat strength: 2.5/5** — Distribution and brand in a neglected market provide real but narrow advantages; no proprietary model or data moat yet, and Google dependency is a single-point risk.

## 8. Risks & Problems

### Technical complaints
- No specific Reddit threads, HN posts, or GitHub issues found targeting SpeakX's AI quality
- General app issues common to ed-tech (offline access limitations, occasional glitches) referenced in generic reviews but not with SpeakX specifics
- Company's heavy reliance on Google Gemini API creates **platform risk** — any Google pricing change, API deprecation, or outage directly impacts product
- ASR accuracy for heavy regional accents (e.g., Tamil, Telugu speakers learning English) is unverified — this will be a key risk as SpeakX expands to non-Hindi markets
- Reported Google Play Store rating: 4.4–4.5 / 5 (58–74K ratings) — strong but not exceptional; iOS rating 4.8 / 5 (196 ratings, small sample)

### Pricing pain points
- Refund policy: **No refunds** on monthly subscriptions or trial periods (per speakx.in/refund-policy)
- Customer care contact: contact@ivypods.com — no dedicated phone line widely published
- At ₹299/month (~$3.60), pricing is accessible but could feel steep for rural India at <₹15K/month income

### Safety / misuse
- No reported safety incidents found
- AI conversation partner could theoretically be misused for content outside English learning scope; no published content policy found
- No specific moderation framework described publicly

### Legal / regulatory
- No litigation found
- MCA filing shows HDFC Bank loan of ₹7 Cr (Feb 2025) and RBL Bank loan of ₹2.5 Cr (Dec 2025) — moderate debt load for a ~$1.15M revenue entity, though EBITDA-positive claim mitigates risk
- Founders' equity diluted to ~14.9% after multiple rounds; institutional funds hold 57.62%

### Churn signals
- Month-3 retention: 35% (claimed, Outlook Business). This means ~65% of users churn within 3 months — significant for a subscription product
- 200K paying subscribers on 10M+ downloads implies ~2% conversion rate — reasonable but suggests large leaky funnel
- No evidence of customer success or human intervention layer to reduce churn

## 9. Competitive Position

- **Direct competitors:**
  - **ELSA Speak** (US-headquartered; 25M+ users, 400+ enterprise clients; focused on American English pronunciation; $25M+ raised; stronger in enterprise)
  - **Duolingo** (40M DAU globally; heavy gamification; broad language coverage; not India-specific; much higher valuation)
  - **Josh Skills / JoshTalks** (India; spoken English; similar Tier 2/3 positioning; integrates video content)
  - **Airlearn** (India; mentioned in inc42 as direct competitor; limited public info)
  - **Lingokids, Praktika AI, SpeakBUDDY** (mentioned on Tracxn as competitors; different segments)
  - **Speak.com** (US; $500M+ valuation; OpenAI-backed; global language learning; different price point)

- **Where it's winning:**
  - Price point (₹299 vs. $20–40/month for ELSA/Duolingo premium) for Indian market
  - Hindi-native interface and Hinglish understanding
  - Tier 2/3 India penetration and cultural resonance
  - Unit economics: 1-day CAC payback and 3.7x LTV/CAC (claimed) — among best in Indian edtech
  - Lean AI-native model (20-person team, zero human tutors) enabling profitability at small scale

- **Where it's losing:**
  - No Indic language diversity (only Hindi UI for now)
  - No enterprise/institutional track record at scale vs. ELSA's 400+ org clients
  - No published research credibility vs. AI4Bharat-aligned players
  - Smaller absolute user base vs. Duolingo or ELSA
  - Zero open-source or model-level brand (no HF presence, no arXiv papers)
  - Platform dependency (Google) vs. competitors building proprietary ASR

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| Oct 2024 | Selected for Google for Startups Accelerator (cohort of 20); access to Google AI tools, cloud credits, and Android/Play team mentorship | CXO Today |
| Nov 2024 | Partnership with Cloudnine Hospital to train nurses in English communication | APN News, BusinessReviewLive |
| Feb 2025 | YourStory feature on GenAI English learning approach | YourStory |
| Apr 2025 | Achieved EBITDA profitability (claimed) | Multiple sources |
| Jul 2025 | Reports of planned $11M raise from Elevation Capital and WestBridge begin circulating | StartupNews.fyi, CEO India Magazine |
| Oct 14, 2025 | Closed $16M Pre-Series B led by WestBridge Capital; valuation ~$50M | Inc42, Entrackr, YourStory, AIM |
| Nov 2025 | Announced $1M ESOP buyback for 15 employees | Entrackr, HRKatha, MediaBrief |
| Feb 10, 2026 | App updated to v5.4.3 (iOS) | App Store |
| May 2026 | Arpit Mittal confirmed as speaker at Happy Llama 2026 (Analytics India Magazine event) | AIM Happy Llama |

**Velocity verdict:** High positive momentum. Company executed a clean pivot from failed edtech (Yellow Class) to a profitable AI app in under 2 years. The Pre-Series B close in a difficult edtech funding environment, EBITDA positivity, strong app store ratings, and 624% revenue CAGR (MCA FY24-25) signal genuine product-market fit. The Google Accelerator selection and OpenAI angel (Shyamal Anadkat) lend external validation. However, the company is still small ($7.5M ARR claimed), and regional language expansion + enterprise scale-up are unproven. Velocity is accelerating but from a small base.

## 11. Bull Case / Bear Case

**Bull:**
- India has 400M+ aspiring English speakers who are underserved at sub-$5/month price points; SpeakX is the only EBITDA-positive pure-play in this segment
- 1-day CAC payback and 3.7x LTV/CAC create a compounding growth flywheel; every dollar of the $16M raise directly amplifies a proven unit economics model
- Google Gemini infrastructure enables rapid feature shipping with a 20-person team; expanding to 5 more Indic UI languages within 12 months could 3–4x TAM
- Strategic angels (OpenAI's Shyamal Anadkat, upGrad's Ronnie Screwvala) open doors to enterprise and international partnerships
- Targeting $300–400M revenue in India alone within 3 years is ambitious but not unreasonable given market size

**Bear:**
- 65% monthly churn at month 3 is structurally dangerous; if retention does not improve at scale, growth becomes an expensive treadmill
- Zero proprietary AI — any Google pricing change or API deprecation (Gemini) directly threatens the product
- The $7.5M ARR claim vs. ₹9.63 Cr MCA revenue is a red flag; transparency on financials is low for an institutional-backed company
- Duolingo, with $78M raised and 40M DAU, is actively expanding its India-specific offering and could flood the market with a free tier
- ELSA Speak has the enterprise moat SpeakX needs but lacks; selling into hospitals and corporates requires a sales org SpeakX has not built
- Headcount went from 67 → 20 during the pivot — key institutional knowledge may have been lost; scaling back up post-funding is risky

## 12. What I Couldn't Find
- Exact post-money valuation (conflicting figures: $50M from MCA CCPS analysis vs $66M from one media source; company did not confirm)
- iOS App Store review count is very low (196 ratings as of Feb 2026) — suggests iOS is not the primary acquisition channel; Android metrics more material
- Specific ARR reconciliation between $7.5M claimed and ₹9.63 Cr (~$1.15M) MCA-filed revenue
- Anshul Gupta's current activities post-departure (no recent LinkedIn activity found)
- Bhashini, AI4Bharat, ONDC, or government tender involvement — none found
- Published ASR/LLM benchmarks or model evaluation reports
- HuggingFace presence — none found
- Specific Series A valuation in 2021 (Crunchbase showed ₹178 Cr but this may be Yellow Class era, not verified)
- SpeakX Business pricing or enterprise customer count beyond Cloudnine Hospital
- Any patent filings or IP registrations

## Sources
1. https://yourstory.com/2025/10/gen-ai-english-speaking-speakx-funding-westbridge-elevation
2. https://analyticsindiamag.com/ai-news-updates/speakx-raises-16m-pre-series-b-to-scale-ai-powered-spoken-english-learning/
3. https://inc42.com/buzz/speakx-raises-16-mn-to-offer-english-learning-course-in-regional-languages/
4. https://inc42.com/startups/a-timely-pivot-how-genai-allowed-speakx-to-find-a-new-edtech-mission/
5. https://entrackr.com/news/edtech-startup-speakx-raises-16-mn-led-by-westbridge-10559891
6. https://entrackr.com/snippets/edtech-startup-speakx-announces-1-mn-esop-buyback-for-15-employees-10810376
7. https://www.outlookbusiness.com/start-up/investors/speakxai-raises-16-mn-from-westbridge-capital-eyes-regional-language-expansion-amid-profitable-growth
8. https://www.entrepreneur.com/en-in/news-and-trends/speakxai-raises-usd-16-mn-to-strengthen-ai-powered-english/498354
9. https://www.tice.news/know-this/from-small-town-dreams-to-global-classrooms-how-speakx-is-rewriting-indias-edtech-story-with-ai-11802352
10. https://startuptalky.com/arpit-mittal-speakx-shares-insights/
11. https://www.adgully.com/post/1688/how-edtech-startup-speakx-is-using-real-time-ai-to-revolutionise-english-learning-in-tier-2-3
12. https://tracxn.com/d/companies/speakx/__Fw1PYzB_LG5e1_815d4j4yITneR6DBNYf_o3F0OuGF8
13. https://tracxn.com/d/legal-entities/india/ivypods-technology-private-limited/__bwrQvyouzYyw332dNCxgylYzCBSa8Zczx03f5_THnpM
14. https://www.thecompanycheck.com/company/ivypods-technology-private-limited/U80100HR2019PTC081913
15. https://www.zaubacorp.com/IVYPODS-TECHNOLOGY-PRIVATE-LIMITED-U80100HR2019PTC081913
16. https://www.crunchbase.com/organization/yellow-class
17. https://pitchbook.com/profiles/company/454358-71
18. https://play.google.com/store/apps/details?id=yellowclass.kids.live&hl=en_US
19. https://apps.apple.com/in/app/speakx-english-speaking-app/id6756059415
20. https://github.com/yellowclass
21. https://cxotoday.com/press-release/speakx-gets-selected-for-google-startup-accelerator/
22. https://www.apnnews.com/speakx-partners-with-cloudnine-hospital-to-enhance-english-communication-skills-for-nurses/
23. https://businessreviewlive.com/speakx-partners-with-cloudnine-hospital-to-enhance-english-communication-skills-for-nurses/
24. https://startupnews.fyi/2025/10/14/speakx-raises-16-million-from-westbridge-others-pivots-to-an-english-learning-app/
25. https://startupnews.fyi/2025/11/25/edtech-startup-speakx-announces-1-mn-esop-buyback-for-15-employees/
26. https://theorg.com/org/speakx/org-chart/arpit-mittal
27. https://theorg.com/org/speakx/teams/engineering
28. https://theorg.com/org/speakx/org-chart/deepank-agarwal
29. https://www.linkedin.com/in/arpitmittal4/
30. https://www.linkedin.com/in/deepank411/
31. https://happyllama.analyticsindiamag.com/speaker/arpit-mittal/
32. https://bwdisrupt.businessworld.in/article/Renting-Platform-FastFox-com-Acquires-Roofpik-com-/22-05-2018-149884/
33. https://speakx.in/refund-policy
34. https://www.siliconindia.com/news/startups/speakx-surpasses-10000--paid-subscribers-monthly--achieves-500000-arr-in-under-8-months-nid-232028-cid-19.html
35. https://arabfounders.net/en/speakx-raises-16m-ai-english-learning/
36. https://www.ceovine.com/speakx-raises-16-million-pre-series-b/
37. https://ceoindiamagazine.com/ai-based-edtech-startup-speakx-raises/
38. https://speakx.ai/
39. https://www.indiacustomercare.com/speakx-learning-customer-care-no
40. https://www.truevalueinfosoft.com/speakx-ai-english-learning.html
