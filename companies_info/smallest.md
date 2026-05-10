# Smallest.ai

**Website:** https://smallest.ai  •  **HQ:** San Francisco, CA, USA (R&D: Pune, Maharashtra, India)  •  **Founded:** November 2023  •  **Stage:** Seed
**Last updated:** 2026-05-10

---

## 1. Snapshot
- **One-line pitch:** Full-stack real-time voice AI platform — TTS (Lightning), STT (Pulse), SLM (Electron), and agentic orchestration (Atoms) — purpose-built for sub-100ms enterprise conversational AI.
- **Total funding to date:** $8.26M (across 4 rounds; verified via Tracxn and SiliconANGLE)
- **Last round:** $8M seed, October 2025, led by Sierra Ventures
- **Headcount:** ~23 employees (as of August 2025; per Tracxn/MCA filing)
- **Revenue / ARR:** Not publicly disclosed. Indian legal entity (AWAAZ LABS PRIVATE LIMITED) reported ₹93.2L (~$110K USD) revenue for FY2024-25 (ending March 31, 2025) — this reflects very early-stage commercial activity. The company claims 300% YoY US growth and 150% India growth as of October 2025 (unverified absolute figures).

---

## 2. Funding History
| Date | Round | Amount (USD) | Amount (INR est.) | Lead | Other Investors | Source |
|------|-------|-------------|-------------------|------|-----------------|--------|
| Sep 27, 2024 | Angel | ~$0.26M (implied from total) | ~₹2.2Cr | — | DeVC, LetsVenture (LVX), angel investors incl. Mehul Goyal | Tracxn |
| Nov 18, 2024 | Seed | Undisclosed (part of ~$0.26M pre-seed pool) | — | — | 3one4 Capital, Upsparks Capital | Tracxn, Inc42 |
| Dec 31, 2024 | Seed | Undisclosed | — | — | Schema Ventures, Tiny VC | Tracxn |
| Oct 2025 | Seed | $8M | ~₹70.9Cr | Sierra Ventures | 3one4 Capital, Better Capital, Upsparks Capital, Schema Ventures, Tiny VC + angels | SiliconANGLE, Entrackr, YourStory |

**Notes:**
- Tracxn shows total of $8.26M; the $0.26M gap is implied pre-seed/angel funding from 2024 rounds.
- The $8M seed round was described as oversubscribed (claimed, source: BW Disrupt).
- Post-money valuation: Not disclosed in any public source.
- No YC backing found. No Series A announced as of 2026-05-10.
- The Inc42 article (verified) states earlier funding was ~$1.7M from 3one4 Capital, Upsparks Capital, and DeVC.

---

## 3. Product & Customers

### Products
Smallest.ai positions itself as a full-stack voice AI company owning the entire conversation stack in-house. Products as of May 2026:

| Product | Category | Status | Key Claims |
|---------|----------|--------|-----------|
| **Lightning TTS** (v3.1 current) | Text-to-Speech | GA | Sub-100ms TTFB, 44.1kHz, non-autoregressive, 12 languages |
| **Lightning V2** | TTS (legacy) | Deprecated (endpoints still live) | ~$0.20/10K chars |
| **Pulse STT** | Speech-to-Text | GA | 64ms TTFT, 38 languages, code-switching, emotion detection |
| **Electron v2** | Small Language Model | GA | ~4B params, 53ms TTFT, hallucination-resistant |
| **Hydra** | Speech-to-Speech (native) | Early access / waitlist | Sub-300ms, full-duplex, 15+ languages |
| **Atoms** | AI Voice Agent Platform | GA | Agentic orchestration, outbound calling, graph workflows |
| **Waves API** | Developer API layer for TTS/STT | GA | REST + WebSocket, Python/Node SDKs |

**Atoms capabilities (verified from Python SDK README):**
- Create outbound calling agents with custom voices/languages
- Attach knowledge bases (PDF, URL scraping)
- Configure graph-based conversation workflows
- Manage bulk calling campaigns
- Deploy across voice, email, chat, social channels

### Pricing
(Verified from pricing page fetch, May 2026)

| Plan | Monthly | TTS Lightning V2 | TTS Lightning V3.1 | STT Pulse Standard | STT Pulse Realtime | Concurrent TTS |
|------|---------|-----------------|-------------------|-------------------|-------------------|----------------|
| Free | $0 | ~$0.20/10K chars | ~$0.25/10K chars | ~$0.005/min | ~$0.008/min | 5 streams |
| Pro | $9/mo | same | same | same | same | 5 streams |
| Enterprise | Custom | custom/vol discount | custom | custom | custom | custom |

