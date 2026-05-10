# Bolna AI

**Website:** https://bolna.ai  •  **HQ:** Bengaluru, India (US entity: Dover, Delaware)  •  **Founded:** February 2024  •  **Stage:** Seed
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): Orchestration middleware that stitches together best-of-breed ASR, LLM, and TTS providers into deployable voice agents tuned for India's noisy telephony, multilingual, and high-volume enterprise calling environment.
- Total funding to date: ~$6.92M across 3 rounds (Tracxn; verified via multiple sources)
- Last round: $6.3M seed, January 20 2026, lead: General Catalyst
- Headcount: ~25 (Tracxn, March 2026); 21 per YC profile (Feb 2026); nine of those are "forward-deployed engineers" per TechCrunch; growing 2–3 engineers/month
- Revenue / ARR: ~$700K ARR as of Jan 2026 (verified: TechCrunch, Inc42); monthly revenue ~INR 50 lakh (~$59K); FY26 (ending Mar 2026) projected INR 3–4 Cr (~$360–480K); FY27 target INR 45–50 Cr (~$5.4–6M). 75% of revenue is self-serve.

## 2. Funding History
| Date | Round | Amount | Lead | Other Investors | Source |
|------|-------|--------|------|-----------------|--------|
| Nov 5, 2024 | Seed (accelerator) | Undisclosed | Upekkha | — | Tracxn; Upekkha portfolio page |
| Aug 31, 2025 | Seed | Undisclosed (YC standard deal ~$500K) | Y Combinator | — | Bolna newsroom; YC profile (YC F25 batch) |
| Jan 20, 2026 | Seed | $6.3M (INR ~57.3 Cr) | General Catalyst (Akarsh Shrivastava) | Blume Ventures, Orange Collective, Pioneer Fund, Transpose Capital, Eight Capital; angels: Aarthi Ramamurthy, Arpan Sheth, Sriwatsan Krishnan, Ravi Iyer, Taro Fukuyama | Bolna newsroom; TechCrunch; Inc42 |

**Notes:**
- Post-money valuation not publicly disclosed in any round.
- Tracxn estimates post-money range $2.8M–$7.9M across the three rounds (methodology unclear; treat as estimate).
- Legal entity for US fundraising: Whismurwave Inc. (Delaware). Indian subsidiary: Whismurwave Labs Private Limited (CIN: U62099HR2024PTC118989, incorporated Feb 16, 2024, registered in Haryana).
- Bolna applied to YC five times before acceptance per TechCrunch; early skepticism from YC that "Indian enterprises are not going to pay."

## 3. Product & Customers

### Products
Bolna offers three primary access modes for the same underlying orchestration platform:

1. **Open-Source SDK (bolna-ai/bolna on GitHub)** — MIT-licensed Python framework; self-hosted; WebSocket-based pipeline connecting ASR + LLM + TTS + telephony. Described as "innovations land here first."
2. **Hosted Platform (platform.bolna.ai)** — No-code/low-code dashboard for designing, testing, and deploying voice agents; includes workflow builder, agent templates, call monitoring, and batch calling.
3. **Enterprise / On-Premise** — Full data-sovereignty deployment on customer's own AWS/GCP/Azure/bare-metal; audio, logs, and transcripts stay within customer environment; only billing metrics sent to Bolna cloud. Containerized via Docker/Kubernetes.

**Key platform capabilities (verified from website and docs):**
- Bulk calling (thousands of simultaneous calls)
- Custom API triggers for real-time external integrations during calls
- Human-in-the-loop call transfer
- IVR routing (multi-digit collection, conditional branching — added Jan 2026)
- Auto-retry for failed calls (up to 3 retries, configurable delay — Jan 2026)
- Auto-reschedule when callers request callback (Jan 2026)
- Multilingual message auto-switching (detects caller language mid-call — Jan 2026)
- Noise cancellation (Jan 2026)
- Truecaller caller ID verification integration (India-specific)
- English number pronunciation regardless of core call language
- Keypad DTMF input support
- Model switching per call / per use case
- Vobiz telephony integration for India (Jan 2026)

