# Skill: Onboarding Agent — Sentinel-CMMC

## When to Use This Skill

Invoke this skill when the user asks for help with any of the following:
- Designing or improving the product onboarding flow
- Building a homepage demo or interactive product tour
- Structuring a live or recorded sales demo
- Creating test/trial flows for prospects
- Writing FAQ content for onboarding screens or help docs
- Reducing drop-off between signup and activation
- Planning the post-signup email or in-app sequence
- Evaluating what's working or broken in the current onboarding

Trigger phrase: `/onboarding-agent` or any request related to user onboarding, demos, activation, or reducing time-to-value in Sentinel-CMMC.

---

## Research Foundation

This skill is built from analysis of 67 SaaS onboarding flows ("I Tried 67 SaaS Onboarding Flows, Here's What Actually Works") combined with teardowns of 36+ products from UserGuiding, Supademo, and DesignRevision. The patterns below are validated across product-led and sales-led B2B products.

---

## Core Framework: Three Evaluation Signals

Use these three metrics to evaluate and design every onboarding touchpoint:

1. **Time-to-Value (TTV)** — How long until the user sees something real and relevant? Target: under 5 minutes for self-serve, under 30 minutes for guided onboarding.
2. **Activation Event** — The single action that signals the user "got it." For Sentinel, this is: *viewing a control gap linked to a specific contract risk*. Everything before this moment is pre-activation.
3. **Friction Ratio** — Every step between signup and activation that doesn't move the user toward the activation event is friction. Audit mercilessly.

---

## Three-Phase Onboarding Model

### Phase 1 — Orient (0–60 seconds)
Goal: answer "is this for me?" and eliminate decision paralysis.

- Welcome screen leads with a specific business outcome, not a product feature
- One clear CTA with a time signal ("See your readiness snapshot in 5 minutes")
- Ask one segmentation question: "What's your primary goal?" with options like:
  - Prepare for an upcoming CMMC assessment
  - Understand which contracts are at risk
  - Track compliance controls across our environment
  - Show leadership our readiness status
- The answer routes users into a personalized flow — show them relevant defaults

### Phase 2 — Activate (1–10 minutes)
Goal: reach the activation event — showing a control gap tied to a contract risk.

- Pre-fill a sample environment with realistic (anonymized) data so users don't face a blank state
- Walk users through one flow, not all features: Findings → Controls → Readiness → Contract Risk
- Use interactive walkthroughs (user performs real actions) over passive slideshows
- Celebrate the activation moment explicitly: "You can now see which gaps put contract revenue at risk."
- Progress: show "Step 2 of 4" — completion rates improve 30–50% with visible progress

### Phase 3 — Reinforce (Day 1–7)
Goal: prevent the second wave of churn by showing continued value.

- 5–7 item checklist after activation (not before): things like "Upload your current scan", "Invite your compliance lead", "Generate your executive report"
- Contextual tooltips triggered by behavior (hover or inaction), not on page load
- 3-email sequence: Day 1 recap of what they found, Day 3 "here's the next step", Day 7 executive report preview
- At Day 3, surface the most alarming gap they have — make the value undeniable

---

## Homepage Demo Flow

The homepage demo is the first conversion touchpoint. It must answer "what does this actually do?" in under 90 seconds without requiring a login.

### Structure

**Hero Section**
- Headline: outcome-first, not product-first
  - Use: "Know which cyber gaps are putting your contracts at risk"
  - Avoid: "Vulnaguard Sentinel — the compliance intelligence platform"
- Sub-headline: name the problem precisely ("Most contractors have scans. Few have readiness clarity.")
- Single CTA above the fold: "See a live demo" or "Try it with sample data" (not "Sign up")
- Social proof near CTA: number of contractors assessed, or one short quote

**Interactive Demo Widget**
- Embed a Supademo-style interactive walkthrough (no login required)
- 4–5 screens max: Dashboard → Control Gap → Contract Risk → Executive Report
- Let the visitor click through at their own pace — no auto-advance
- End screen: "This is what you'd see for your environment — start your pilot"

**Below the Fold**
- "How it works" — three steps, plain language: Import → Analyze → Report
- Two use-case examples: "Preparing for a CMMC assessment" and "Briefing an executive on contract risk"
- Exit-intent modal: if visitor tries to leave, show "See a 2-minute walkthrough first"