**Additional charges (sourced from qcall.ai review — treat as approximate):**
- Voice cloning: $25/voice on starter tier (free tier claims up to 100 voice clones)
- Custom model training: $500 setup + $200/mo
- Priority processing: ~50% upcharge
- HIPAA add-on (Pro): $1,000/mo
- Overage: ~$0.05/1,000 chars beyond plan limits
- TTS at scale quoted as $0.02-0.03/minute; voice cloning $0.045/minute (from competitive comparison pages — self-reported)

**Free tier:** $10 in free credits on sign-up, no credit card required (claimed).

### Languages & Voices
- **Lightning TTS v3.1 (GA):** 12 languages — English, Hindi, Marathi, Kannada, Tamil, Bengali, Gujarati, Telugu, Malayalam, Punjabi, Odia, Spanish. Mid-sentence code-switching supported.
- **Lightning v3.1 extended (marketing claims):** "30+ languages with thousands of local accents" — not confirmed by documentation; the docs API model page lists 12 languages explicitly.
- **Pulse STT:** 38 languages with auto-detection including Italian, French, German, Portuguese, Ukrainian, Russian, Japanese, Korean, Chinese, and all major Indic languages.
- **Voice count:** 47 voices across languages (sourced from qcall.ai review; Smallest.ai marketing says "thousands of accents" — not verified). The Sarvam comparison blog claims "100+ voices" — conflicts with the 47-voice figure. Treat as approximately 50-100 voices.
- **Voice cloning:** Up to 100 clones in free tier; from 5-15 seconds of audio sample.

### Named Customers
The following are cited as enterprise customers (source: bestvantageinvestments.com article and Smallest.ai website testimonials, October 2025 seed announcement):
- **Paytm** (fintech/payments, India)
- **MakeMyTrip** (travel, India)
- **ServiceNow** (enterprise software, US)
- **Dalmia Cement** (industrial, India)

**Caveat:** No standalone case study links found for any of these customers. Mentions appear in a single press/investor release during the seed announcement. The Inc42 article (October 2025) quoted Akshat Mandloi saying customers include "publicly listed banks and fintech companies in India and the US" but declined to name them in that interview. The four named customers appear in funding announcement coverage — treat as claimed, not independently verified via customer-published case studies.

**Industry verticals targeted:** BFSI (banking, fintech, insurance), healthcare, BPO/contact centers, telecom, retail, e-commerce, recruitment, real estate, logistics.

### Integrations / SDKs
**Verified (from GitHub and blog):**
- Python SDK (`smallest-python-sdk`, MIT, 40 stars) — supports Atoms, Waves (TTS+STT), voice cloning, streaming
- Node.js / TypeScript SDK (`smallest-node-sdk`, 16 stars)
- Vercel AI SDK provider (`smallest-ai-vercel-provider`, TypeScript)
- MCP Server (`mcp-server`, TypeScript) — Model Context Protocol integration
- Pipecat integration — Smallest.ai is a listed TTS provider in pipecat-ai package (verified from search results)
- LiveKit — Native plugin announced May 7, 2026 (Pulse STT + Lightning TTS, 64ms transcription, ~100ms synthesis, interruptible; from blog)
- n8n — PDF-to-Podcast template (May 5, 2026; from blog)
- BiteFlow (`BiteFlow`, Python, 15 stars) — "Add voice to your apps"

**Not found (not verified):** Twilio, Vapi direct integration documentation not surfaced.

---

## 4. Technical Architecture

### Model approach
- **Lightning TTS:** Non-autoregressive (NAR) model. Generates entire speech clips simultaneously rather than token-by-token. Uses a two-stage pipeline: (1) an acoustic model (diffusion-based or transformer-based) mapping phoneme representations to acoustic features, then (2) a neural vocoder converting to waveform. The Tenstorrent paper (arXiv 2604.03279, April 2026) explicitly characterizes it as "diffusion-based." Uses phoneme-based input (not BPE tokenizers) for fast multilingual expansion. Includes a "Style Diffusor" component for voice style transfer.
- **Electron v2:** Small Language Model, ~4B parameters. Described as outperforming "24B-class models at 4B cost." Uses "state-of-the-art data pipelines and intelligence layers." Future versions to incorporate in-house reinforcement learning.
- **Pulse STT:** Described as streaming + batch ASR; no architecture details published.
- **Hydra:** Native speech-to-speech model (not a cascaded STT+LLM+TTS pipeline). Single unified model for audio-in/audio-out. Full-duplex capability. Architecture specifics not published.