**Use-case verticals:** E-commerce (cart recovery, delivery follow-up), BFSI (collections, lead qualification), recruitment (screening, scheduling), customer support, logistics, education.

### Pricing
(Verified from bolna.ai/pricing and docs; as of May 2026)

| Plan | Price | Includes |
|------|-------|---------|
| Pay-as-you-go | Top-up credits $10–$5,000 | Flexible; no commitment |
| Pilots | 10,000 min base + 20% bonus = 12,000 min | ~6¢/min effective; 100 concurrent calls; 1 pre-built agent; free phone number 30 days; sub-accounts |
| Enterprise | Custom | Volume discounts; dedicated account manager; custom integrations; priority support |

- **Platform fee:** ~$0.02/min flat (Bolna surcharge on top of provider pass-through costs)
- **All-in estimated cost:** ~$0.06/min including ASR + LLM + TTS provider costs at standard rates
- **BYOK (Bring Your Own Key):** Supported — users can connect own Deepgram/OpenAI/ElevenLabs accounts to reduce cost
- **Free trial:** $5 credit on signup (claimed; not independently verified)
- **INR pricing:** ~₹5–7/min standard; drops to ~₹3/min at volume (per comparison blogs and Inc42)
- No free tier for ongoing use beyond trial credits.

### Languages & Voices
- **Claimed:** 10+ Indian languages including Hindi, Hinglish, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Odia, plus English and other global languages (100+ total via provider pass-through per May 2025 changelog)
- **Via Sarvam AI integration (Saarika STT + Bulbul TTS):** Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Odia — native accent and code-switching support
- **Voice count:** Not published as a discrete number; voices depend on TTS provider chosen (ElevenLabs library, Azure neural voices, Cartesia, etc.)
- **50+ accents** claimed on YC profile (unverified; likely refers to provider-level voice options)
- Indic language quality relies heavily on Sarvam AI (Saarika/Bulbul) rather than proprietary Bolna models; AI4Bharat models not explicitly listed as an integration

### Named Customers
| Customer | Vertical | Metric (claimed) | Source |
|----------|----------|-----------------|--------|
| GoKwik | E-commerce enablement | 400K+ unique engagements; 250K min processed; 250 peak concurrent calls | bolna.ai case study |
| Varun Beverages | BFSI/enterprise | Mentioned as customer | Inc42; TechCrunch |
| Spinny | Auto/e-commerce | Named customer | Bolna website; Inc42 |
| Snabbit | Quick commerce | Named customer | Bolna website |
| Awign | Recruitment/staffing | 10K+ daily calls; 250 concurrent; seamless human escalation | Bolna website |
| Hyreo | HR tech | 96.55% call minutes growth; 10K+ conversations | Bolna website |
| Futwork | Gig economy | 10K+ daily calls | Bolna website |
| Physics Wallah | EdTech | Named customer | Bolna website |
| Knot Dating | Consumer app | Named customer | Bolna website |
| Shop Labs | Retail tech | Named customer | Bolna website |

**Total paying customers:** 1,050+ as of Jan 2026 (verified: Inc42, TechCrunch). E-commerce: ~40% of revenue; BFSI: ~20–25%.

### Integrations / SDKs
**Telephony:** Twilio, Plivo, Vobiz (India), Exotel (coming soon per README), Vonage (coming soon)
**ASR:** Deepgram, Azure, ElevenLabs Transcription (README); Sarvam Saarika (Indic)
**LLM:** OpenAI, Anthropic, Azure OpenAI, Groq, DeepSeek, Llama (via Ollama/Fireworks/Together/Anyscale/DeepInfra), Mistral, Cohere, Perplexity, VLLM, Google Gemini (feature-requested), and custom endpoints — all via LiteLLM
**TTS:** ElevenLabs, Cartesia, AWS Polly, OpenAI TTS, Deepgram Aura, Smallest.ai lightning-v2, Fourie/XTTS; Sarvam Bulbul (Indic)
**Workflow automation:** Zapier, Make.com (Integromat), n8n
**Scheduling:** Cal.com
**CRM/other:** Custom webhook/API triggers; no named CRM-native integrations documented

## 4. Technical Architecture

