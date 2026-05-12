# Skill: Sentinel Growth Commander — Outbound Growth System

## When to Use This Skill

Invoke this skill when the user asks for help with any of the following:
- Designing or building the multi-agent outbound growth system
- Architecting or extending any individual growth agent (research, messaging, sequencing, etc.)
- Generating cold outreach copy, follow-up sequences, or LinkedIn messages for Vulnaguard Sentinel
- Reviewing or improving message quality, personalization, or compliance safety
- Planning the database schema, tech stack, or API integrations for the growth system
- Triaging campaign failures, escalation logic, or notification routing
- Prioritizing leads or evaluating prospect intelligence outputs
- Deciding what to automate vs. keep human-approved

Trigger phrase: `/growth-commander` or any request related to outbound prospecting, cold email, lead research, outreach sequencing, campaign operations, or growth system architecture for Sentinel-CMMC.

---

## System Objective

Build a multi-agent outbound growth system that researches prospects, generates qualified leads, creates intelligent outreach, manages follow-up sequences, monitors campaign health, and escalates important events to Sean.

The system behaves like an elite outbound operations team — not a mass-email spam system. Quality over volume at every layer.

---

## Architecture Overview

```
                Sentinel Growth Commander
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
Research Layer     Persuasion Layer       Operations Layer
     │                     │                     │
Lead Research       Offer Positioning     Sequence Manager
Intelligence Agent  Psychology Profiling  Notification Agent
Enrichment Agent    Message Writer        Response Parser
Risk Context Agent  CTA Optimization      Escalation Engine
```

---

## System Components

### 1. Sentinel Growth Commander (Orchestrator)

The master orchestration agent. Manages all sub-agents, evaluates outputs, approves workflows, detects failures, and escalates critical events.

**Campaign State Machine:**
- `APPROVED_TO_CONTACT` — research passed, message approved, ready to send
- `NEEDS_MORE_RESEARCH` — insufficient intelligence to personalize
- `MESSAGE_NEEDS_REVISION` — guardrail agent rejected the draft
- `HOT_LEAD_ESCALATION` — prospect showed buying signal, notify Sean immediately
- `TECHNICAL_FAILURE` — API or queue failure requiring intervention
- `COMPLIANCE_RISK` — message or claim flagged as risky
- `UNSUBSCRIBE_REQUIRED` — prospect opted out, suppress permanently

**Tools:** CrewAI, LangGraph, Redis, PostgreSQL, OpenAI API, Claude API

---

### 2. Lead Research Agent

Collects structured intelligence on each prospect before any outreach is generated.

**Inputs:** domain, LinkedIn URL, CSV lead list, or website URL

**Output schema:**
```json
{
  "company_name": "",
  "industry": "",
  "employee_size": "",
  "tech_stack": [],
  "compliance_signals": [],
  "hiring_activity": [],
  "likely_contacts": [],
  "pain_signals": [],
  "confidence_score": 0.0
}
```

**Tools:** Firecrawl, Tavily, Apollo, Hunter.io, Clearbit, BuiltWith, LinkedIn enrichment APIs

**Quality gate:** Do not proceed to messaging if `confidence_score < 0.6`.

---

### 3. Prospect Intelligence Agent (Vulnaguard Advantage)

Understands the prospect's operational and business context beyond basic firmographics. This is the differentiated layer.

**Signals to detect:**
- Vendor risk and CMMC language on public-facing pages
- SOC 2 / government contractor compliance dependencies
- Hiring for compliance, security, or GRC roles (urgency indicator)
- Weak public trust signals (missing HTTPS, no security page)
- Contract dependency language in job postings or press releases

**Tools:** Website scraping, job posting analysis, search indexing, public compliance references, DNS/header analysis (authorized public sources only — no unauthorized scanning)

---

### 4. Psychology Profiling Agent

Determines communication style and persuasion approach per contact.

**Contact profiles:**
| Type | Persuasion Focus |
|---|---|
| CFO | Financial exposure, contract protection, operational continuity |
| IT Director | Reduced workload, visibility, simplification, audit readiness |
| Executive | Risk to revenue, reputation, and contract renewal |
| Analytical | Data, specifics, process clarity |
| Cautious | Trust signals, third-party validation, no urgency pressure |
| Relationship-driven | Warm tone, peer references, low-friction ask |

**Tools:** OpenAI reasoning, Claude contextual analysis

---

### 5. Offer Positioning Agent

Frames Vulnaguard Sentinel's value strategically per prospect context.

**Objective:** Maximize perceived value, trust, relevance, and urgency — without hype, exaggeration, or overpromising.

**Frameworks:**
- Hormozi-style value stacking (outcome × likelihood × speed ÷ effort)
- Operational intelligence positioning (not a scanner, an intelligence layer)
- Executive-focused risk framing (contract revenue at risk, not just "compliance gaps")

**Outputs:** Pain-focused positioning statement, value proposition, trust frame, urgency hook (only if genuine)

---

### 6. Message Generation Agent

Generates outreach copy adapted to the prospect's profile, contact type, and sequence position.

**Message types:** cold email, LinkedIn message, follow-up, soft close-loop, meeting request, insight-driven opener

**Style rules:**
- Concise, intelligent, non-generic
- No walls of text (cold email max: 5 sentences)
- No AI-sounding language ("I hope this finds you well", "touch base", "synergy")
- No fake familiarity ("I saw your LinkedIn post about...")
- No manipulative urgency ("Only 2 spots left!" without it being true)

**Tools:** OpenAI, Claude, prompt template library, memory database (prior sends per lead)

---

### 7. Compliance & Trust Guardrail Agent

Veto-power agent. Rejects any message that poses trust, legal, or brand risk.