### Training data
Not publicly disclosed for any model. The blog post on Lightning notes the phoneme-based approach allows new languages to be added "with as little as one hour of training data" — suggesting a low-shot transfer approach. No information on training data scale, sourcing, or licensing. No public dataset releases on HuggingFace or elsewhere.

### Latency profile
(Verified sources: arXiv paper, blog posts, docs)
| Metric | Value | Source |
|--------|-------|--------|
| Lightning TTS TTFB | <100ms | Product page (claimed) |
| Lightning v3.1 RTF | 0.3 | Competitive comparison blog |
| Lightning V2 RTF | 0.01 | Blog post on Lightning architecture |
| Lightning VRAM | <1GB | Multiple sources |
| Pulse STT TTFT (streaming) | ~64ms | Docs, LiveKit blog |
| Electron v2 TTFT | 53.25ms avg | Electron blog |
| Electron v2 throughput | 41.89 tokens/sec | Electron blog |
| Hydra (speech-to-speech) | <300ms end-to-end | Product page (claimed) |
| Atoms voice agent | <400ms avg latency-to-response | Homepage (claimed) |
| Lightning V2 on Tenstorrent P150 | ~250ms single-device | arXiv 2604.03279 |

### Voice cloning
- Input: 5-15 seconds of reference audio (marketing says "as little as 10 seconds" consistently)
- No fine-tuning or training required; instant inference-time cloning
- Free tier: up to 100 voice clones
- Supports 44.1kHz output; 8-24kHz downsampling for telephony
- Style Diffusor component enables prosody/style transfer

### Prosody / emotion control
- Emotional voices supported; context-adaptive without manual tuning (claimed)
- Breathing patterns and intonation included in v3 (from Lightning V3 launch press release)
- Hydra preserves "tone, urgency, hesitation, and warmth" through the model without text conversion
- Electron v2 includes NSFW and prompt-attack protection

### Indic language strategy
- Lightning v3.1 explicitly supports 8 Indic languages in the API docs: Hindi, Marathi, Kannada, Tamil, Bengali, Gujarati, Telugu, Malayalam, Punjabi, Odia
- Pulse STT supports all major Indic languages in its 38-language set
- Phoneme-based architecture (vs. BPE) designed to require minimal data per new language
- **No Bhashini, ONDC, or AI4Bharat partnerships found** in any source. No government tender exposure identified.
- Primary India go-to-market: BFSI and contact center direct enterprise sales

### Inference stack
- Primarily hosted on AWS (cloud-agnostic; can deploy on customer infrastructure)
- Tenstorrent hardware optimization demonstrated: Lightning V2 on Tenstorrent P150 achieves 4× lower cost vs. NVIDIA L40S (BlockFloat8, 80% of layers, 95% LoFi ops)
- Fleet economics at 550 concurrent 5s-requests: 27 Tenstorrent P150 devices (~$37K) vs. 11 NVIDIA L40S GPUs (~$100K)
- On-premises deployment: listed as "Coming Soon" on website (as of May 2026)
- Self-hosting repo (`smallest-self-host`) exists on GitHub (not yet public/stars)

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Rewriting TTS Inference Economics: Lightning V2 on Tenstorrent Achieves 4× Lower Cost Than NVIDIA L40S | arXiv paper | April 2026 | https://arxiv.org/html/2604.03279 |
| Lightning V3 launch announcement | Press release | March 27, 2026 | https://vmpl.scnwire.com/2026/03/smallestai-launches-lightning-v3-new.html |
| Lightning: Fastest Text-to-Speech Model by Smallest.ai | Blog | Undated | https://smallest.ai/blog/lightning-fastest-text-to-speech-model-by-smallestai |
| Electron V2: A SLM powering real-time conversations | Blog | Undated | https://smallest.ai/blog/electron-v2-a-slm-powering-real-time-conversations-by-smallestai |
| TTS Benchmark 2025: Smallest.ai vs ElevenLabs | Blog | 2025 | https://smallest.ai/blog/tts-benchmark-2025-smallestai-vs-elevenlabs-report |
| TTS Benchmark 2025: Smallest.ai vs Cartesia | Blog | 2025 | https://smallest.ai/blog/tts-benchmark-2025-smallestai-vs-cartesia-report |
| Designing Voice Assistants: STT, LLM, TTS, Latency Budget | Blog | Undated | https://smallest.ai/blog/designing-voice-assistants-stt-llm-tts-tools-and-latency-budget |
| Lightning V2 on Tenstorrent | Blog | April 17, 2026 | https://smallest.ai/blog/ |
| LiveKit Native Integration | Blog | May 7, 2026 | https://smallest.ai/blog/ |
| Pipecat collaboration | Blog | April 30, 2026 | https://smallest.ai/blog/ |