### Model approach
Bolna is NOT a model company — it is an **orchestration layer / middleware**. It does not train its own ASR, LLM, or TTS models. The core innovation is:
- A WebSocket-based real-time pipeline that coordinates ASR → LLM → TTS with interruption handling
- A **dynamic model router** that selects the best provider per call based on language, use case, and network conditions (avoids single-vendor lock-in)
- LiteLLM for unified LLM API abstraction across 15+ providers
- An "innovations-first" open-source architecture where new features land in the SDK before the hosted product

### Training data
Not applicable — Bolna does not train foundational models. Provider models (OpenAI, Deepgram, ElevenLabs, Sarvam etc.) handle their own training. Bolna's "proprietary AI/ML" referred to in funding announcements likely means fine-tuning or adapting provider models for Indian telephony conditions (noise, accents, code-switching) — details not publicly disclosed.

### Latency profile
| Metric | Claimed value | Source |
|--------|--------------|--------|
| End-to-end pipeline | <600ms (orchestration only) | Docs (platform-concepts page) |
| End-to-end pipeline | <500ms (enterprise claim) | YC profile |
| End-to-end pipeline | ~300ms (blog, year-one post) | Bolna blog |
| Human tolerance threshold | 1,000–1,500ms | Bolna engineering blog |
| RTF / streaming | Not published | — |
| TTFB | Not published | — |

**Note:** The 300ms figure (from Dec 2024 blog) vs 500–600ms from later docs suggests improvement claims have shifted over time; treat as "sub-600ms in production" as the verified baseline.

### Voice cloning
Not a listed feature in any public documentation or pricing page as of May 2026. Voice customization is achieved by selecting from provider voice libraries (ElevenLabs, Cartesia, Azure). Custom voice cloning would require an ElevenLabs Professional Voice Clone subscription passed through Bolna.

### Prosody / emotion control
Not explicitly documented. Prosody is provider-dependent (ElevenLabs, Cartesia support style/emotion tags). Bolna's platform does not expose a proprietary prosody API. "Natural-sounding" claims in marketing refer to provider TTS quality.

### Indic language strategy
- **Primary partner:** Sarvam AI (Saarika STT + Bulbul TTS) — purpose-built for Indian languages, handles code-switching, heavy accents, cultural references
- **Secondary:** Azure Cognitive Services (broad Indic coverage via Neural TTS)
- **AI4Bharat lineage:** Not a direct integration; Bolna relies on Sarvam (which itself has AI4Bharat academic roots from IIT Madras ecosystem) rather than raw AI4Bharat/IndicF5/Indic-Parler-TTS models
- **Bhashini:** No documented integration or partnership found
- **India-specific engineering:** Noise cancellation, Truecaller ID verification, English number pronunciation in Indic calls, DTMF support for IVR

### Inference stack
- Hosted cloud: Multi-tenant; data residency options for India and USA (claimed; not certified)
- On-premise: Docker/Kubernetes; customer-managed; only billing metrics leave environment
- No published information on GPU type, inference framework (vLLM, TensorRT, etc.), or batch processing architecture

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Should your engineering team build Voice AI stack? | Engineering opinion | Apr 16, 2026 | https://blog.bolna.ai/should-your-engineering-team-build-voice-ai-stack/ |
| How to Choose the Right Voice AI Models for Your Voice Agent 2025 | Technical guide | Nov 18, 2025 | https://blog.bolna.ai/choosing-the-right-voice-ai-models/ |
| Build a Multilingual Voice AI Customer Support Agent in Minutes | How-to | Nov 12, 2025 | https://blog.bolna.ai/multilingual-voice-ai/ |
| Bolna vs Vapi: Choosing the Right Voice AI for Your Business | Comparison | 2025 | https://blog.bolna.ai/bolna-vs-vapi-voice-ai-platform/ |
| Bolna vs Retell: Choosing the Smarter Voice AI Platform | Comparison | 2025 | https://blog.bolna.ai/bolna-vs-retell-voice-ai-platform/ |
| Bolna Turns One: A Year of Growth and Innovation | Retrospective | ~Dec 2024 | https://blog.bolna.ai/bolna-turns-one-reflecting-on-a-year-of-growth-and-innovation/ |

