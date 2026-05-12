# Sentinel Growth Commander Architecture

This project is configured as a CrewAI Flow that wraps a full outbound command
crew. The flow is deployable through the CrewAI CLI, while the supporting stack
files define the services needed for production build-out.

## Agent Map

| Layer | Agents |
|---|---|
| Commander | Sentinel Growth Commander |
| Research | Lead Research Agent, Enrichment Agent, Prospect Intelligence Agent, Risk Context Agent |
| Persuasion | Psychology Profiling Agent, Offer Positioning Agent, CTA Optimization Agent, Message Generation Agent |
| Safety | Compliance and Trust Guardrail Agent |
| Operations | Outreach Sequence Agent, Response Interpretation Agent, Notification and Escalation Agent, Campaign Health Agent |

## State Machine

- `APPROVED_TO_CONTACT`
- `NEEDS_MORE_RESEARCH`
- `MESSAGE_NEEDS_REVISION`
- `HOT_LEAD_ESCALATION`
- `TECHNICAL_FAILURE`
- `COMPLIANCE_RISK`
- `UNSUBSCRIBE_REQUIRED`

## Tooling

`config/tooling.yaml` maps tools and providers to the agents that use them.
Provider API keys live in `.env` and are documented in `.env.example`.

## Persistence

`db/schema.sql` defines the required Postgres/pgvector tables:

- `leads`
- `lead_profiles`
- `outreach_messages`
- `outreach_sequences`
- `message_versions`
- `responses`
- `campaigns`
- `notifications`
- `escalation_events`
- `suppression_list`
- `activity_logs`
- `prompt_memory`

## Local Services

Use Docker Compose for local Postgres and Redis:

```bash
docker compose up -d
```

The current CrewAI flow produces the outbound command plan and does not send
email automatically. That preserves the Phase 1 human-approval rule.