**Note:** No peer-reviewed academic papers beyond the Tenstorrent arXiv preprint found. All benchmarks are self-published.

---

## 5. Open Source Footprint

### GitHub
**Organization:** https://github.com/smallest-inc (14 public repos; verified by fetching)

| Repo | Stars | Forks | License | Language | Notes |
|------|-------|-------|---------|----------|-------|
| smallest-python-sdk | 40 | 12 | MIT | Python | Official Python client; Atoms + Waves; last release v2.1.0 March 4, 2025 |
| cookbook | 19 | 9 | — | Python | Usage examples and guides |
| smallest-node-sdk | 16 | 1 | — | TypeScript | Official Node.js/TS SDK |
| BiteFlow | 15 | 5 | — | Python | "Add voice to your apps" |
| waves-examples | 9 | 5 | — | Python | Waves API examples |
| atoms-sdk-example | 1 | 2 | — | TypeScript | Atoms SDK demo |
| mcp-server | 1 | 0 | — | TypeScript | Public MCP Server |
| smallest-ai-documentation | 0 | 1 | — | MDX | Fern-based SDK/docs generator |
| smallest-ai-vercel-provider | 0 | 0 | — | TypeScript | Vercel AI SDK provider |
| velocity-cli | 0 | 0 | — | Go | Internal CLI (Velocity) |
| smallest-self-host | — | — | — | — | Listed but not public/crawlable |
| smallest-ai-openclaw | — | — | — | — | Listed |
| mintlify-old-docs-redirects | — | — | — | — | Legacy doc redirects |
| waves-examples (dupe?) | — | — | — | — | Listed |

**Assessment:** GitHub presence is purely SDK/developer tooling. No model weights, training code, or research repos are open-sourced. Star counts are modest (flagship SDK at 40 stars), indicating early developer community traction.

### Hugging Face
**Org profiles:**
- https://huggingface.co/smallest-ai ("Smallest Admin") — 0 public models, 0 datasets, 2 followers
- https://huggingface.co/small-ai — 0 public models, 0 datasets, 7 followers

**Verdict:** No models published on HuggingFace as of May 2026. The company is fully proprietary/API-only. No open weights.

### Top contributors
Not determinable from public GitHub data (contributor lists not accessed). Key GitHub handle: `smallest-admin` (linked from HuggingFace).

---

## 6. Team

### Founders
| Name | Role | Background | LinkedIn |
|------|------|------------|----------|
| Sudarshan Kamath | CEO & Co-founder | B.Tech Mechanical Engineering, IIT Guwahati; former engineer at Robert Bosch GmbH | https://www.linkedin.com/in/sudarshankamath/ |
| Akshat Mandloi | CTO & Co-founder | AI Scientist background, IIT Guwahati; former engineer at Robert Bosch GmbH | https://www.linkedin.com/in/akshat-2503/ |

Both founders are college friends (IIT Guwahati alumni) who worked together at Bosch before founding Smallest.ai in November 2023. The founding catalyst was the observation that voice AI was growing but "not a lot of players were focusing on real-time conversations." They bootstrapped initially (working from bedrooms and cafes) until a viral LinkedIn demo in mid-2024 triggered investor interest.

### Key technical hires
| Name | Role | LinkedIn |
|------|------|----------|
| Apoorv Sood | Global Head of Go-To-Market (appointed Oct 2025 with $8M seed announcement) | https://www.linkedin.com/in/apoorv-sood/ |
| Tausif Patel | Employee (specific role unclear) | https://www.linkedin.com/in/tausifpatel/ |

**Note:** The company has ~23 employees. Beyond the founders and Apoorv Sood, individual technical hires are not publicly named in available sources. Speech AI research talent described internally as a "needle in a haystack" problem.

