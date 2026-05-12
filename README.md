# Cold Outreach CrewAI Flow

CrewAI Flow for Sentinel-CMMC outbound growth operations. It converts the Claude skill guidance in `.claude/skills/` into an agentic workflow that researches a prospect, enriches intelligence, frames the offer, drafts outreach, reviews it for trust/compliance risk, plans follow-up operations, and escalates important events.

## Project Layout

```text
.claude/skills/                         Source Claude skill files
config/tooling.yaml                     Tool/provider map by agent
db/schema.sql                           PostgreSQL + pgvector schema
docker-compose.yml                      Local PostgreSQL and Redis
docs/architecture.md                    System architecture notes
src/cold_outreach_flow/main.py          Flow entrypoint
src/cold_outreach_flow/crews/growth_crew/
  growth_crew.py                        Crew wiring
  config/agents.yaml                    Agent definitions
  config/tasks.yaml                     Task workflow
.env.example                            Environment template
pyproject.toml                          CrewAI CLI/project config
```

## Local Setup

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY plus any provider keys you want enabled
pip install crewai
crewai install
crewai run
```

Optional local services:

```bash
docker compose up -d
```

You can also run the script entrypoint directly after install:

```bash
kickoff
```

The flow writes the final plan to `output/sentinel_outreach_plan.md`.

## Configured Agents

- Sentinel Growth Commander
- Lead Research Agent
- Enrichment Agent
- Prospect Intelligence Agent
- Risk Context Agent
- Psychology Profiling Agent
- Offer Positioning Agent
- CTA Optimization Agent
- Message Generation Agent
- Compliance and Trust Guardrail Agent
- Outreach Sequence Agent
- Response Interpretation Agent
- Notification and Escalation Agent
- Campaign Health Agent

## Configured Stack

- Core orchestration: CrewAI, LangGraph
- Backend: FastAPI
- Database: PostgreSQL, pgvector
- Queue: Redis, Celery
- Email: Resend, Postmark, SendGrid
- AI models: OpenAI, Claude
- Research: Firecrawl, Tavily, BuiltWith, Apollo, Hunter.io, Clearbit, LinkedIn enrichment
- Frontend target: Next.js, Tailwind, shadcn/ui
- Hosting targets: Railway, Render, Vercel, CrewAI AMP

## Change Prospect Inputs

Set these in `.env` before running:

```bash
COMPANY_NAME="Acme Defense Systems"
CONTACT_NAME="Jane Smith"
CONTACT_ROLE="COO"
COMPANY_DOMAIN="acmedefense.example"
CHANNEL="email"
SEQUENCE_POSITION="day_1"
PRIMARY_GOAL="Book a 15-minute discovery call for the 90-day pilot."
KNOWN_CONTEXT="50-person defense subcontractor preparing for CMMC Level 2."
```

CrewAI AMP trigger payloads can also pass those same keys when deployed.

## Plot The Flow

```bash
crewai flow plot
# or
plot
```

## Deploy With CrewAI CLI

CrewAI deploys crews and flows to AMP from a GitHub-backed project.

```bash
crewai login
crewai deploy create
crewai deploy status
crewai deploy logs
```

After code changes:

```bash
crewai deploy push
```

Useful management commands:

```bash
crewai deploy list
crewai deploy remove <deployment_id>
```

## Notes

- Keep real secrets in `.env`, not in Git.
- The first version intentionally keeps sending human-approved. It drafts and recommends; it does not send email.
- The compliance guardrail task rejects fake findings, fake urgency, invented references, and scanner-like claims.