No arXiv papers, conference papers, or formal research publications found. Not an AI research organization.

## 5. Open Source Footprint

### GitHub
Organization: https://github.com/bolna-ai (current; previously also hosted at https://github.com/voxos-ai as "VoxOS" — earlier org name before rebranding)

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| bolna-ai/bolna | 639 | 285 | MIT | May 9, 2026 (v0.10.35) | Flagship SDK; Python 99.7%; 37 open issues |
| bolna-ai/web-call | ~0 | 1 | Unknown | Oct 17, 2025 | JavaScript; browser-based call demo |
| bolna-ai/self-hosted-bolna | 1 | 0 | Unknown | Jun 28, 2025 | Docker compose for self-hosting |
| voxos-ai/bolna | Historical | — | MIT | Archived/redirect | Pre-rebrand org; same codebase |

**Total org followers:** 37 (GitHub, as of May 2026 fetch)
**Release cadence:** Active; v0.10.35 shipped May 9, 2026; frequent minor releases throughout 2025–2026
**Issue velocity:** 37 open issues; recent issues include routing bugs (Vobiz India routing), feature requests (Mars8 TTS, Gemini 2.0), and documentation gaps; no critical security disclosures found

### Hugging Face
No Bolna-owned models found on Hugging Face. The platform is a consumer of HF-hosted models (via provider APIs) but does not publish models. Sarvam AI (partner) publishes Saarika and Bulbul on HF under sarvamai org.

| Model | Downloads | Likes | License |
|-------|-----------|-------|---------|
| (None found under bolna-ai org) | — | — | — |

### Top contributors
Exact contributor list not fetched (GitHub contributor tab not extracted). Key contributors identifiable from commits include the founding team (Prateek Sachan / xan_ps on GitHub) and likely Marmik Pandya (mentioned in early LinkedIn post as a founding team member alongside the two co-founders). Community PRs exist given 285 forks and MIT license.