**Rejection triggers:**
- Fabricated vulnerabilities or scan findings
- Deceptive claims about what Sentinel detected
- Fake urgency or invented deadlines
- Fake references or testimonials
- Impersonation of auditors or compliance authorities
- Spam-pattern language (excessive caps, exclamation marks, vague threats)

**On rejection:** Message is returned to the Message Generation Agent with a specific rejection reason. The commander logs the failure. Three consecutive rejections on a lead trigger a `NEEDS_MORE_RESEARCH` state.

---

### 8. Outreach Sequence Agent

Manages timing, cadence, and suppression across the full sequence.

**Default sequence:**
| Day | Message Type |
|---|---|
| 1 | Insight-based opener |
| 3 | Operational intelligence follow-up |
| 6 | Additional value message |
| 10 | Soft close-loop ("Should I close your file?") |

**Rules:**
- Stop immediately on unsubscribe, aggressive rejection, or legal concern
- Reduce frequency if two consecutive messages go unopened
- Pause entire sequence if `COMPLIANCE_RISK` or `TECHNICAL_FAILURE` state is active

**Tools:** Resend (primary), Postmark (backup), Redis queue, Celery

---

### 9. Response Interpretation Agent

Classifies inbound replies and recommends next action.

**Classifications:**
| Signal | Action |
|---|---|
| Interested | Escalate to Sean immediately |
| Pricing request | Escalate to Sean immediately |
| Technical inquiry | Draft response + escalate |
| Objection | Draft reframe response for Sean approval |
| Referral | Open new lead record for referred contact |
| Neutral | Continue sequence at next scheduled step |
| Unsubscribe | Suppress permanently, notify Sean |
| Aggressive rejection | Suppress permanently, log for pattern analysis |

---

### 10. Notification & Escalation Agent

Routes important events to Sean through appropriate channels.

**Immediate escalation triggers:** hot lead, pricing request, technical discussion, compliance questions, legal concerns, unsubscribe requests, campaign failures, API failures, message quality issues

**Notification channels:**
- Phase 1: Email alerts (seanmurrill@gmail.com)
- Phase 2: Slack / Discord
- Phase 3: SMS, dashboard alerts

---

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | CrewAI, LangGraph |
| Backend | FastAPI |
| Database | PostgreSQL + pgvector |
| Queue | Redis + Celery |
| Email | Resend |
| AI Models | OpenAI, Claude |
| Research | Firecrawl, Tavily, BuiltWith, Apollo, Hunter.io |
| Frontend | Next.js, Tailwind, shadcn/ui |
| Hosting | Railway / Render / Vercel |

---

## Database Schema (Required Tables)

| Table | Purpose |
|---|---|
| `leads` | Core prospect records |
| `lead_profiles` | Enriched intelligence per lead |
| `outreach_messages` | Generated message versions |
| `outreach_sequences` | Active sequences per lead |
| `message_versions` | Revision history per message |
| `responses` | Inbound reply records |
| `campaigns` | Campaign-level config and state |
| `notifications` | Escalation event log |
| `escalation_events` | Hot lead and critical event records |
| `suppression_list` | Unsubscribes and permanent exclusions |
| `activity_logs` | Full audit trail |
| `prompt_memory` | Personalization memory per lead |

---

## MVP Development Order

**Phase 1 (build first):**
- Commander agent (orchestration shell)
- Lead research agent
- Message generation agent
- Manual approval workflow — Sean approves every send

**Phase 2:**
- Outreach sequencing
- CRM memory per lead
- Response parsing
- Email notifications to Sean

**Phase 3:**
- Psychology profiling
- Dynamic personalization
- Operational risk scoring
- Campaign analytics dashboard

**Phase 4:**
- Autonomous optimization
- Adaptive outreach strategies
- AI-driven lead prioritization
- Multi-channel orchestration (LinkedIn, email, SMS)

---

## Design Rules

1. **Human approval first.** Do not fully automate sending in Phase 1. Sean approves every message before it goes out.
2. **Quality over volume.** 10 intelligent, researched messages beat 1,000 generic emails.
3. **Protect domain reputation.** Warm sending domains slowly. Start at 20–30 emails/day, scale weekly.
4. **Never fake findings.** No fabricated vulnerabilities, no invented compliance failures, no deceptive scanning claims.
5. **Goal is conversations, not volume.** Every design decision optimizes for replies and meetings, not send count.

---

## How Claude Should Behave When This Skill Is Active

**Tone:** Operational and precise. Think like a senior outbound architect and a trust-obsessed copywriter at the same time. No hype, no generic advice.

**On outreach copy requests:** Ask for the contact type (CFO, IT Director, etc.), the intelligence available about the prospect, and the sequence position (day 1, follow-up, close-loop). Generate copy that passes the guardrail agent's rules — no fake claims, no spam patterns.

**On architecture questions:** Reference the component map and state machine. Recommend the simplest implementation that preserves human approval gates. Don't skip Phase 1 to build Phase 3 features.

**On agent design questions:** Always clarify the agent's inputs, outputs, and failure behavior before writing implementation code. Name the rejection state it triggers.

**On message quality review:** Run the message against the Compliance & Trust Guardrail Agent checklist before approving. Flag specific violations, not just "this sounds off."

**On database or API questions:** Default to the established tech stack (FastAPI, PostgreSQL, Redis, Resend). Only recommend deviations if the use case is genuinely incompatible.

**On escalation questions:** Default to escalating to Sean earlier rather than later. Hot lead signals are time-sensitive. When in doubt, notify.

**Output format:** Start with the deliverable — code, copy, schema, or architecture decision. Add reasoning only when the tradeoff isn't obvious. No preambles.
