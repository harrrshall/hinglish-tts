# Vobiz.ai

**Website:** https://vobiz.ai  •  **HQ:** Bengaluru, Karnataka, India  •  **Founded:** 2025  •  **Stage:** Seed
**Last updated:** 2026-05-10

## 1. Snapshot
- One-line pitch (your words): AI-native SIP trunking and telephony infrastructure for voice AI agents, built for India's regulatory environment and sub-80ms latency requirements.
- Total funding to date: $1,000,000 USD (~₹9.5 crore)
- Last round: $1M seed, ~May 5 2026, led by Piper Serica VC Fund
- Headcount: Not publicly disclosed; LinkedIn page exists (in.linkedin.com/company/vobizai) but employee count not indexed as of research date (2026-05-10)
- Revenue / ARR: Not publicly disclosed; company targets $5M ARR by end of FY27 (claimed in Outlook Business, May 2026)

---

## 2. Funding History
| Date | Round | Amount (USD) | Amount (INR) | Lead | Other Investors | Source |
|------|-------|-------------|--------------|------|-----------------|--------|
| ~May 5, 2026 | Seed | $1,000,000 | ~₹9.5 crore | Piper Serica VC Fund | Not disclosed | [Entrackr](https://entrackr.com/snippets/telephony-infra-startup-vobizai-raises-1-mn-led-by-piper-serica-11801843), [Outlook Business](https://www.outlookbusiness.com/corporate/vobizai-raises-1-million-in-seed-funding-round) |

**Notes:**
- Post-money valuation: Not publicly disclosed. No MCA filing data found at time of research.
- Piper Serica VC Fund is a Bengaluru-based early-stage fund; prior portfolio includes Ubiqedge (AIoT, Rs 10 crore seed). No other Vobiz investors disclosed.
- No angel round or pre-seed was surfaced in any source. Tracxn lists the company as "unfunded" for Posibl AI (the predecessor), suggesting no prior institutional capital was raised.

---

## 3. Product & Customers

### Products

Vobiz is a CPaaS (Communications Platform as a Service) focused exclusively on telephony infrastructure for AI voice agents. It is NOT a TTS/STT/LLM provider itself — it is the carrier-and-media layer that plugs into AI providers. Key products/modules (as documented at docs.vobiz.ai, verified 2026-05-10):

1. **SIP Trunking** — Enterprise SIP connections to PSTN; supports G.711 µ-law (8 kHz) and G.722 wideband (16 kHz); setup latency ~1 second; UDP/TCP/TLS signaling; direct carrier interconnects for low-latency India routing.
2. **DID (Direct Inward Dialing) Provisioning** — Instant phone number acquisition; India 1400/1600/92 series; 50+ countries claimed; no provisioning wait times cited in legacy carriers (days/weeks).
3. **WebSocket Streaming** — Raw G.711 µ-law audio (8 kHz, 8-bit) streamed to developer endpoints; near-instant connection; enables custom Python pipelines (Pipecat, custom LLM integrations).
4. **VoiceXML API** — XML-based call flow control via webhooks; interactive XML builder for code generation; callback events: Ring, StartApp, Hangup, recording.completed, conference events.
5. **Conference Calling** — Multi-party call management.
6. **Call Recording and Playback** — Built-in recording with CDR.
7. **WebRTC Browser SDK** — Browser-based calling via endpoint credentials; demo at rtc-demo.vobiz.ai; reference repo: github.com/vobiz-ai/Vobiz-RTC-demo.
8. **WhatsApp Business API** — Claimed in some articles; not found in core docs — treat as "claimed" [India Hood, 2026].
9. **Real-time Sentiment Analysis** — Claimed in some articles; not separately documented in public API docs — treat as "claimed" [India Hood, 2026].
10. **Noise Cancellation** — Built into the media stack.
11. **TRAI/DLT Compliance Automation** — Automated workflows for 1400 (promotional) and 1600 (transactional) series; PE ID, header, content template, consent template requirements handled.
12. **Sub-account Management** — Multi-tenant account hierarchy for agencies/resellers.
13. **Observability Tools** — Listed as a roadmap item (12-18 months from May 2026).

**Notable integration samples (from GitHub, verified):**
- Vobiz + Sarvam AI (Saaras v3 STT + Bulbul v3 TTS) for Hindi/Hinglish voice agents
- Vobiz + Pipecat (FastAPI + WebSocket)
- Vobiz + LiveKit (SIP hub)
- Vobiz + OpenAI Realtime (WebSocket)

### Pricing
(Verified from docs.vobiz.ai/llms.txt, 2026-05-10)

| Item | Price |
|------|-------|
| SIP Trunking | ₹0.45/minute |
| WebSocket Streaming | ₹0.65/minute |
| DID Phone Number | ₹500/month per number |
| Integration fee | ₹0 (free signup, no credit card) |

- Starter credits available for onboarding; free trial offered.
- India-denominated pricing cited as a feature for forex simplification and GST input credit.
- No per-seat or per-1M-char pricing — this is a telephony infra company, not a TTS provider.
- No published enterprise/volume pricing tiers found.

### Languages & Voices

Vobiz is infrastructure, not a TTS/STT model provider. Language and voice support depends on the AI provider plugged in (ElevenLabs, Sarvam, OpenAI, etc.). Vobiz itself handles audio transport in codec-agnostic fashion (G.711, G.722). The Vobiz-Sarvam sample repo demonstrates Hindi/Hinglish via Sarvam's APIs. No proprietary voice or language model.

### Named Customers

No named customers disclosed publicly as of 2026-05-10. The following anonymized use cases are described in the CIOL founder article (verified):
- An NBFC collections team: AI agent calls customers 1-7 days overdue on EMI; TRAI-compliant; cost far below human agents.
- A healthcare network: appointment scheduling across 12 clinics via AI voice agent.
- Real estate: handling 300+ simultaneous inbound inquiry calls.
- Logistics: delivery exception management.

Company claims 5,000+ signups and 80%+ month-on-month growth (claimed in CIOL/Outlook Business, May 2026 — self-reported, not independently verified). Scale cited as growing from 100K calls/week to 1M+ calls/day (claimed, May 2026).

Prior to Vobiz pivot, Posibl AI had 15 paying BFSI customers (claimed in YourStory, Aug 2025).

### Integrations / SDKs

**Verified supported platforms (docs.vobiz.ai, GitHub repos):**
- VAPI (labeled "Most Popular" in Vobiz docs)
- Retell AI
- ElevenLabs (direct PSTN connection)
- LiveKit (WebRTC+SIP hybrid)
- Pipecat (open-source Python framework)
- Bolna.ai (confirmed integration page on bolna.ai)
- Ultravox
- OpenAI Realtime API

**Also mentioned but not separately documented in public docs:**
- Sarvam AI (via sample repo — Saaras v3 STT + Bulbul v3 TTS)

**SDK/API surface:**
- REST API (account, calls, DIDs, CDR, recordings)
- VoiceXML / XML call flow
- WebSocket audio streaming
- HMAC-SHA256 webhook signature verification
- CLI support mentioned in Tracxn summary

---

## 4. Technical Architecture

### Model approach

Vobiz is NOT an AI model company. It is a carrier/CPaaS infrastructure layer. The architecture separates:
1. **Telecom layer (Vobiz):** SIP signaling, PSTN connectivity, DID management, media routing, noise cancellation.
2. **AI layer (customer-selected):** STT (Sarvam Saaras, Deepgram, etc.) → LLM (OpenAI GPT-4o, etc.) → TTS (ElevenLabs, Sarvam Bulbul, etc.).

Vobiz is conceptually analogous to Twilio Voice, not to ElevenLabs or Cartesia.

### Training data

Not applicable — Vobiz does not train or publish AI/ML models.

### Latency profile

- **Claimed end-to-end latency:** Under 80ms (vs. legacy providers' 400-600ms) — self-reported in CIOL article (May 2026), not independently benchmarked.
- **SIP setup latency:** ~1 second (signaling handshake).
- **WebSocket streaming:** Near-instant connection (no SIP handshake overhead).
- **Target for AI conversational turn-taking:** <1000ms total pipeline (including STT+LLM+TTS); Vobiz contribution is the carrier hop component.
- Architecture: single-hop, event-driven; direct carrier interconnects; intelligent edge routing; Voice Activity Detection (VAD) for barge-in; elastic concurrency.

### Voice cloning

Not applicable — Vobiz does not offer voice cloning; this is delegated to integrated TTS providers.

### Prosody / emotion control

Not applicable — Vobiz does not control prosody or emotion; delegated to TTS/LLM providers.

### Indic language strategy

Vobiz provides telephony infrastructure, not language models. Indic language support comes from integrated STT/TTS providers. Verified Indic integration: Sarvam AI (Hindi/Hinglish via Saaras v3 STT + Bulbul v3 TTS) — sample repo at github.com/vobiz-ai/Vobiz-Sarvam.

Regulatory compliance is Indic-focused: 1400/1600/92 number series support; TRAI DLT registration automation; India-denominated billing.

No AI4Bharat, IndicTTS, Shrutilipi, or Bhashini integration found in public documentation or repos as of 2026-05-10. No government (Bhashini/ONDC) contracts publicly disclosed.

### Inference stack

Not applicable (telephony infrastructure, not ML inference). Call processing stack: carrier interconnects → SIP/WebRTC signaling → media servers → WebSocket audio bridge → customer AI endpoint.

### Published research / blog posts
| Title | Type | Date | Link |
|-------|------|------|------|
| Why Telecom Infrastructure Is Holding Back AI Voice | Founder op-ed | ~Apr 2026 | [CIOL](https://www.ciol.com/founders/why-telecom-infrastructure-is-holding-back-ai-voice-11745325) |
| Architecting Real-Time Voice AI: A Deep Dive into Vobiz and Vapi SIP Integration | Third-party Medium post | Mar 2026 | [Medium](https://piyushsahoo7.medium.com/architecting-real-time-voice-ai-a-deep-dive-into-the-vobiz-and-vapi-sip-integration-e21892fd3eeb) |
| Build an AI Voice Agent | Docs guide | 2025/2026 | [docs.vobiz.ai](https://www.docs.vobiz.ai/guides/ai-voice-agent) |
| Making it 'Posibl': Bengaluru startup helping India's BFSI sector | YourStory feature (on predecessor Posibl AI) | Aug 2025 | [YourStory](https://yourstory.com/2025/08/bengaluru-startup-posibl-ai-bfsi-sector-ai-voice-agents) (paywalled) |

No arXiv papers, conference talks, or HuggingFace research artifacts found.

---

## 5. Open Source Footprint

### GitHub

Organization: **github.com/vobiz-ai** (verified 2026-05-10; 5 followers; contact: support@vobiz.ai)

| Repo | Stars | Forks | License | Last commit | Notes |
|------|-------|-------|---------|-------------|-------|
| Vobiz-RTC-demo | 0 | 1 | Not specified | 2025/2026 | JavaScript; WebRTC browser demo; hosted at rtc-demo.vobiz.ai |
| Vobiz-Pipecat | 0 | 0 | Not specified | 1 commit | Python; FastAPI + WebSocket + Pipecat; outbound calling |
| LiveKit-Vobiz-Outbound | 1 | 1 | Not specified | 2025/2026 | Python; forked repo |
| Vobiz-X-Pipecat | 1 | 1 | Not specified | 2025/2026 | Python; forked repo |
| Livekit-vobiz-inbound | 0 | 0 | Not specified | 2025/2026 | Python; forked repo |
| Vobiz-Python-Voice-API-Example | 0 | 1 | Not specified | 2025/2026 | Python; API usage example |
| Vobiz-Android-Sample | 0 | 0 | Not specified | 2025/2026 | Dart; Android client |
| Vobiz-Sarvam | 0 | 0 | Not specified | 2 commits | Python; Hindi/Hinglish voice agent via Sarvam STT+TTS |
| Vobiz-All-XML-python | 0 | 0 | Not specified | 2025/2026 | Python; VoiceXML examples |
| Vobiz-IVR-XML-Python | 0 | 0 | Not specified | 2025/2026 | Python; IVR flow |
| Vobiz-Call-Survey-XML-Python | 0 | 0 | Not specified | 2025/2026 | Python; call survey |
| Vobiz-Number-Capture-XML-Python | 0 | 0 | Not specified | 2025/2026 | Python; DTMF number capture |
| Vobiz-Call-Queue-XML-Python | 0 | 0 | Not specified | 2025/2026 | Python; call queuing |
| Vobiz-Appointment-reminder-XML-Python | 0 | 0 | Not specified | 2025/2026 | Python; appointment reminders |
| Vobiz-OTP-call-XML-Python | 0 | 0 | Not specified | 2025/2026 | Python; OTP calls |
| Livekit-Vobiz-Machine-Detection-Agent-example | 0 | 0 | Not specified | 2025/2026 | Python; answering machine detection |

Assessment: All repos are sample/demo code, not a production SDK or open-source engine. No licenses specified on any repo reviewed. Stars and forks are minimal (0-1 across all), indicating very early community traction. Repos appear to be developer onboarding materials, not open-source product releases.

### Hugging Face

No Hugging Face organization, models, datasets, or spaces found under "vobiz" or "vobizai" as of 2026-05-10. Not applicable (company does not train or publish AI models).

### Top contributors

Primary contributor appears to be internal Vobiz team. Third-party community repos found on GitHub from individual developers integrating Vobiz:
- github.com/Piyush-sahoo/LiveKit-Vobiz-Outbound
- github.com/AVVKavvk/vobiz-openai (WebSocket connection between Vobiz and OpenAI Realtime)

No Discord server found. No community forum or Slack found publicly.

---

## 6. Team

### Founders

**Suman Gandham** — Founder & CEO
- LinkedIn: [linkedin.com/in/gsuman](https://in.linkedin.com/in/gsuman)
- Education: M.Sc., IT University of Copenhagen (2003–2005)
- Serial entrepreneur with telecom and fintech background.
- Co-founded **Finin** (2019) — India's mobile-first neobank; raised ~$1M from angels including Unicorn India Ventures + ~50 lakh founder capital; acquired by Open Financial Technologies (Google-backed) in a $10M cash-and-stock deal, announced Dec 2021, closed 2023. Gandham served as VP Strategy & New Initiatives at Open post-acquisition through ~2023.
- Founded **Dacio** (2024) — AI mobility/dashcam startup for fleet safety; paid customers in logistics/education/OEM (Business Standard, Aug 2024). Status relative to Vobiz is unclear (parallel venture or wound down).
- Founded **Posibl AI** (April 2025) — AI voice agents for BFSI (lending, insurance, banking); 15 paying customers claimed by Aug 2025 (YourStory). Pivoted to infrastructure and rebranded as Vobiz.ai in late 2025.
- Angel investment: Fedo (seed round, Oct 2020, $1.02M round).
- The RocketReach profile labels the entity as "Vobiz AI (formerly Posibl AI)" confirming the entity continuity.

**Vikash Srivastava** — Co-founder
- LinkedIn: Not directly verified; no public profile URL confirmed in research.
- Prior experience: Multiple articles describe him as coming from the telephony/CPaaS industry; one search result summary (unverified) mentions prior experience at Plivo. CIOL article quotes him: "we built the necessary fundamental architecture for voice technologies entirely from scratch, focusing purely on artificial intelligence compatibility." No further biographical detail found publicly.

### Key technical hires

**Kunal Goyal** — Role unspecified; LinkedIn profile exists at [linkedin.com/in/kunal-goyal86/](https://www.linkedin.com/in/kunal-goyal86/) and is listed in the context of "Vobiz AI (formerly Posibl AI)." Specific function (engineering, sales, product) not confirmed.

No VP Engineering, Head of Research, or named ML leads found publicly.

### Recent joiners (last 12mo)

Not publicly available. No LinkedIn headcount data accessible without authentication.

### Notable departures (last 12mo)

None found.

### Open roles signal

No published job listings found on Vobiz website or major job boards as of 2026-05-10. Seed round use-of-funds explicitly includes "strengthening engineering capabilities" and "expanding go-to-market" — suggesting near-term hiring in engineering and sales/BD. The August Fest 2026 speaker listing shows Suman Gandham, suggesting founder conference circuit activity.

### Advisors / Board

Not publicly disclosed.

---

## 7. Moat & Defensibility

- **Data moat:** Weak at present. Vobiz is a telephony infrastructure layer, not a model trainer. Call data flows through the platform but there is no disclosed proprietary dataset, training pipeline, or RLHF program. Regulatory call recordings carry consent requirements under DPDPA that would constrain data reuse. Moat potential exists only if call metadata is leveraged for observability products. Currently: none demonstrated.

- **Model moat:** Not applicable. Vobiz does not train AI models. The architectural differentiation is at the carrier/media-server layer (direct interconnects, single-hop media routing, WebSocket streaming). This is replicable given capital and telecom licensing. No proprietary model, architecture, or training technique published.

- **Distribution moat:** Early-stage but potentially significant. Vobiz claims 5,000+ developer signups and 80%+ MoM growth within ~6 months of launch (self-reported). Integration with Bolna.ai as a listed telephony provider (alongside Twilio, Plivo, Exotel) is a concrete distribution signal. Being listed in Vapi's SIP trunking docs and having sample repos for every major voice AI framework (Pipecat, LiveKit, Retell, ElevenLabs) suggests deliberate platform distribution strategy. India-first compliance (TRAI DLT, INR billing) creates switching friction for India-deployed voice agents. No exclusive telco partnerships or government contracts found.

- **Brand / community moat:** Early. GitHub org exists but repos have near-zero stars. No Discord or community forum. Founder op-ed in CIOL is a positioning play. Integration with Bolna.ai (a known voice AI platform in India) lends credibility. Founder's prior exit (Finin → Open) provides some brand trust with Indian enterprise buyers. No G2/Capterra reviews found.

- **Regulatory moat:** Moderate for India-specific deployments. TRAI DLT compliance, 1400/1600/92 series management, and India-denominated billing are non-trivial to replicate quickly for foreign CPaaS entrants (Twilio, Telnyx). DPDP Act compliance is a claimed differentiator. No SOC2, HIPAA, or ISO 27001 certifications found publicly — the India Hood article claims "GDPR and ISO-certified security standards" for Vobiz but this could not be independently verified from official documentation as of 2026-05-10.

- **Replication cost (6mo, $10M competitor):** LOW-to-MODERATE barrier. A well-funded competitor with $10M and 6 months could replicate the core SIP trunking + DID provisioning stack (this is commercially available infrastructure: Asterisk, FreeSWITCH, Kamailio, standard carrier interconnects). The India regulatory compliance layer and existing carrier agreements would take 3-6 months to negotiate. Developer mindshare and existing integrations would take longer to replicate. True moat lies in go-to-market velocity and carrier relationship depth, not technology exclusivity.

- **Moat strength: 2/5** — Regulatory compliance and India-first positioning create real but replicable advantages; no technical or data moat has been demonstrated yet at this stage.

---

## 8. Risks & Problems

### Technical complaints

No public user complaints found on Reddit, Hacker News, X, GitHub issues, G2, or Capterra as of 2026-05-10. The company is very early-stage (launched late 2025, seed round May 2026), so the user base is not yet large enough to generate public complaint threads. This absence is not a positive signal — it reflects low public visibility rather than high satisfaction.

Known technical constraints (from docs, not complaints):
- WebSocket architecture requires one container/worker per concurrent call (scalability burden on customer).
- International calling requires explicit account-level enablement.
- Standard numbers limited to 500-600 calls/day maximum; warm calling (1K-10K/day) requires verified opt-in.
- SIP setup adds ~1 second of latency before audio begins (tradeoff for enterprise compatibility).
- IP whitelisting required for production trunks (operational overhead).

### Pricing pain points

No public pricing complaints found. At ₹0.45-0.65/minute, Vobiz is priced similarly to or slightly above Exotel/Plivo for India (~₹0.30-0.45/minute for basic outbound). The ₹500/month per DID number is competitive. The WebSocket streaming premium (₹0.65 vs ₹0.45 for SIP) may discourage high-volume deployments on the lower-latency channel.

### Safety / misuse

No safety incidents or misuse reports found. Automated voice calling at scale (1M+ calls/day claimed) carries inherent regulatory risk under India's TRAI Unsolicited Commercial Communications (UCC) framework. The platform's compliance automation is marketed as a mitigation, but the risk of platform abuse for spam calling is real and unaddressed in public documentation.

### Legal / regulatory

- **TRAI/DLT:** Primary regulatory framework. Vobiz claims to automate DLT compliance. No violations or TRAI notices found.
- **DPDP Act (Digital Personal Data Protection Act, 2023):** Voice call recordings and transcripts may contain personal data. Compliance obligations on Vobiz as a data processor are not publicly detailed.
- **EU AI Act / US state laws:** Not applicable for India-focused deployment at this stage, but relevant if the company expands to global markets (50+ countries claimed for DID inventory).
- No litigation, IP disputes, or founder controversies found.

### Churn signals

No publicly available data on churn. The pivot from Posibl AI (application layer) to Vobiz (infrastructure layer) in late 2025 effectively reset the customer base, so historical churn from the Posibl AI phase is not relevant to the current product.

---

## 9. Competitive Position

**Direct competitors (Indian CPaaS/telephony):**
- **Exotel** — Largest Indian CPaaS; $35M+ funded; established enterprise customer base; built for human contact centers, retrofitting AI. Much larger but less AI-native.
- **Plivo** — Global CPaaS with India operations; $20M+ funded; developer-friendly; competes directly on SIP trunking and number provisioning.
- **Ubona** — India-focused voice AI platform; less developer-oriented.
- **Knowlarity (now part of Kaleyra/Sinch)** — Enterprise IVR and cloud telephony India.

**Global CPaaS with India presence:**
- **Twilio** — Dominant global CPaaS; ~$3.5B revenue; deep integrations with AI voice frameworks; but priced in USD and not India-regulation-native.
- **Telnyx** — US-based; developer-friendly CPaaS; no India-specific compliance layer.
- **Vonage (Ericsson)** — Enterprise focus; not AI-native.

**AI voice orchestration platforms (indirect competition but also integration partners):**
- **VAPI, Retell AI, Bolna.ai** — These are voice AI orchestration platforms that sit above telephony; they ARE integration partners but also could vertically integrate downward into telephony (risk).

**Where Vobiz is winning:**
- India regulatory compliance as a native feature (TRAI DLT, 1400/1600/92 series) — foreign CPaaS don't do this well.
- Sub-80ms claimed latency vs legacy provider 400-600ms — relevant for LLM response cycles.
- INR billing / no forex exposure — meaningful for Indian startups.
- Native integrations with every major voice AI framework (Vapi, Retell, Pipecat, LiveKit, ElevenLabs, Bolna, Ultravox, OpenAI Realtime) — breadth of integration is a genuine strength.
- Developer-first: instant DID provisioning (no sales calls required), free signup, free integration.

**Where Vobiz is losing:**
- Scale and trust: Exotel and Plivo have years of enterprise relationships and SLAs; Vobiz is months old.
- Enterprise features: Observability tools, advanced compliance dashboards, and enterprise SLAs are on the roadmap, not yet shipped.
- Geography: 50+ countries claimed for DID, but the product is clearly India-first; global competitors have deeper international carrier agreements.
- Funding: $1M seed vs Exotel ($35M+) and Twilio ($3.5B revenue) — massive resource disparity.
- No SOC2/ISO27001 certification publicly confirmed — may block regulated-sector (BFSI, healthcare) procurement.

---

## 10. News & Momentum (last 12 months)
| Date | Event | Source |
|------|-------|--------|
| Aug 2025 | YourStory feature on Posibl AI (predecessor), 15 paying BFSI customers | [YourStory](https://yourstory.com/2025/08/bengaluru-startup-posibl-ai-bfsi-sector-ai-voice-agents) |
| ~Nov 2025 | Pivot from Posibl AI to Vobiz; official platform launch | [CIOL](https://www.ciol.com/founders/why-telecom-infrastructure-is-holding-back-ai-voice-11745325) |
| Mar 2026 | Third-party Medium article on Vobiz+Vapi SIP architecture deep-dive | [Medium](https://piyushsahoo7.medium.com/architecting-real-time-voice-ai-a-deep-dive-into-the-vobiz-and-vapi-sip-integration-e21892fd3eeb) |
| May 5, 2026 | $1M seed round announced, led by Piper Serica VC Fund | [Entrackr](https://entrackr.com/snippets/telephony-infra-startup-vobizai-raises-1-mn-led-by-piper-serica-11801843) |
| May 6, 2026 | Coverage across 10+ Indian startup media outlets (The AI World, Indian Startup Times, India Hood, Laffaz, Ascendants, Outlook Business, Viestories, DealRoom, DailyHunt) | Multiple |
| May 2026 | Bolna.ai integration listing — Vobiz listed as official integration partner | [Bolna.ai](https://www.bolna.ai/integrations/vobiz) |
| 2026 (TBD) | Suman Gandham listed as speaker at The August Fest 2026 | [theaugustfest.com](https://theaugustfest.com/speaker/suman-gandham/) |

**Velocity verdict: Accelerating.** The company launched in late 2025, raised a seed round within ~6 months, claims 5,000+ signups with 80%+ MoM growth, and has achieved integration-partner status with Bolna.ai and documentation presence in Vapi's ecosystem. Media coverage is entirely positive and driven by the funding announcement — no independent analyst coverage yet. The accelerating signal is real but early and based entirely on self-reported metrics.

---

## 11. Bull Case / Bear Case

**Bull:**
India's voice AI market is at an inflection point — the BFSI, healthcare, and D2C sectors are deploying AI voice agents at scale, and they need compliant Indian telephony infrastructure. Vobiz is the first mover in the "AI-native CPaaS" category in India, has a founder with a prior successful exit and deep BFSI domain knowledge, claims strong early traction (5K+ signups, 1M+ calls/day), and has built native integrations with every major voice AI framework. If the $5M ARR target for FY27 is achieved, the company would be well-positioned for a Series A at a meaningful valuation. The India market structural advantage (TRAI compliance, INR billing) could be a durable moat as foreign CPaaS players struggle to navigate Indian regulations.

**Bear:**
The core product (SIP trunking + DID provisioning) is commodity infrastructure that can be replicated by well-funded competitors. Exotel and Plivo are already actively building AI-native features on their platforms. The voice AI orchestration platforms (Vapi, Retell, Bolna) could vertically integrate downward into telephony, disintermediating Vobiz. The company has $1M in capital, no disclosed SOC2/HIPAA certifications, and is targeting regulated sectors (BFSI, healthcare) that require them. The Posibl AI pivot history suggests the business model is still evolving. Stated metrics (5K signups, 1M calls/day) are self-reported with no third-party verification. The ARR target of $5M by FY27 implies very aggressive monetization of a developer-first product.

---

## 12. What I Couldn't Find
- **CIN / MCA registration details** — MCA portal not scraped; corporate entity name (legal name of the Indian company) not found publicly.
- **Vikash Srivastava detailed background** — LinkedIn URL, education, prior companies, tenure at Plivo (mentioned in one unverified source) not confirmed.
- **Headcount** — LinkedIn employee count not indexed; estimated at <20 given seed stage and funding amount.
- **Current ARR / MRR** — No disclosed revenue figure; only forward target ($5M ARR by FY27).
- **Post-money valuation** — Not disclosed in any funding announcement.
- **Equity structure / cap table** — Not public.
- **SOC2 / ISO 27001 / HIPAA certifications** — Claimed in India Hood article ("GDPR and ISO-certified security standards") but no official trust portal or certification documentation found at vobiz.ai.
- **Named enterprise customers** — All case studies anonymous.
- **G2 / Capterra reviews** — No Vobiz listing on either platform found.
- **Bhashini / ONDC government contracts** — No evidence found.
- **AI4Bharat / IndicTTS / Shrutilipi data lineage** — Not applicable; Vobiz does not train language models.
- **Dacio AI relationship to Vobiz** — Whether Suman Gandham is running both simultaneously or Dacio was wound down before Posibl AI/Vobiz is not clear from public sources.
- **Discordserver / community channels** — None found.
- **Advisor / board names** — Not disclosed publicly.
- **Open job listings** — None found on website or job boards as of 2026-05-10.
- **Actual GitHub license files** — All repos examined had no license specified; open-source status unclear.

---

## Sources
1. [Entrackr — Telephony infra startup Vobiz.ai raises $1 Mn led by Piper Serica](https://entrackr.com/snippets/telephony-infra-startup-vobizai-raises-1-mn-led-by-piper-serica-11801843)
2. [Laffaz — Vobiz.ai Raises $1 Mn Seed Led by Piper Serica for Voice AI Infra](https://laffaz.com/vobizai-raises-seed-funding-piper-serica-voice-ai-infra/)
3. [Outlook Business — Vobiz.ai Raises $1 Million Seed Funding](https://www.outlookbusiness.com/corporate/vobizai-raises-1-million-in-seed-funding-round)
4. [Indian Startup Times — Vobiz.ai Raises $1M to Build AI-Native Voice Infrastructure](https://www.indianstartuptimes.com/investment/vobiz-ai-raises-1m-to-build-ai-native-voice-infrastructure-for-the-next-wave-of-conversational-tech/)
5. [India Hood — Vobiz Secures $1 Million to Develop AI Voice Calling Platform](https://www.indiahood.com/vobiz-secures-1-million-to-develop-ai-voice-calling-platform-in-india/)
6. [The AI World — Vobiz.ai Raises $1M Seed Round for AI Voice Infrastructure](https://theaiworld.org/news/vobizai-raises-1m-seed-round-for-ai-voice-infrastructure)
7. [Ascendants — Vobiz.ai Raises $1M Seed Funding Led By Piper Serica](https://ascendants.in/funding-feed/vobiz-ai-raises-1m-seed-funding/)
8. [Viestories — Vobiz.ai Raises $1Mn Seed Funding Led by Piper Serica](https://viestories.com/funding-alert/vobizai-raises-1mn-seed-funding-led-by-piper-serica-11801990)
9. [DealRoom — Telephony infrastructure startup Vobiz.ai raises $1M](https://app.dealroom.co/news/feed/telephony-infrastructure-startup-vobiz-ai-raises-1m-led-by-piper-serica)
10. [CIOL — Why Telecom Infrastructure Is Holding Back AI Voice](https://www.ciol.com/founders/why-telecom-infrastructure-is-holding-back-ai-voice-11745325)
11. [Tracxn — Vobiz 2026 Company Profile](https://tracxn.com/d/companies/vobiz/__ohCK8-z7-80hEu2U7Gf9yHFnVzRpvmQctXWZ5_qvN5M)
12. [Tracxn — Suman Gandham 2026 Portfolio](https://tracxn.com/d/people/suman-gandham/__sFn0wmZqVUQQcx9f5rdjnDJgXqvuuUYePCRI0Agzg6c)
13. [Crunchbase — VObiz Company Profile & Funding](https://www.crunchbase.com/organization/vobiz)
14. [Vobiz API Documentation (LLM context)](https://www.docs.vobiz.ai/llms.txt)
15. [Vobiz Docs — AI Voice Agent Guide](https://www.docs.vobiz.ai/guides/ai-voice-agent)
16. [Vobiz Docs — SIP Trunking Concepts](https://www.docs.vobiz.ai/concepts/sip-trunking)
17. [Vobiz Docs — AI Voice Agent Solutions](https://www.docs.vobiz.ai/solutions/ai-voice-agent)
18. [Vobiz Docs — WebRTC Application Setup](https://www.docs.vobiz.ai/integrations/webrtc-application-setup)
19. [Medium — Architecting Real-Time Voice AI: Vobiz and Vapi SIP Integration](https://piyushsahoo7.medium.com/architecting-real-time-voice-ai-a-deep-dive-into-the-vobiz-and-vapi-sip-integration-e21892fd3eeb)
20. [Bolna.ai — Vobiz Integration Page](https://www.bolna.ai/integrations/vobiz)
21. [GitHub — vobiz-ai Organization](https://github.com/vobiz-ai)
22. [GitHub — vobiz-ai/Vobiz-Sarvam](https://github.com/vobiz-ai/Vobiz-Sarvam)
23. [GitHub — vobiz-ai/Vobiz-Pipecat](https://github.com/vobiz-ai/Vobiz-Pipecat)
24. [GitHub — vobiz-ai/Vobiz-RTC-demo (referenced in docs)](https://github.com/vobiz-ai/Vobiz-RTC-demo)
25. [YourStory — Making it 'Posibl': Bengaluru startup helping India's BFSI sector (paywalled)](https://yourstory.com/2025/08/bengaluru-startup-posibl-ai-bfsi-sector-ai-voice-agents)
26. [Business Standard — Serial entrepreneur Suman Gandham launches AI-mobility company Dacio](https://www.business-standard.com/companies/news/serial-entrepreneur-suman-gandham-launches-ai-mobility-company-dacio-124080801141_1.html)
27. [They Got Acquired — Finin acquired by Open Financial Technologies](https://theygotacquired.com/fintech/finin-acquired-by-open/)
28. [The August Fest 2026 — Suman Gandham speaker listing](https://theaugustfest.com/speaker/suman-gandham/)
29. [RocketReach — Suman Gandham at Vobiz AI (formerly Posibl AI)](https://rocketreach.co/suman-gandham-email_644485)
30. [Vobiz LinkedIn — in.linkedin.com/company/vobizai](https://in.linkedin.com/company/vobizai)
31. [Suman Gandham LinkedIn — in.linkedin.com/in/gsuman](https://in.linkedin.com/in/gsuman)
32. [Viestories — Top Funding Wrap of the Week 04-08 May 2026](https://viestories.com/funding-alert/top-funding-wrap-of-the-week-04-may-to-08-may-2026-11815764)
33. [Vobiz Status Page](https://status.vobiz.ai/)
34. [Vobiz Console](https://console.vobiz.ai/)
35. [Vobiz Products — Voice Overview](https://www.vobiz.ai/products/voice-overview)