**Community signals:**
- Discord: https://discord.com/invite/59kQWGgnm8 — 65 members (small; primarily support-oriented rather than large developer community)
- Product Hunt launch: Sep 17, 2024
- HN "Show HN" post: Aug 2024 (https://news.ycombinator.com/item?id=41234490) — community reception not deeply sampled but post exists
- PyPI package: https://pypi.org/project/bolna/ — available for pip install

## 6. Team

### Founders
| Name | Role | Education | Prior Experience | GitHub/Social |
|------|------|-----------|-----------------|---------------|
| Maitreya Vaibhav Wagh | CEO & Co-founder | IIT Delhi | Bain & Company (strategy consulting), Probo (founder's office — founder's office at fast-growing consumer startup), Datamuni | linkedin.com/in/maitreya-wagh |
| Prateek Sachan | CTO & Co-founder | IIT Delhi | Zomato, Tata 1MG, BrowserStack, Atlassian, Google, Houm Technology (Singapore) | linkedin.com/in/prateek-sachan; x.com/xan_ps |

**Founding story:** Both IIT Delhi alumni; met and built Bolna starting Feb 2024. Applied to YC five times; accepted in F25 batch (Fall 2025). Maitreya's insight came from seeing Probo struggle to scale customer communication. Prateek brought infrastructure-at-scale experience from Zomato/Atlassian.

### Key technical hires
| Name | Role | Source |
|------|------|--------|
| Marmik Pandya | Early founding team member (engineering) | LinkedIn post by Maitreya (Jan 2024 "we three" reference) |
| Vikram Singh | Engineering (Bolna YC F25) | linkedin.com/in/gujjar95 |
| Dev Gupta | Engineering (Bolna YC F25) | linkedin.com/in/dagupta |

Note: Full org chart not publicly available. Nine "forward-deployed engineers" exist per TechCrunch (Jan 2026).

### Recent joiners (last 12mo)
Two to three engineering hires per month since Jan 2026 per TechCrunch. Specific names not publicly listed. Company grew from ~5 (GetLatka, late 2024) to ~25 (Tracxn, Mar 2026) over 18 months, implying ~20 hires since founding.

### Notable departures (last 12mo)
None found in public sources. One past director (Pramod Abcsdd) ceased Nov 25, 2024 per MCA filings — likely a nominee director from incorporation, not operational departure.

### Open roles signal
Bolna hiring via Gem (jobs.gem.com/bolna) and YC Work at a Startup (workatastartup.com/companies/bolna-ai). Specific roles not extracted due to auth-gated pages. Hiring trajectory (2–3 engineers/month) signals aggressive engineering buildout; "forward-deployed engineers" model suggests customer-success-embedded technical roles — unusual and India-enterprise-appropriate. No ML research scientist roles found, consistent with orchestration (not model training) focus.

## 7. Moat & Defensibility

- **Data moat:** Moderate and growing. 200K+ calls/day through the platform generates call metadata, model performance comparisons, and language/accent signal data usable for router optimization. However, audio data stays with customers (on-premise option) or is not claimed to be retained for training. No disclosed proprietary training dataset. Data moat is real but not yet deep.

- **Model moat:** Weak currently. Bolna does not build foundational models; all models are third-party. Moat here is purely in orchestration logic (routing heuristics, interruption handling, latency optimization) and India-tuned system prompts/configurations. A well-resourced competitor could replicate the orchestration layer in 3–6 months. The bet is that moat builds as Bolna accumulates more enterprise relationships and model-switching data.

- **Distribution moat:** Moderate and strongest of the three. 1,050+ paying customers in 10+ countries after <1 year of commercial operation is strong traction for a seed-stage company. Enterprise relationships (Varun Beverages, GoKwik scale deployments) create switching costs. Nine forward-deployed engineers embedded with customers is a relationship moat. No documented telco partnerships, BFSI framework agreements, Bhashini integration, or ONDC exposure found — these would significantly strengthen distribution if pursued.

- **Brand / community moat:** Early. YC F25 badge, Tech30 2025 recognition (YourStory), TechCrunch coverage, and General Catalyst backing give credibility. GitHub community is small (639 stars, 65-member Discord) — not yet a Vapi-level developer brand. "Innovations land in open source first" philosophy could build developer loyalty over time.

- **Regulatory moat:** Nascent. On-premise offering addresses DPDP Act (India's data protection law) concerns by keeping data on-premise. No SOC 2 certification found in public documentation. No HIPAA or ISO 27001 certifications mentioned. Regulatory compliance is a selling point but not yet a certified moat.

- **Replication cost (6mo, $10M competitor):** A well-funded competitor (e.g., US-based Vapi or Retell expanding to India) could replicate the orchestration layer and provider integrations in 3–4 months for ~$2M in engineering. The harder-to-replicate elements are: India-specific telephony knowledge (Vobiz, Exotel, Truecaller integrations), Sarvam/Indic language tuning, and the customer relationships. Replication of feature parity: achievable in 6mo with $5M. Replication of market position (1,050 customers): 12–18 months minimum. Estimated full replication cost: ~$8–10M over 18 months.

- **Moat strength: 2.5/5** — Strong early traction and India-native positioning, but the orchestration layer is technically replicable and Bolna does not yet own a model, dataset, or telco partnership that creates durable lock-in; defensibility depends on accumulating enterprise relationships faster than competitors can enter India.

## 8. Risks & Problems

### Technical complaints
- **Audio glitches on Twilio calls** — user-reported issue (unresolved per review aggregate data; cited in Tabbly comparison blog). Specific GitHub issue not isolated.
- **GitHub issue #666 (Apr 27, 2026):** "Was this a fork of Vapi?" — suggests community confusion about Bolna's originality vs Vapi; the question alone is a reputational signal worth noting.
- **Vobiz India routing showing "Black" despite active number** (GitHub issue #614, Apr 1, 2026) — integration bug in newest telephony provider.
- **Auto Language Detection works but no visible code in logs** (GitHub issue #659, Apr 22, 2026) — debugging visibility gap.
- **37 open GitHub issues** as of May 2026; no critical CVEs found.
- Latency claims have varied (300ms in Dec 2024 blog vs 500–600ms in later docs) — inconsistent external communication.

### Pricing pain points
- **Developer workflow lock-in:** Some users (per comparison blogs) report that every conversation flow change requires engineering involvement — no true no-code editing of script logic. Contradicts "no-code" marketing claim.
- **Shift from open-source to proprietary features:** Platform shifted some advanced features to hosted-only, raising concerns among open-source users about long-term flexibility.
- **Pricing opacity:** All-in cost (platform fee + provider passthrough + telephony) requires manual calculation; no real-time cost estimator found. BYOK reduces cost significantly, creating ambiguity for self-serve buyers.
- **Customer support responsiveness:** Trustpilot reviews (only 3 total, retrieved via search aggregate) include at least one report of months of non-response to refund requests and multiple failed demo bookings with no callbacks.

### Safety / misuse
- No documented safety incidents, deepfake voice misuse cases, or regulatory actions found.
- Potential misuse vector: high-volume outbound calling platform could be weaponized for spam/fraud at scale. No published content moderation or misuse detection layer found in docs.
- TRAI (India's telecom regulator) has strict rules on unsolicited commercial communications — compliance burden falls on customers, but Bolna's platform could be implicated if customers violate TRAI regulations.

### Legal / regulatory
- No litigation found.
- DPDP Act (India, 2023) compliance: On-premise option addresses this; no DPDP-specific compliance statement found.
- No SOC 2, ISO 27001, HIPAA certifications found.
- US entity registered in Delaware (Whismurwave Inc.); India subsidiary in Haryana (not Bengaluru despite "Bengaluru-based" branding — registered address is Gurgaon).

### Churn signals
- 75% self-serve revenue suggests long tail of small customers, which typically churns faster than enterprise accounts.
- Only 2 named enterprise accounts paying at time of TechCrunch article (Jan 2026); 4 more in pilot — concentration risk in early enterprise book.
- $700K ARR from 1,050+ customers implies average revenue ~$667/customer/year — extremely low for B2B SaaS, dominated by small pilots.

## 9. Competitive Position

- **Direct competitors:**
  - **Vapi** (US) — developer-first, code-centric, ~$0.05/min, strong global brand, no India-native features; most similar architecture
  - **Retell AI** (US) — ~$0.10/min, faster latency (~600ms claimed), English-first, growing enterprise base
  - **Bland AI** (US) — outbound calling focus, US enterprise
  - **Yellow.ai** (India) — conversational AI, older generation, enterprise-heavy, broader NLU platform
  - **Uniphore** (India/US) — enterprise voice AI, BFSI focus, more expensive
  - **Observe.AI** (US/India) — contact center AI, post-call analytics focus
  - **Sarvam AI** (India) — partner today but potential competitor; builds full stack including voice models; could add orchestration layer
  - **Krutrim** (India, Ola) — broader AI play; could enter voice agent space

- **Where it's winning:**
  - India-native enterprise market (noise cancellation, Truecaller, Indic language routing, INR pricing, Vobiz/Exotel telephony)
  - Mid-market self-serve velocity (1,050+ customers in <1 year)
  - Open-source credibility and developer adoption (faster than Yellow.ai/Uniphore for technical buyers)
  - Cost (significantly cheaper than Retell; comparable to Vapi for equivalent use cases)
  - E-commerce and recruitment verticals in India (GoKwik, Awign, Hyreo case studies)

- **Where it's losing:**
  - Enterprise trust / compliance certifications (no SOC 2 vs. Observe.AI, Uniphore)
  - Developer community size (Vapi has much larger GitHub/Discord community globally)
  - Pure English-language or US-market deployments (Vapi/Retell have home advantage)
  - Large BFSI/government contracts requiring full compliance audits
  - Voice cloning / custom voice brand (ElevenLabs has direct enterprise voice offering)

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| Aug 31, 2025 | YC F25 acceptance; raised undisclosed seed from Y Combinator | Bolna newsroom |
| Sep 17, 2024 | Product Hunt launch | Bolna newsroom |
| Nov 5, 2025 | YourStory Tech30 2025 recognition | Bolna newsroom |
| Nov 2025 | YourStory feature article: "Bolna AI is building voice infrastructure for enterprises and Indian languages" | YourStory |
| Jan 20, 2026 | $6.3M seed round led by General Catalyst | TechCrunch, Inc42, Bolna newsroom |
| Jan 20, 2026 | TechCrunch: "Bolna nabs $6.3M from General Catalyst for India-focused voice orchestration platform" | TechCrunch |
| Jan 2026 | General Catalyst blog: "Seeding the Future with Bolna" | generalcatalyst.com |
| Jan 2026 | Inc42: Revenue revealed at INR 50L/month; FY27 target INR 45–50 Cr | Inc42 |
| Jan 27, 2026 | Vobiz telephony integration shipped | Bolna docs changelog |
| Jan 26, 2026 | IVR support + auto-retry for failed calls shipped | Bolna docs changelog |
| May 9, 2026 | v0.10.35 released (most recent GitHub release as of research date) | GitHub |

**Velocity verdict:** High and accelerating. The company went from ~1,500 calls/day to 200,000+ calls/day (133x) in roughly 8 months of commercial operation (May–Jan). ARR approaching $700K from zero in under a year with a team of ~25 is strong execution for an India-focused seed company. Funding velocity (three rounds in 14 months, culminating in a $6.3M General Catalyst-led round) and media coverage (TechCrunch, Inc42, YourStory) signal healthy momentum. Key risk: $5M ARR target by June 2026 is aggressive (7x in ~5 months from Jan 2026 baseline) and may slip.

## 11. Bull Case / Bear Case

**Bull:**
India has over a billion business calls/day, a multilingual population, large enterprises still running manual call centers, and BFSI/e-commerce sectors with strong unit economics for automation. Bolna's orchestration approach avoids model-training capex while still providing enterprise-grade infrastructure. The BYOK model and open-source SDK create a developer flywheel. General Catalyst and YC backing provides both capital and enterprise BD access. If Bolna captures even 0.1% of India's enterprise voice automation market and expands to Southeast Asia, the business is a $50–100M ARR opportunity. The "distribution layer for every voice model" positioning (Jan 2026 blog claim) mirrors Twilio's playbook in telephony — a compelling analogy.

**Bear:**
The orchestration layer has low inherent defensibility — Vapi, Retell, or a well-funded Indian competitor (Sarvam, Krutrim) could replicate the stack. Bolna does not own models, data, or exclusive telephony agreements. At $667 average revenue per customer, scaling to $5M ARR requires either massive customer growth or significant upmarket movement — both hard simultaneously with a 25-person team. Customer support complaints and the small Discord community suggest product-market fit may be narrower than the 1,050-customer count implies. Regulatory tightening (TRAI on spam calls, DPDP Act on data) could increase compliance burden or restrict use cases. The India telephony market is price-sensitive, and competition from incumbent contact-center vendors with existing relationships (Uniphore, Yellow.ai, Exotel's own AI layer) could squeeze margins.

## 12. What I Couldn't Find
- Exact post-money valuations for any round (not publicly disclosed)
- Detailed MCA financial filings / audited revenue figures for Whismurwave Labs Pvt Ltd
- Confirmed SOC 2 / ISO 27001 / HIPAA certification status
- Bhashini integration (none found; likely not yet integrated)
- ONDC exposure (none found)
- Government / telco partnerships (none found publicly)
- Discord member count (65 members found — very small; possibly a newer server)
- Exact GitHub top-contributor breakdown (contributor tab not extracted)
- Specific voice cloning capability (not advertised)
- Upekkha round amount (undisclosed)
- YC standard deal terms confirmation (YC typically invests $500K for 7% in standard deal; not confirmed for Bolna)
- HN "Show HN" post vote count and comment sentiment (page returned 429 error)
- Trustpilot full review text (403 error on direct fetch; aggregate data from secondary sources)
- AI4Bharat or Bhashini direct technical integration

## Sources
1. https://www.ycombinator.com/companies/bolna-ai — YC company profile
2. https://www.bolna.ai — Official website
3. https://www.bolna.ai/newsroom — Press releases
4. https://www.bolna.ai/newsroom/bolna-bags-63-million-seed-funding-led-by-general-catalyst-to-build-indias-voice-ai-platform — Funding announcement
5. https://techcrunch.com/2026/01/20/bolna-nabs-6-3-million-from-general-catalyst-for-its-india-focused-voice-orchestration-platform/ — TechCrunch funding article
6. https://inc42.com/buzz/voice-ai-startup-bolna-raises-inr-57-cr-to-deepen-tech-stack/ — Inc42 revenue and financials
7. https://tracxn.com/d/companies/bolna/__7a7TB7-ZD3lxeIrRnakYOLHeeX1PcB4LuODEfz4DpFw — Tracxn company profile (funding rounds, employee count, valuation estimates)
8. https://github.com/bolna-ai/bolna — GitHub main repo (639 stars, 285 forks, MIT, v0.10.35)
9. https://github.com/bolna-ai — GitHub org page
10. https://github.com/voxos-ai/bolna — Previous org name / historical repo
11. https://www.bolna.ai/docs/platform-concepts — Technical architecture docs
12. https://www.bolna.ai/docs/pricing/call-pricing — Pricing documentation
13. https://www.bolna.ai/pricing — Pricing page
14. https://www.bolna.ai/docs/enterprise/on-premise-deployments — On-premise deployment docs
15. https://www.bolna.ai/docs/changelog/january-2026 — January 2026 changelog
16. https://www.bolna.ai/integrations/sarvam-tts — Sarvam AI integration page
17. https://www.bolna.ai/customer-story/gokwik — GoKwik case study
18. https://www.generalcatalyst.com/stories/seeding-the-future-with-bolna — General Catalyst investment thesis
19. https://blog.bolna.ai/should-your-engineering-team-build-voice-ai-stack/ — Technical blog post
20. https://blog.bolna.ai/bolna-turns-one-reflecting-on-a-year-of-growth-and-innovation/ — Year-one retrospective
21. https://blog.bolna.ai/choosing-the-right-voice-ai-models/ — Technical guide
22. https://blog.bolna.ai/multilingual-voice-ai/ — Multilingual how-to
23. https://blog.bolna.ai/bolna-vs-vapi-voice-ai-platform/ — Vapi comparison
24. https://blog.bolna.ai/bolna-vs-retell-voice-ai-platform/ — Retell comparison
25. https://startupnews.fyi/2026/01/29/bolna-raised-6-3mn-in-seed/ — Startup news coverage
26. https://www.thesaasnews.com/news/bolna-raises-6-3-million-seed-round — SaaS News
27. https://www.upekkha.io/up-portfolio/bolna — Upekkha portfolio (early investor)
28. https://www.thecompanycheck.com/company/whismurwave-labs-private-limited/U62099HR2024PTC118989 — Indian legal entity; CIN U62099HR2024PTC118989
29. https://getlatka.com/companies/bolna.dev — Revenue data ($550K with 5-person team, 2025)
30. https://news.ycombinator.com/item?id=41234490 — HN "Show HN" post (Aug 2024)
31. https://www.bolna.ai/docs/changelog/may-2025 — May 2025 changelog (100+ languages milestone)
32. https://pypi.org/project/bolna/ — PyPI package
33. https://discord.com/invite/59kQWGgnm8 — Bolna Discord (65 members)
34. https://www.linkedin.com/company/bolna-ai — LinkedIn company page
35. https://www.linkedin.com/in/maitreya-wagh/ — Maitreya Wagh LinkedIn
36. https://www.linkedin.com/in/prateek-sachan/ — Prateek Sachan LinkedIn
37. https://x.com/xan_ps — Prateek Sachan on X (Twitter)
38. https://www.saasworthy.com/product/bolna-ai — SaaSworthy product listing
39. https://yourstory.com/2025/11/bengaluru-startup-bolna-ai-voice-infrastructure-enterprises-indian-languages — YourStory feature (Nov 2025)
40. https://pitchbook.com/profiles/company/616216-60 — PitchBook profile
41. https://www.crunchbase.com/organization/whismurwave-inc — Crunchbase profile (legal entity name source)
42. https://github.com/bolna-ai/bolna/issues — GitHub open issues
43. https://github.com/bolna-ai/bolna/releases — GitHub releases