### What to Avoid
- Autoplaying product videos (people skip them)
- Feature lists before establishing the problem
- Long forms before delivering any value
- Generic messaging ("comprehensive compliance platform")

---

## Test Flow (Self-Serve Trial)

The test flow allows a prospect to explore Sentinel with pre-loaded sample data before committing to a pilot.

### Design Principles

**Value before signup where possible**
- Let visitors view the sample dashboard before entering an email
- Require only an email to unlock the editable sample environment
- Full account creation comes after the user has seen their first meaningful output

**Blank-state elimination**
- Pre-load a sample defense contractor profile with:
  - 12 control gaps (mix of Critical, High, Medium)
  - 2 mock active contracts with associated risk scores
  - One ready-to-export executive summary
- First view should never be an empty state asking "where do I start?"

**Build-first, sign-up later**
- Allow users to run a mock remediation ranking before asking for their real data
- Gate only the "export" and "invite team" actions behind account creation
- Auth wall positioned at the moment of value, not before

### Test Flow Steps

1. **Landing** — Prospect clicks "Try it with sample data" from homepage
2. **Instant access** — Load the sample dashboard (no login)
3. **Guided moment** — Tooltip on first load: "This is a Defense Manufacturing subcontractor with 3 active contracts. Click any gap to see its contract risk."
4. **Aha moment** — User clicks a Critical gap and sees it's blocking a specific contract renewal
5. **Soft gate** — "Want to run this on your own environment? Enter your email to continue."
6. **Activation** — After email, show a 3-step checklist to import real data

### Measuring Test Flow Performance
- Track: % who reach step 4 (aha moment), % who enter email after step 4, % who complete real data import
- If drop-off is at step 2 or 3, the sample data isn't compelling enough — make the risk more concrete
- If drop-off is at the email gate, move the gate later or ask for less information

---

## Demo Flow (Live Sales Demo)

Use this for discovery calls, pilot kickoffs, and recorded leave-behind demos.

### Demo Philosophy
Show outcomes, not features. Every screen shown should be prefaced with a business problem, not a product capability.

### Live Demo Script (25–30 minutes)

**Opening (3 min)**
- "Before I share my screen — what's the one thing you're most hoping to see today?"
- Listen for: contract pressure, executive reporting need, manual process pain
- Tailor the demo to what they said — don't run a canned sequence

**Act 1 — The Problem Made Visible (5 min)**
- Open on the Control Gap Summary
- "This is what a typical assessment gap looks like — 23 controls with partial or missing implementation"
- Point out two or three gaps. Ask: "Do any of these sound familiar?"
- Goal: make them feel seen, not sold to

**Act 2 — The Connection to Revenue (8 min)**
- Navigate to Contract Eligibility view
- "Now here's what most tools don't show you — which of these gaps are actually blocking contracts"
- Walk through one contract at risk: which controls are failing, what the remediation priority is
- Ask: "If you had this view today, what would you do differently?"

**Act 3 — The Executive Layer (7 min)**
- Open the Executive Report preview
- "This is what goes to leadership or your assessment auditor — no technical jargon, just: readiness score, at-risk contracts, fix priority"
- Let them read it for 30 seconds before you speak
- "Would your CEO or ops lead find this useful?"

**Close (5 min)**
- "Based on what you saw — what's the most valuable thing here for your situation?"
- Listen before pitching
- Transition to pilot if qualified: "We run focused 90-day pilots — [X] spots left. Want to talk scope?"

### Recorded Demo (Leave-Behind)
- Maximum 8 minutes
- Voice-over with screen recording (Loom or Tella)
- Chapters: 0:00 Intro, 1:30 Control Gaps, 3:30 Contract Risk, 5:30 Executive Report, 7:00 How the Pilot Works
- End with a direct CTA: "Book a 15-minute call to see this on your own data"
- Send via direct link, not attachment — track opens

---

## FAQ Section

### Where to Surface FAQs

| Location | FAQ Type | Trigger |
|---|---|---|
| Onboarding checklist | "What do I do next?" | After activation event |
| Control Gap view | "What does this mean?" | On hover of unfamiliar term |
| Contract Risk view | "How is risk calculated?" | First visit to this screen |
| Executive Report | "Who should receive this?" | Before export action |
| Empty states | "How do I get started?" | When no data has been imported |

### Core FAQ Content

**Getting Started**

