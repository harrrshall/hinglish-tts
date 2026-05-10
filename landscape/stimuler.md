# Stimuler

**Website:** https://stimuler.tech  •  **HQ:** Bengaluru, Karnataka, India (registered address: Lucknow, UP)  •  **Founded:** March 2022  •  **Stage:** Pre-Series A
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): Voice-first AI English tutor targeting the 800 million+ global ESL population, offering real-time phoneme-level feedback on pronunciation, fluency, grammar, and vocabulary via an AI coach named Sarah.
- Total funding to date: ~$4.78M (verified from Tracxn; comprises three rounds)
- Last round: $3.75M Pre-Series A, 30 April 2025, co-led by Lightspeed and SWC Global
- Headcount: ~34 (Tracxn, as of March 2026); ~10 full-time at Pre-Series A announcement (April 2025); 7-member engineering team (claimed via ZoomInfo)
- Revenue / ARR: ₹3.16 Cr (~$380K USD) annual revenue as of March 31, 2025 (MCA filing via Tracxn). Revenue grew ~5x during 2025; company targeting cashflow-positive in 2026 (claimed). 85% of revenue from outside India.

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| Jul 15, 2022 | Pre-Seed / Seed | $25,000 (claimed) | GradCapital | CIIE (IIM-A incubator), Alagu Periyannan (angel) | D2C Insider; Tracxn; Crunchbase pre-seed round |
| Jul 17, 2023 | Seed | Undisclosed (total $1.02M est.) | Lightspeed India, Rebright Partners | Additional angels | Tracxn |
| Apr 30, 2025 | Pre-Series A | $3.75M (INR ~31.9 Cr) | Lightspeed, SWC Global | M Venture Partners, Rebright Partners, Force Ventures, gradCapital, Operators Studio | Inc42; Entrackr; Entrepreneur India |

**Notes:**
- Tracxn lists total raised as $4.78M across 3 rounds. The gap between $3.75M (Apr 2025) and $4.78M total implies ~$1.03M across the two prior rounds combined.
- Post-money valuations are not publicly disclosed for any round. A 2023 valuation of ₹34.3 Cr (~$4.1M) is cited by one source (PitchBook/Tracxn-era estimate) but unverified.
- YC backing: Akshay Akash has a post titled "Our Y Combinator Interview Experience: Stimuler" (LinkedIn, 2022), indicating they applied but were **not** selected. No evidence of YC batch membership.
- CIN: U72900UP2022PTC160662. Legal entity registered in Lucknow, UP; operations in Bengaluru.

## 3. Product & Customers

### Products
Stimuler is a mobile-first AI English coaching app (Android + iOS) with the following core modules:

1. **AI Conversation Practice (Sarah)** — Voice calls with an AI coach named Sarah across 100+ topics and 20+ themed categories (everyday, tech, hobbies, travel, professional). Users speak for 60 seconds; feedback is returned within ~30 seconds covering pronunciation, fluency, grammar, vocabulary, filler words, pace, and clarity (15+ speech metrics claimed).
2. **Impromptu Speaking Challenges** — Random topics for spontaneous practice to build confidence.
3. **Scenario-Based Roleplay** — Simulated real-world situations: job interviews, client calls, travel scenarios.
4. **IELTS Speaking Mock Tests** — 15+ full-length mock tests structured as Parts 1, 2, and 3. Real-time IELTS band score estimates. Launched "live video mock IELTS interviews with a proprietary AI interviewer" (claimed first-in-class).
5. **Day-wise Learning Roadmap** — Personalized 10–20 min/day exercise plan tailored to individual speech bottlenecks.
6. **Phone Call with AI Tutor** — Launched March 2025 as "world's first phone-call-style AI tutor experience."
7. **Web Platform** — Accessible at stimuler.tech in addition to mobile apps.

**Recognition:** Google Play "Best App with AI 2023."

### Pricing
- **Free tier:** Available (basic sessions, limited daily interactions)
- **Premium:** $4.99–$12.99/month (monthly plans); $18.99–$59.99/year (annual plans) — verified from App Store in-app purchases as of early 2026.
- Marketing claims price as "under $5/month" and "$5–7/month" for premium (may refer to annual pricing tier). One source cites plans from $3/month; another $9.99/month for "unlimited." Discrepancy likely reflects multiple tiers.
- No enterprise/B2B pricing publicly listed.