### Recent joiners (last 12mo)
- **Apoorv Sood** — Global Head of GTM (October 2025)
- Other hires not publicly announced

### Notable departures (last 12mo)
None found in any public source.

### Open roles signal
No careers page found (returned 404). No job listings surfaced on LinkedIn or job boards in searches. With 23 employees and an $8M seed raise in October 2025, active hiring is likely but specific open roles are not publicly listed.

### Advisors / board
Not publicly disclosed. Investor board seats: Sierra Ventures likely holds a board seat (standard for lead seed investor) but not confirmed.

---

## 7. Moat & Defensibility

- **Data moat:** Weak at this stage. Training data sourcing and scale not disclosed. No proprietary labeled speech datasets released. The phoneme-based architecture claims 1-hour language onboarding — suggesting efficient transfer rather than brute-force data. As the platform processes "1B+ calls monthly" (claimed), proprietary voice interaction data accumulates but is not yet a stated moat. Rating: 2/5.

- **Model moat:** Moderate. The non-autoregressive + diffusion architecture achieves genuine latency advantages (RTF 0.01 on CPU is exceptional). Tenstorrent hardware co-optimization demonstrates serious inference engineering. The full-stack ownership (STT + LLM + TTS + agent layer) is differentiated vs. API assemblers. However, models are entirely closed/proprietary with no published weights, and the architecture (NAR diffusion TTS) is not novel — competitors like Cartesia (Sonic), ElevenLabs (Flash), and Sarvam use similar NAR approaches. Rating: 3/5.

- **Distribution moat:** Moderate and growing. Named logos include Paytm, MakeMyTrip, ServiceNow, Dalmia Cement. India BFSI focus leverages founder network and local market understanding. 3one4 Capital's portfolio relationships help. Pipecat and LiveKit integrations (verified) build into the developer ecosystem. The GTM hire (Apoorv Sood) signals North America expansion. No Bhashini, ONDC, or government tender exposure found. Rating: 3/5.

- **Brand / community moat:** Early stage. ProductHunt: Lightning V3 ranked #2 Product of Day (April 2026, 324 upvotes). GitHub: ~100 total stars across repos. LinkedIn: product launches visible. The viral LinkedIn demo in mid-2024 was the founding growth moment. Blog content marketing is active (20+ posts). Community is developer-focused but small. Rating: 2/5.

- **Regulatory moat:** None identified. SOC 2 Type II, HIPAA, GDPR, PCI DSS compliance are table stakes for enterprise sales and represent a barrier to smaller competitors, but established players all have these. No specific regulatory certifications, government contracts, or DPDP Act compliance advantages found. No Bhashini integration. Rating: 1/5.

- **Replication cost (6mo, $10M competitor):** A $10M competitor with 6 months could replicate the Lightning TTS API layer using open-source NAR/diffusion TTS foundations (e.g., CosyVoice, StyleTTS2) and add a wrapper. They could not easily replicate: (1) the Electron SLM trained from scratch for conversational AI, (2) the Tenstorrent inference optimization (requires hardware relationships), (3) the Hydra native S2S model, (4) enterprise compliance stack, or (5) the Atoms agentic platform. The full-stack moat is meaningful but not impenetrable at the model layer.

- **Moat strength: 2.5/5** — Strong latency engineering and full-stack ownership create genuine differentiation, but the model architecture is not novel, training data is unknown, open-source community is tiny, and the company lacks the distribution or data flywheels of ElevenLabs or platform giants.

---

## 8. Risks & Problems

### Technical complaints
- **Rate limiting without warning:** Kicks in at 100 RPM on starter/Pro plans with no advance warning (qcall.ai review, 2026).
- **Generic error messages:** "Error 500" responses with minimal debugging information (qcall.ai review, 2026).
- **No sandbox environment:** Every API call incurs charges, making development iteration expensive (qcall.ai review, 2026).
- **Mobile SDKs weak:** iOS/Android SDKs "feel like afterthoughts"; web API performs better (qcall.ai review, 2026).
- **No edge/offline processing:** Cloud-only synthesis, no on-device option (on-premise still "Coming Soon" as of May 2026).
- **Benchmark self-publication:** All TTS quality benchmarks (WVMOS 5.06, MOS 4.14) are self-run. No third-party independent verification found. MOS predictors are known to drift on non-English speech.
- **Tenstorrent latency tradeoff:** On Tenstorrent P150, single-device latency is 250ms — higher than GPU inference. Cost advantage comes at scale, not single-request speed (arXiv 2604.03279).