*What does Sentinel actually do?*
It imports your security findings, maps them to NIST 800-171 and CMMC controls, and shows you which gaps are affecting your readiness score and your contract eligibility — with an executive report you can share with leadership or auditors.

*How long does setup take?*
Seeing your readiness snapshot takes under 10 minutes once you import your first environment. Full integration with your scan tool takes 1–2 hours with our support team.

*Do I need technical knowledge to use this?*
No. The interface is built for compliance leads, ops leaders, and executives — not just security engineers. Technical findings are translated into business language automatically.

**Compliance and Controls**

*Which frameworks does Sentinel cover?*
Currently: NIST SP 800-171 Rev 2, CMMC Level 1 and Level 2. NIST CSF and FedRAMP mapping is on the roadmap.

*What's the difference between a "gap" and a "finding"?*
A finding is a raw technical result from a scan tool. A gap is a finding that has been mapped to a specific control — meaning it's not just a security issue, it's a compliance issue with a defined remediation requirement.

*How is the readiness score calculated?*
Each control is weighted by its impact on CMMC Level 2 assessment. Controls mapped to high-risk domains (Access Control, Incident Response, Configuration Management) carry higher weight. The score reflects the percentage of controls with at least partial implementation.

**Contracts and Risk**

*How does Sentinel know which contracts are at risk?*
During setup, you tell us which contracts you're pursuing or currently holding and their associated compliance requirements. Sentinel maps your control gaps against those requirements and flags any that would cause an assessment failure or eligibility issue.

*What if I have multiple contracts with different requirements?*
Each contract gets its own risk view. You can compare readiness across contracts and prioritize gaps that affect the most critical revenue.

**Pilot Questions**

*What's included in the 90-day pilot?*
One environment, full scan import, readiness snapshot, control gap summary, contract eligibility review, revenue-at-risk summary, monthly executive report, and a prioritized remediation roadmap.

*What happens after the pilot?*
We present a 90-day outcomes review against your agreed success metrics and propose a renewal structure. Pilot customers who convert to annual contracts receive 3 months' credit toward their first year.

*Can we add more environments during the pilot?*
The pilot scope is intentionally limited to one environment to ensure depth over breadth. Additional environments can be added at renewal.

---

## Activation Benchmarks

Use these as targets when evaluating Sentinel's onboarding performance:

| Metric | Target |
|---|---|
| Test flow aha-moment rate | >60% of visitors reach "contract risk" screen |
| Email capture rate (test flow) | >40% of aha-moment viewers |
| Activation rate (pilot signup) | 40–60% of qualified prospects who see a live demo |
| Onboarding checklist completion | 65–85% within first 7 days |
| Time to first executive report | <10 minutes from data import |
| 7-day retention | >75% still active after first week |

---

## Anti-Patterns to Avoid

- **Feature-led demos**: opening with "here's everything Sentinel can do" before establishing the specific problem
- **Empty state first impressions**: showing a blank dashboard before any sample data is loaded
- **Front-loading the FAQ**: hiding answers inside a help center instead of surfacing them contextually
- **Mandatory tours**: forcing new users through a linear walkthrough before they've seen the value
- **Email overload**: more than 3 emails in the first 7 days; focus on behavior-triggered, not time-triggered
- **Jargon in executive outputs**: control IDs and technical severity ratings in reports meant for CEOs
- **Asking for too much upfront**: requesting full environment access before showing sample output

---

## How Claude Should Behave When This Skill Is Active

**Tone**: Practical and specific. Think like a product designer who has studied onboarding obsessively and a salesperson who knows what actually converts.

**On demo requests**: Ask first — live demo, recorded walkthrough, or homepage widget? Then tailor the script or structure accordingly. Always anchor demos to the prospect's stated problem before diving into product.

**On FAQ requests**: Ask where it will appear (onboarding screen, help doc, sales page) and who the reader is (new user, executive, auditor). Surface answers at the right depth for the audience.

**On flow design questions**: Reference the three-phase model (Orient → Activate → Reinforce) and always ask: what is the activation event we're optimizing toward?

**On conversion problems**: Start with friction ratio — where are users dropping off and why? Then recommend one targeted fix before proposing a full redesign.

**On test flow or trial design**: Default to "value before signup" and "blank-state elimination." Make the sample data feel like the prospect's own situation.

**Output format**: Start with the deliverable (draft, script, framework, screen copy), then explain the reasoning briefly if it adds value. No lengthy preambles. Reference specific frameworks by name so the user can trace the logic.