### Languages & Voices
- **Language:** English-only instruction (verified). Plans to expand to additional languages "in coming years" post-India/LATAM/SEA consolidation (claimed, no timeline).
- **AI coach voice:** Single named persona ("Sarah") — empathic conversational voice powered via Hume AI's EVI (Empathic Voice Interface), enabling emotionally resonant, natural conversation flow (verified via Hume AI case study).
- **User language support:** App marketed globally; no native-language interface localization details publicly confirmed.

### Named Customers
No named enterprise or institutional customers publicly disclosed. App is direct-to-consumer (D2C). Paying users span 150–175+ countries (claimed; varies by source):
- Strongest traction: Indonesia (#1 edu app App Store in Indonesia for a period; top 5 maintained), Colombia, Mexico (LATAM), India.
- 45,000–60,000 paying users as of April–May 2025 (figures vary slightly across sources; D2C Insider cites 60,000, most press coverage cites 45,000+).
- 5–6.1 million app downloads total (Play Store shows 5M+ installs; App Store shows 6.1K ratings; one source cites 6.1M installs total as of early 2026).
- Featured in HolonIQ 2024 South Asia EdTech 100.
- Featured by A16Z, GSV, and Holon in reports/market maps (as cited in the 2024 Year in Review blog post).
- Speaker at ASU+GSV Summit 2026 (Akshay Akash listed as confirmed speaker).

### Integrations / SDKs
- **Hume AI EVI** — Integrated as the conversational AI backbone ("emotionally resonant" voice interactions). 70% adoption rate in pilot (Hume AI case study).
- **WhisperS2T** — Stimuler's GitHub org forks this repo (OpenAI Whisper-based optimized ASR pipeline), strongly suggesting use in their speech-to-text pipeline.
- **Flutter (Mobile)** — App built in Flutter/Dart (confirmed via GitHub forks of flutter_packages and workmanager).
- No public API, SDK, or B2B integration offering documented.

## 4. Technical Architecture

### Model approach
- Proprietary "in-house audio AI infrastructure" (claimed; use of funds from Pre-Series A). Specifics not disclosed.
- Conversational AI layer: **Hume AI EVI** (Empathic Voice Interface) for natural voice-to-voice conversation with Sarah (verified via Hume AI case study, 2024).
- Speech-to-text: Likely **Whisper** or **WhisperS2T** derivative (inferred from GitHub fork of WhisperS2T repo by Stimuler org).
- Speech scoring/feedback engine: Proprietary ("state-of-the-art voice AI refined using millions of user speeches" — claimed). Evaluates 15+ metrics including phoneme-level pronunciation, fluency, grammar, vocabulary, filler detection, pace, and emotional tone.
- LLM for feedback generation: Not disclosed. Hume's EVI integrates with major LLMs (GPT-4, Claude, Gemini); Stimuler's choice not specified.

### Training data
- "Millions of user speeches" used for model refinement (claimed). No dataset publications or public disclosures.
- No AI4Bharat, Bhashini, or IndicVoices dataset usage mentioned.

### Latency profile
- Feedback delivery: "within 30 seconds" for post-session analysis (claimed on App Store). Real-time conversation latency not specified.
- No TTFB or RTF benchmarks published.

### Voice cloning
- Not offered. Single persona (Sarah) only.

### Prosody / emotion control
- Hume AI EVI provides emotion-aware speech synthesis — "emotionally resonant interactions, crucial for driving learning motivation" (Hume AI case study).
- No user-controlled prosody/emotion parameters described.

### Indic language strategy
- English-only at present. No Bhashini, AI4Bharat, or ONDC integrations documented.
- Target markets are international ESL (LATAM, SEA) — not Hindi/Indic language instruction.
- Founders from IIT-BHU; MLE hire Harshit Samrat previously at Sarvam AI (Indic AI firm) and IIT Madras — possible future Indic capability.

### Inference stack
- Cloud-based (mobile app streams to backend). No on-device inference described.
- Flutter front-end; backend infrastructure not disclosed.
- Internet speed test plugin in GitHub suggests bandwidth sensitivity (streaming speech) is a concern.

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Stimuler: Year in Review 2023 | Blog | 2023 | https://stimuler.tech/blog/stimuler-year-in-review-2023-firsts-are-crazy |
| Stimuler 2024: 2nd Year in Review | Blog (Medium) | Dec 2024 | https://medium.com/@teamstimuler/stimuler-2024-2nd-year-in-review-when-your-startup-starts-becoming-a-company-effb2d8d3cc7 |
| Our 2025 Story at Stimuler — Chaos is a Ladder | Blog | 2025 | https://stimuler.tech/blog/our-2025-story-at-stimuler |
| How Stimuler Uses Hume's AI Voice for Language Learning | Case Study | 2024 | https://www.hume.ai/blog/case-study-hume-stimuler |
| ELSA Speak vs Stimuler | Blog | 2025 | https://stimuler.tech/blog/elsa-speak-vs-stimuler-which-ai-english-app-is-right-for-you |
| Speak vs Stimuler (2026) | Blog | 2026 | https://stimuler.tech/blog/speak-vs-stimuler-2026 |
| Shadowing Technique + AI | Blog | 2025 | https://stimuler.tech/blog/shadowing-technique-ai-speak-like-native |
| AI English Speaking Practice: 30 Days | Blog | 2025 | https://stimuler.tech/blog/ai-english-speaking-practice-30-days |

No academic papers (arXiv, ACL, etc.) found.

## 5. Open Source Footprint

### GitHub
Organization: https://github.com/stimuler — "Your Personal Speech Coach" (verified)

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| flutter_packages | 0 | 306 | Not specified | Feb 2026 | Fork of appinio flutter packages |
| workmanager | 0 | 0 | MIT | Jan 2026 | Fork of flutter_workmanager |
| WhisperS2T | 1 | 76 | MIT | Sep 2024 | Fork — optimized Whisper STT pipeline; key signal of ASR stack |
| flutter_internet_speed_test | 0 | 74 | MIT | Aug 2024 | Fork — bandwidth/streaming optimization |
| .github | 0 | 0 | — | Dec 2023 | Org profile |

All repos are forks; no original open-source contributions. No proprietary code open-sourced.

### Hugging Face
Organization: https://huggingface.co/stimuler (verified — 6 team members, 11 followers, interests: Speech Analysis, NLP)

| Model | Downloads | Likes | License |
|-------|-----------|-------|---------|
| (none published) | — | — | — |

No models, datasets, or spaces published as of May 2026 verification.

### Top contributors
- 4 visible GitHub org members (identities not publicly listed on org page)
- Akshat Baranwal GitHub: https://github.com/AkshatBaranwal (CTO, confirmed)

## 6. Team

### Founders
All four founders graduated IIT (BHU), Varanasi in May 2023; company founded in their 3rd year (2022).

| Name | Role | Education | Prior Experience | LinkedIn |
|------|------|-----------|-----------------|---------|
| Akshay Akash | Co-Founder & CEO | B.Tech, IIT BHU (2019–2023) | First venture (Stimuler); ran newsletters in college | https://www.linkedin.com/in/akshay-akash/ |
| Anesh Srivastav | Co-Founder & CPO (also listed as Chief People Officer) | B.Tech Mechanical Engineering, IIT BHU | First venture | https://in.linkedin.com/in/a-niche |
| Akshat Baranwal | Co-Founder & CTO | B.Tech, IIIT Allahabad (note: some sources say IIT BHU — discrepancy) | Application Developer at Oracle (pre-Stimuler) | https://www.linkedin.com/in/akshat-baranwal (inferred) |
| Ankit Kumar Pandey | Co-Founder, Leading AI | IIT BHU | First venture | https://www.linkedin.com/in/ankit0513/ |

**Note on Akshat Baranwal's education:** Most sources group all four as "IIT BHU founders" but ZoomInfo/RocketReach cites IIIT Allahabad for Akshat. This may be an error; unverified.

### Key technical hires
- **Harshit Samrat** — MLE (Applied Science); B.Tech Biotechnology, IIT Madras; previously research assistant at IIT Madras, and at Sarvam AI. Joined as MLE intern, converted to full-time. (ZoomInfo; LinkedIn post confirmed)
- **Ashutosh** — Founding ML Engineer (name only; joined 2024 per 2024 Year in Review blog). Role: Core ML infrastructure.

### Recent joiners (last 12 months, to May 2026)
- Ankit Kumar Pandey added as director at MCA on May 20, 2025 (MCA filing).
- Company target was 3–5 key hires in 2025 (stated in 2024 Year in Review). Headcount grew from ~10 (April 2025) to ~34 (March 2026 per Tracxn).

### Notable departures (last 12 months)
- Not publicly disclosed.

### Open roles signal
- As of 2023, hiring for Flutter Engineer (Akshat Baranwal LinkedIn post). Active hiring signal for engineering roles consistent with Pre-Series A use of funds ("expand technical team"). No current job board publicly indexed.

## 7. Moat & Defensibility

- **Data moat:** Moderate. "Millions of user speeches" used to train and refine proprietary feedback models — the dataset is growing with every user interaction. However, specifics about dataset size, diversity, or exclusivity are unverified. No Bhashini/public-data partnerships that would augment this further. Rating: 3/5.
- **Model moat:** Low-moderate. Speech scoring engine described as "best-in-world" (claimed) with phoneme-level precision tuned for regional accents. Integration of Hume AI EVI provides emotionally aware conversation; WhisperS2T for ASR. Neither component is proprietary at the foundation layer. Custom fine-tuning degree unknown. Rating: 2/5.
- **Distribution moat:** Moderate. 5M+ installs, Google Play "Best AI App 2023" badge, top education app in Indonesia — strong organic and app store distribution in SEA. LATAM traction (Colombia, Mexico) growing. However, no telco/BFSI/ONDC/Bhashini integrations documented. D2C only. Rating: 3/5.
- **Brand / community moat:** Moderate. 4.6–4.8 star ratings across 120K+ Play Store reviews; strong word-of-mouth in Indonesia. IIT-BHU pedigree resonates in India. Active blog content and SEO strategy. Limited community/forum presence. Rating: 2/5.
- **Regulatory moat:** None documented. No data from government programs, no DPDP Act compliance specifics shared, no Bhashini empanelment. Rating: 1/5.
- **Replication cost (6-month, $10M competitor):** A well-funded competitor could replicate the core product (Whisper ASR + Hume EVI + LLM feedback + Flutter mobile app) in 4–6 months for under $3M in engineering. The defensible layer is the proprietary speech-scoring model trained on millions of user utterances and the distribution in niche geographies (Indonesia, LATAM). Rebuilding that user data flywheel takes 12–18 months minimum.
- **Moat strength: 2.5/5** — The product is well-executed but built largely on licensable components; defensibility rests on data flywheel + distribution lead in SEA/LATAM, both of which are vulnerable to a better-funded entrant.

## 8. Risks & Problems

### Technical complaints
- **AI interrupts users mid-sentence:** Google Play review cited: "The AI to call doesn't wait for you to finish talking when it interrupts you." (sourced from Play Store review aggregation, 2024–2025). This is a known limitation of turn-detection in real-time voice AI.
- **Assessment accuracy:** App Store review (1-star, 2025): "it rates everything as great… when in reality nothing is right." Concern that the feedback model is over-positive.
- **Device/connection reliability:** Users report crashes, slow loading, and delayed voice processing on weak connections and certain Android devices.
- **IELTS exam fidelity:** "The prompt of writing IELTS in this app is not really reliable. It is really different from real IELTS." — Play Store review.

### Pricing pain points
- Free tier reportedly provides only 4 sessions before hard paywall. Users report discovering paywall after download without prior disclosure — "the app initially doesn't disclose that you need to purchase a premium subscription."
- Pricing inconsistency across sources ($3–$12.99/month) may cause confusion. Annual plans ($18.99–$59.99/year) represent steep discount; monthly pricing feels high relative to local purchasing power in target markets (Indonesia, Brazil).

### Safety / misuse
- No publicly documented safety policy, content moderation framework, or misuse reports found.
- Voice AI impersonation or roleplay misuse not addressed in public documentation.

### Legal / regulatory
- No litigation or IP disputes documented.
- Data privacy: App collects voice recordings from users in 175+ countries. No GDPR compliance statement, India DPDP Act (2023) compliance, or data-handling disclosures found in public sources. This is a latent risk given the EU and LATAM regulatory environments.
- MCA filings show Stimuler Private Limited is active and compliant as of September 2024 AGM.

### Churn signals
- Trustpilot: Only 1 review; complaint about false advertising ("lied to about unlimited call time with Sarah") and "non-existent" customer support.
- WhatsApp support reportedly unresponsive to users (multiple review sources).
- 45,000 paying users on 5M+ installs implies ~0.9% paid conversion — relatively low, suggesting high free-user churn or paywall friction.

## 9. Competitive Position

- **Direct competitors:** ELSA Speak (pronunciation-focused, US-headquartered, ~$250M raised), Speak.com (AI conversation, ~$65M raised), Praktika (3D avatar AI tutor), BoldVoice (accent reduction), SpeakX (India-focused, Series A, $7.5M ARR), Talkpal, Gliglish.
- **Where it's winning:**
  - Price: $5–7/month vs ELSA Speak's higher tiers and Speak's $8–19/month.
  - Indonesia: Ranked #1 education app on App Store in Indonesia (at peak); top 5 maintained.
  - IELTS prep: Dedicated mock tests with Part 1/2/3 simulation — differentiated vs ELSA and Speak.
  - Breadth of feedback: 15+ metrics vs competitors' narrower focus.
  - Emotional AI: Hume EVI integration for more natural-feeling conversation vs static AI voice tutors.
- **Where it's losing:**
  - Scale and funding: ELSA Speak (~$250M raised) and Speak.com (~$65M) have orders-of-magnitude more capital.
  - Content depth: ELSA has 7,100+ exercises; Stimuler claims 100+ topics.
  - Revenue: SpeakX is EBITDA-positive at $7.5M ARR vs Stimuler at ~$380K ARR.
  - Brand in India: SpeakX dominates India's vernacular-English learner segment.
  - Indic language depth: No Hindi-medium support; SpeakX and Josh Talks serve this need better.
  - Technical staff: Stimuler has ~7 engineers vs competitors with larger ML teams.

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| Mar 2025 | Launched "World's First Phone Call with AI Tutor" feature | Stimuler 2025 blog (claimed) |
| Apr 30, 2025 | Pre-Series A funding: $3.75M from Lightspeed + SWC Global | Inc42, Entrackr, Entrepreneur India |
| Apr 30, 2025 | Reached 4M+ app installs (5x YoY growth) | Funding press releases |
| 2025 | Revenue grew ~5x during the year | Tracxn (inferred from MCA data + blog) |
| 2025 | Headcount grew from ~10 to ~34 | Tracxn vs funding announcement |
| 2026 | Akshay Akash listed as speaker at ASU+GSV Summit 2026 | ASU+GSV Summit website |
| 2024 | Featured in HolonIQ 2024 South Asia EdTech 100 | Search results (claimed by company) |
| 2024 | Featured in A16Z, GSV, HolonIQ reports and market maps | 2024 Year in Review blog (claimed) |
| Mar 17, 2024 | Times of India newspaper feature | 2024 Year in Review blog |
| Jan 2024 | Began monetization (first paying users) | 2024 Year in Review blog |

**Velocity verdict:** Accelerating. The Pre-Series A at $3.75M signals VC conviction; 5x revenue growth and 5x install growth in 2024–2025 are strong indicators. The company is still small ($380K ARR) but the trajectory from zero to paid monetization in <2 years is credible. Geographic bet on LATAM and Indonesia is differentiated vs India-first competitors. Watch: whether the 5x monetization goal ($1.9M ARR by end-2026) is achieved.

## 11. Bull Case / Bear Case

**Bull:** Stimuler is one of the few AI English apps with real global traction outside the US/India axis — Indonesia and LATAM are large, underserved markets with weak local competition. Lightspeed's involvement signals strategic credibility. The combination of Hume EVI (emotional AI) + proprietary speech scoring creates a qualitatively differentiated product vs ASR-only competitors. Phoneme-level feedback tuned for regional accents (a hard technical problem) is a genuine moat if the dataset flywheel compounds. If they hit $1.9M ARR by end-2026 and expand to additional languages, a Series A at $15–20M valuation is plausible.

**Bear:** The core tech stack (Whisper ASR + Hume EVI + LLM feedback) is licensable by any well-funded competitor. ELSA Speak or Duolingo could add a "real-time AI conversation" feature and leverage their existing 50M+ user bases to dominate. Stimuler's $380K ARR is thin runway even with $4.78M raised. The 0.9% paid conversion rate and customer support complaints suggest structural product-market fit issues. Revenue concentration in Indonesia/LATAM creates FX and geo risk. Team of 34 (mostly junior, IIT-BHU fresh grads) may struggle to hire the senior ML talent needed to build a true model moat.

## 12. What I Couldn't Find
- Exact amounts for the July 2022 and July 2023 seed rounds (individual round sizes undisclosed; only $25,000 GradCapital check in 2022 was found via D2C Insider; total $4.78M across 3 rounds confirmed).
- Post-money valuation for any round (not disclosed).
- Specific LLM(s) used in the feedback/conversation stack (beyond Hume EVI for voice layer).
- Latency benchmarks (TTFB, RTF, end-to-end response time for Sarah).
- Full pricing page with exact tier names and feature breakdown.
- Named enterprise/institutional partnerships or B2B customers.
- Any AI4Bharat, Bhashini, or ONDC connections (none found — they are not building for Indic languages currently).
- Akshat Baranwal's verified undergraduate institution (IIT BHU vs IIIT Allahabad discrepancy).
- Advisors or formal board members beyond the four founding directors.
- MCA-filed financial details (revenue, net profit absolute figures) — paywalled on Tofler/Tracxn.
- GitHub usernames for all 4 org members.
- Any published arXiv or peer-reviewed research from the team.

## Sources
1. https://inc42.com/buzz/stimuler-bags-3-75-mn-to-strengthen-its-ai-led-english-tutor/
2. https://entrackr.com/snippets/stimuler-raises-375-mn-in-pre-series-a-round-led-by-lightspeed-9016664
3. https://www.entrepreneur.com/en-in/news-and-trends/stimuler-raises-usd-375-mn-funding-to-scale-voice-first/490839
4. https://indianstartupnews.com/funding/stimuler-a-voice-first-ai-tutor-for-english-as-a-second-language-esl-users-raises-375-million-in-funding-9017114
5. https://thetechportal.com/2025/04/30/ai-powered-language-learning-startup-stimuler-gets-3-75mn-in-pre-series-a-fundraise
6. https://cxotoday.com/press-release/stimuler-raised-3-75m-from-lightspeed-swc-global-to-transform-english-learning-with-ai/
7. https://tracxn.com/d/companies/stimuler/__1Nxuzm2NInbBGjEcJEacsp-6K70lSzHfTO6UHCSZ_hw
8. https://tracxn.com/d/companies/stimuler/__1Nxuzm2NInbBGjEcJEacsp-6K70lSzHfTO6UHCSZ_hw/funding-and-investors
9. https://tracxn.com/d/companies/stimuler/__1Nxuzm2NInbBGjEcJEacsp-6K70lSzHfTO6UHCSZ_hw/founders-and-board-of-directors
10. https://www.thecompanycheck.com/company/stimuler-private-limited/U72900UP2022PTC160662
11. https://www.tofler.in/stimuler-private-limited/company/U72900UP2022PTC160662
12. https://medium.com/@teamstimuler/stimuler-2024-2nd-year-in-review-when-your-startup-starts-becoming-a-company-effb2d8d3cc7
13. https://stimuler.tech/blog/our-2025-story-at-stimuler
14. https://stimuler.tech/blog/stimuler-year-in-review-2023-firsts-are-crazy
15. https://www.hume.ai/blog/case-study-hume-stimuler
16. https://github.com/stimuler
17. https://huggingface.co/stimuler
18. https://apps.apple.com/us/app/stimuler-english-speaking-app/id1627501632
19. https://play.google.com/store/apps/details?id=com.stimuler&hl=en_US
20. https://www.trustpilot.com/review/stimuler.tech
21. https://yourstory.com/2025/07/startup-helping-esl-learners-find-voice-ai-iit-bhu
22. https://www.asugsvsummit.com/speakers/akshay-akash
23. https://www.linkedin.com/in/akshay-akash/
24. https://in.linkedin.com/in/a-niche (Anesh Srivastav)
25. https://www.linkedin.com/in/ankit0513/ (Ankit Kumar Pandey)
26. https://www.zoominfo.com/p/Akshat-Baranwal/9881725526
27. https://www.zoominfo.com/p/Harshit-Samrat/13604047334
28. https://pulse.d2cinsider.com/stimuler-is-revolutionising-spoken-english-for-esl-learners-using-ai-voice-first-technology/
29. https://indiatechdesk.com/ai-driven-english-tutor-stimuler-raises-3-75m-to-empower-esl-learners-globally/
30. https://www.outlookbusiness.com/corporate/stimuler-raises-375m-pre-series-a-to-scale-voice-first-ai-english-tutor
31. https://www.marcamoney.com/stimuler-raises-3-75-million-from-lightspeed-swc-global-and-others/
32. https://pitchbook.com/profiles/company/519397-66
33. https://wellfound.com/company/stimuler-1/people
34. https://stimuler.tech/blog/elsa-speak-vs-stimuler-which-ai-english-app-is-right-for-you
35. https://stimuler.tech/blog/speak-vs-stimuler-2026
36. https://www.holoniq.com/notes/2024-south-asia-edtech-100
37. https://www.voiceaispace.com/tool/stimuler
38. https://www.futurepedia.io/tool/stimuler
39. https://github.com/AkshatBaranwal
40. https://www.appbrain.com/app/stimuler-ai-english-fluency/com.stimuler