### Pricing pain points
- **Character-based billing opacity:** Users report 40% higher actual costs than projected (qcall.ai review).
- **Hidden fees:** Voice cloning costs $25/voice on starter; priority processing +50%.
- **Annual cost competitiveness:** At 500K chars/mo, annual cost (~$4,788) reportedly exceeds ElevenLabs ($3,600) and Murf.ai ($4,200) (qcall.ai review — these are third-party estimates, not Smallest.ai's published figures; treat as indicative).
- **Limited voice variety:** 47 voices vs. ElevenLabs' 1,200+ (qcall.ai review).
- **Billing analytics lag 24 hours** — difficult to track real-time spend.

### Safety / misuse
- No published safety policy specific to Smallest.ai found (contrast with ElevenLabs, which publishes a dedicated safety page with consent verification).
- Blog post on "Recognizing and Avoiding AI Voice Cloning Scams" exists but is educational content, not a policy statement.
- Free tier offering up to 100 voice clones with no published consent verification mechanism is a potential misuse vector.
- TAKE IT DOWN Act (US, May 2025) and evolving deepfake legislation create regulatory exposure for any voice cloning provider.

### Legal / regulatory
- No patent filings found in public searches.
- No litigation found.
- Indian entity (AWAAZ LABS PRIVATE LIMITED, CIN U62099PN2024PTC229392) is active and compliant with ROC Pune.
- US entity registered at 311 California Street, Suite 320, San Francisco, CA 94104.
- DPDP Act (India Digital Personal Data Protection) compliance status not disclosed.
- HIPAA compliance offered as a $1,000/mo add-on for Pro plans — standard for healthcare.

### Churn signals
- Documentation described as "incomplete" and "lacking depth" with no video tutorials (multiple review sources).
- Support response time 4-6 hours; phone support enterprise-only.
- "Updates quarterly" vs. competitors shipping monthly (qcall.ai).
- Only 1 verified public review on ProductHunt as of May 2026 (5 stars, 803 followers — small sample).
- No G2 or Capterra profile found. No public churn data.

---

## 9. Competitive Position

- **Direct competitors:**
  - **ElevenLabs** — Dominant in TTS quality/voice variety; slower (527ms India TTFB vs. Smallest.ai's sub-100ms); much larger voice library (1,200+); US-focused.
  - **Cartesia** (Sonic model) — Closest latency competitor (~40ms TTFA claimed); San Francisco; ~$15M+ funded.
  - **Sarvam AI** — India-focused Indic language specialist; 10+ Indian languages; slower (~800ms); different market (open-source friendly, Bhashini-integrated).
  - **Deepgram** — Strong STT; their own TTS offering launched; larger, US-based.
  - **PlayHT / LMNT / Resemble AI** — Western TTS API competitors.
  - **Murf.ai, Speechify** — Creator-focused TTS; less enterprise/latency-oriented.
  - **Yellow.ai, Uniphore, Avaamo** — Contact center AI platforms; more established enterprise distribution.
  - **Bland AI** — Voice agent competitor (Smallest.ai published a direct comparison blog).

- **Where it's winning:**
  - Sub-100ms TTS latency — best-in-class or near-best for real-time conversational applications (Lightning NAR architecture genuinely fast).
  - India BFSI enterprise market — local relationships, Hindi/Indic language support, on-the-ground team in Pune.
  - Full-stack ownership — the only company combining proprietary STT + SLM + TTS + agent platform at this price point.
  - Inference cost efficiency — Tenstorrent co-optimization yields 4× cost reduction at scale vs. NVIDIA L40S.
  - Voice cloning speed — 5-second sample (vs. ElevenLabs 30 seconds).

- **Where it's losing:**
  - Voice variety and quality at scale — 47 voices vs. ElevenLabs 1,200+; MOS scores self-reported.
  - Developer ecosystem/community — GitHub stars in double digits; no open-source models.
  - Geographic reach — primarily India + early US; no Europe/APAC sales motion visible.
  - On-premise deployment — still "Coming Soon" as of May 2026, limiting regulated-industry deals requiring data sovereignty.
  - Marketing/brand — ElevenLabs and Cartesia have significantly larger developer mindshare globally.

---

## 10. News & Momentum (last 12 months)

| Date | Event | Source |
|------|-------|--------|
| May 2025 | TTS API launched on ProductHunt (126 upvotes) | Product Hunt |
| Sep-Oct 2025 | Seed round closes; initial funding from 3one4, Upsparks, DeVC ~$1.7M disclosed | Inc42 |
| Oct 9, 2025 | SiliconANGLE exclusive: $8M seed funding, Sierra Ventures lead | SiliconANGLE |
| Oct 28, 2025 | $8M seed round officially announced; Apoorv Sood joins as Global GTM Head | Entrackr, YourStory, BW Disrupt, Business Standard |
| Oct 2025 | Listed in Inc42 "30 Startups To Watch – April 2025" (timing noted) | Inc42 |
| Mar 27, 2026 | Lightning V3 launched; beats OpenAI, ElevenLabs, Cartesia on MOS benchmarks (self-reported) | The Wire, Business Upturn |
| Apr 2, 2026 | Lightning V3 on ProductHunt — #2 Product of the Day (324 upvotes) | Product Hunt |
| Apr 17, 2026 | Lightning V2 on Tenstorrent paper published; 4× cost reduction vs. NVIDIA L40S | arXiv 2604.03279 |
| Apr 30, 2026 | Pipecat partnership/integration announced | Smallest.ai blog |
| May 5, 2026 | n8n integration announced (PDF-to-Podcast template) | Smallest.ai blog |
| May 7, 2026 | LiveKit native plugin launched (Pulse STT + Lightning TTS) | Smallest.ai blog |

**Velocity verdict:** High and accelerating. Four meaningful product/partnership announcements in a single month (April-May 2026). The Tenstorrent arXiv paper signals serious infrastructure investment. The LiveKit and Pipecat integrations signal a deliberate developer ecosystem build-out. The seed raise attracted credible India (3one4) and US (Sierra) investors simultaneously. Momentum appears strongest in the US enterprise market (300% growth claimed). Key risk is whether the company can close the gap in voice variety and developer community before ElevenLabs or Cartesia improve latency and enter India aggressively.

---

## 11. Bull Case / Bear Case

**Bull:** Smallest.ai owns one of the genuinely fastest TTS inference stacks in production (NAR + Tenstorrent optimization). The full-stack approach (STT + SLM + TTS + agent) creates unique integration leverage for enterprise buyers who want one vendor. India BFSI is a structurally large and underpenetrated market for voice AI, and local presence matters for winning regulated-industry deals. If 1B calls/month is real, the data flywheel for voice quality improvement compounds. The $8M seed from Sierra + 3one4 gives 18-24 months of runway at current burn (23 employees). If Hydra (native S2S) ships and demonstrates quality, it becomes a category-defining product.

**Bear:** All benchmarks are self-published and methodology is weak (comparing against ElevenLabs Flash V2.5, not latest models; WVMOS is known to be unreliable for non-English). With 47 voices and no open-source community, customer lock-in is fragile — a developer can swap the TTS API in a day. ElevenLabs is investing heavily in latency (Flash is at 350ms in US, improving). Cartesia's Sonic claims ~40ms TTFA and is better-funded. The Indian entity revenue (₹93.2L FY25 = ~$110K USD) is tiny relative to the operational scale claimed (1B calls/month would imply millions in revenue — significant discrepancy suggests either the calls claim is inflated or MRC pricing is extremely low). On-premise ("Coming Soon") blocks large regulated deals. No open-source models means no researcher community gravity. Churn risk is elevated given pricing complexity and documentation gaps.

---

## 12. What I Couldn't Find
- ARR or exact revenue figures (Indian entity revenue ~$110K for FY24-25 is the only hard data; company claims growth but no absolute numbers)
- Post-money valuation for any round (not disclosed)
- Named LinkedIn profiles for technical team beyond the two founders and Apoorv Sood
- Full list of angel investors beyond "Mehul Goyal" (12 angels total per Tracxn; identities behind paywall)
- Any independent third-party benchmark or peer review of Lightning TTS quality
- Case study links or customer testimonials published directly by customers (Paytm, MakeMyTrip, ServiceNow, Dalmia)
- Hydra launch date or formal GA availability
- On-premise self-hosting status (repo exists, page says "Coming Soon")
- Government/Bhashini/ONDC integrations (none found)
- CIN for any US entity (US entity appears to be "Smallest Inc." at 311 California St., SF — no Delaware filing details found)
- G2 or Capterra listing or reviews
- Any IP filings (patents, trademarks)
- Specific technical team members (ML researchers, speech scientists)
- LinkedIn headcount delta (6 months ago vs. current — LinkedIn company page not scraped)

---

## Sources
1. https://siliconangle.com/2025/10/09/exclusive-voice-ai-developer-smallest-ai-nabs-8m-investment/
2. https://tracxn.com/d/companies/smallestai/__M_bkNG86V8a7CnAiGLw2oCkEQHuMuRhd0YAMsTbEeGU
3. https://tracxn.com/d/companies/smallestai/__M_bkNG86V8a7CnAiGLw2oCkEQHuMuRhd0YAMsTbEeGU/funding-and-investors
4. https://tracxn.com/d/legal-entities/india/awaaz-labs-private-limited/__103wd9Ers1Lu4aQqxRh_eAu1W4nJ43RXvU9QF9HCtkE
5. https://entrackr.com/snippets/smallestai-raises-8-mn-in-seed-funding-led-by-sierra-ventures-10600511
6. https://www.3one4capital.com/blogs/precision-over-scale-smallest-ai-and-the-future-of-voice-ai
7. https://inc42.com/startups/how-smallest-ai-is-leveraging-small-models-to-fix-voice-ais-latency-problem/
8. https://www.bwdisrupt.com/article/voice-ai-startup-smallest-ai-raises-8-mn-seed-funding-from-sierra-ventures-3one4-capital-others-574944
9. https://smallest.ai/ (homepage, fetched May 2026)
10. https://smallest.ai/text-to-speech (Lightning TTS product page, fetched May 2026)
11. https://smallest.ai/pricing (pricing page, fetched May 2026)
12. https://smallest.ai/voice-cloning (voice cloning page, fetched May 2026)
13. https://smallest.ai/speech-to-speech (Hydra page, fetched May 2026)
14. https://smallest.ai/on-premise (on-premise page, fetched May 2026)
15. https://smallest.ai/blog/lightning-fastest-text-to-speech-model-by-smallestai
16. https://smallest.ai/blog/designing-voice-assistants-stt-llm-tts-tools-and-latency-budget
17. https://smallest.ai/blog/tts-benchmark-2025-smallestai-vs-elevenlabs-report
18. https://smallest.ai/blog/electron-v2-a-slm-powering-real-time-conversations-by-smallestai
19. https://smallest.ai/blog/smallest-ai-vs-sarvam-ai
20. https://arxiv.org/html/2604.03279 (Lightning V2 on Tenstorrent, April 2026)
21. https://github.com/smallest-inc (GitHub org, fetched May 2026)
22. https://github.com/smallest-inc/smallest-python-sdk
23. https://huggingface.co/smallest-ai (fetched May 2026)
24. https://huggingface.co/small-ai (fetched May 2026)
25. https://www.producthunt.com/products/smallest-ai
26. https://docs.smallest.ai/waves/documentation/getting-started/models
27. https://docs.smallest.ai/waves/documentation/speech-to-text-pulse/overview
28. https://qcall.ai/smallest-ai-review
29. https://www.bestvantageinvestments.com/post/smallest-ai-secures-8-million-to-redefine-voice-ai-for-the-enterprise-world
30. https://vmpl.scnwire.com/2026/03/smallestai-launches-lightning-v3-new.html
31. https://finance.yahoo.com/news/smallest-ai-raises-8m-seed-120000316.html
32. https://startupnews.fyi/2025/10/28/smallest-ai-raises-8-mn-in-seed-funding-led-by-sierra-ventures/
33. https://www.crunchbase.com/organization/smallest-ai
34. https://www.crunchbase.com/person/apoorv-sood
35. https://theorg.com/org/smallest-ai/org-chart/sudarshan-kamath
36. https://cartesia.ai/vs/elevenlabs-vs-smallest (competitor page mentioning Smallest.ai)
37. https://x.com/Analyticsindiam/status/1801864777108443573 (AIM tweet on IIT Guwahati founders)
38. https://www.techtimes.com/articles/309548/20250303/smallestai-disrupting-speech-ai-cost-effective-innovation.htm
39. https://www.linkedin.com/in/sudarshankamath/
40. https://www.linkedin.com/in/akshat-2503/
41. https://www.linkedin.com/in/apoorv-sood/
42. https://www.linkedin.com/in/tausifpatel/
43. https://blog.dograh.com/smallest-ai-review-2025-pros-cons-pricing-and-features/
44. https://aimmediahouse.com/ai-startups/smallest-ai-raises-8-million-seed-for-global-expansion
