"""Sentinel Growth Commander — event-driven agentic flow.

Sean provides the minimum to get started. Agents research and discover
everything else autonomously.

Three events map to three business situations:

  new_lead          Sean enters a company name and domain.
                    Agents research the company, identify the right contact,
                    build an intelligence profile, write and compliance-check
                    the message, plan the sequence, and hand Sean the approved
                    outreach package for final send approval.

  response_received An inbound reply arrives.
                    Agents classify it, log it, and alert Sean if it requires
                    immediate action (hot lead, pricing request, legal, etc.).

  health_check      Campaign health audit.
                    Agents check metrics, detect deliverability or quality
                    issues, and alert Sean if anything needs attention.

Set EVENT_TYPE env var or pass via payload. Defaults to new_lead.
"""

from __future__ import annotations

import os

from crewai import Crew, Process
from crewai.flow import Flow, listen, router, start
from pydantic import BaseModel, Field

from cold_outreach_flow.crews.growth_crew.growth_crew import GrowthCrew


# ---------------------------------------------------------------------------
# Flow state — ONLY real user inputs. No internal / output fields.
# The platform UI exposes every field here, so keep this list minimal.
# ---------------------------------------------------------------------------

class OutreachFlowState(BaseModel):
    # ── Routing ────────────────────────────────────────────────────────────
    event_type: str = Field(
        default="new_lead",
        description="new_lead | response_received | health_check",
    )

    # ── new_lead inputs ────────────────────────────────────────────────────
    company_name: str = Field(
        default="",
        description="Target company name (required for new_lead)",
    )
    company_domain: str = Field(
        default="",
        description="Company domain or website — agents will search if blank",
    )
    contact_name: str = Field(
        default="",
        description="Known contact name — agents will find the best contact if blank",
    )
    channel: str = Field(
        default="email",
        description="Outreach channel: email or linkedin",
    )
    known_context: str = Field(
        default="",
        description="Any notes you already have about this prospect (optional)",
    )

    # ── response_received inputs ───────────────────────────────────────────
    inbound_reply: str = Field(
        default="",
        description="Full text of the inbound reply (for response_received event)",
    )
    reply_from_email: str = Field(
        default="",
        description="Email address of the person who replied",
    )

    # ── health_check inputs ────────────────────────────────────────────────
    campaign_id: str = Field(
        default="",
        description="Specific campaign ID to audit — leave blank to check all",
    )


# ---------------------------------------------------------------------------
# Flow
# ---------------------------------------------------------------------------

class ColdOutreachFlow(Flow[OutreachFlowState]):
    """Sentinel Growth Commander — runs the full outbound intelligence cycle."""

    # ------------------------------------------------------------------
    # Entry point — load inputs from payload or environment
    # ------------------------------------------------------------------

    @start()
    def load_inputs(self, crewai_trigger_payload: dict | None = None) -> str:
        p = crewai_trigger_payload or {}

        self.state.event_type    = p.get("event_type",    os.getenv("EVENT_TYPE",    "new_lead"))
        self.state.company_name  = p.get("company_name",  os.getenv("COMPANY_NAME",  ""))
        self.state.company_domain= p.get("company_domain",os.getenv("COMPANY_DOMAIN",""))
        self.state.contact_name  = p.get("contact_name",  os.getenv("CONTACT_NAME",  ""))
        self.state.channel       = p.get("channel",       os.getenv("CHANNEL",       "email"))
        self.state.known_context = p.get("known_context", os.getenv("KNOWN_CONTEXT", ""))

        self.state.inbound_reply    = p.get("inbound_reply",    os.getenv("INBOUND_REPLY",    ""))
        self.state.reply_from_email = p.get("reply_from_email", os.getenv("REPLY_FROM_EMAIL", ""))

        self.state.campaign_id = p.get("campaign_id", os.getenv("CAMPAIGN_ID", ""))

        return self.state.event_type

    # ------------------------------------------------------------------
    # Router — dispatch to the correct path
    # ------------------------------------------------------------------

    @router(load_inputs)
    def dispatch(self, event_type: str) -> str:
        if event_type == "response_received":
            return "response_received"
        if event_type == "health_check":
            return "health_check"
        return "new_lead"

    # ------------------------------------------------------------------
    # Path 1: new_lead
    # Full 13-agent hierarchical pipeline. Agents discover everything.
    # ------------------------------------------------------------------

    @listen("new_lead")
    def process_new_lead(self) -> str:
        if not self.state.company_name:
            return "ERROR: company_name is required to process a new lead."

        result = GrowthCrew().crew().kickoff(inputs=self._lead_inputs())
        print("\nSentinel outreach plan written to output/sentinel_outreach_plan.md")
        return result.raw

    # ------------------------------------------------------------------
    # Path 2: response_received
    # 2-agent crew: classify the reply, log it, alert Sean if urgent.
    # ------------------------------------------------------------------

    @listen("response_received")
    def process_response(self) -> str:
        if not self.state.inbound_reply:
            return "ERROR: inbound_reply is required for response_received event."

        gc = GrowthCrew()
        crew = Crew(
            agents=[
                gc.response_interpretation_agent(),
                gc.notification_escalation_agent(),
            ],
            tasks=[
                gc.response_interpretation_task(),
                gc.notification_escalation_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff(inputs=self._response_inputs())
        print("\nResponse processed.")
        return result.raw

    # ------------------------------------------------------------------
    # Path 3: health_check
    # 2-agent crew: audit metrics, alert Sean if action is needed.
    # ------------------------------------------------------------------

    @listen("health_check")
    def run_health_check(self) -> str:
        gc = GrowthCrew()
        crew = Crew(
            agents=[
                gc.campaign_health_agent(),
                gc.notification_escalation_agent(),
            ],
            tasks=[
                gc.campaign_health_task(),
                gc.notification_escalation_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff(inputs=self._health_inputs())
        print("\nHealth check complete.")
        return result.raw

    # ------------------------------------------------------------------
    # Crew input builders
    # All template variables used in agents.yaml / tasks.yaml must appear
    # here with sensible defaults so agents always have something to work
    # from even when the human provided minimal input.
    # ------------------------------------------------------------------

    def _lead_inputs(self) -> dict:
        name = self.state.company_name
        domain = self.state.company_domain or f"[research {name}'s domain]"
        contact = self.state.contact_name or "[research the best contact at this company]"
        context = self.state.known_context or "No prior context. Full research required."
        return {
            # core identifiers
            "company_name":    name,
            "company_domain":  domain,
            "contact_name":    contact,
            "channel":         self.state.channel or "email",
            "known_context":   context,
            # fields agents must discover — provided as placeholders so
            # task/agent YAML templates always resolve without error
            "contact_role":    "[to be discovered by Lead Research Agent]",
            "sequence_position": "day_1_initial_outreach",
            "primary_goal": (
                "Book a 15-minute discovery call for the 90-Day Sentinel-CMMC "
                "Compliance Intelligence Pilot ($3,000/month). If CMMC is not "
                "the primary fit, identify the most relevant compliance or "
                "operational risk angle for this prospect."
            ),
        }

    def _response_inputs(self) -> dict:
        return {
            "company_name":    self.state.company_name  or "[unknown — research from reply context]",
            "company_domain":  self.state.company_domain or "",
            "contact_name":    self.state.contact_name  or "[identify from reply]",
            "contact_role":    "[identify from reply context]",
            "channel":         self.state.channel       or "email",
            "known_context":   self.state.known_context or "",
            "inbound_reply":   self.state.inbound_reply,
            "reply_from_email": self.state.reply_from_email or "",
            "sequence_position": "response_received",
            "primary_goal": "Classify this reply, log it, and alert Sean immediately if escalation is required.",
        }

    def _health_inputs(self) -> dict:
        scope = "all active campaigns" if not self.state.campaign_id else f"campaign {self.state.campaign_id}"
        return {
            "company_name":    "[campaign health check — no single prospect]",
            "company_domain":  "",
            "contact_name":    "[n/a]",
            "contact_role":    "[n/a]",
            "channel":         "all",
            "known_context":   f"Health check scope: {scope}",
            "campaign_id":     self.state.campaign_id or "all",
            "sequence_position": "health_check",
            "primary_goal": (
                "Audit campaign health. Check domain reputation, deliverability, "
                "engagement rates, suppression events, and API failures. "
                "Alert Sean immediately if any metric crosses a critical threshold."
            ),
        }


# ---------------------------------------------------------------------------
# CLI entry points
# ---------------------------------------------------------------------------

def kickoff() -> None:
    """Default entry point — new_lead pipeline."""
    ColdOutreachFlow().kickoff()


def kickoff_response(
    inbound_reply: str,
    company_name: str = "",
    contact_name: str = "",
    reply_from_email: str = "",
) -> None:
    """Process an inbound reply."""
    ColdOutreachFlow().kickoff(inputs={
        "event_type":        "response_received",
        "inbound_reply":     inbound_reply,
        "company_name":      company_name,
        "contact_name":      contact_name,
        "reply_from_email":  reply_from_email,
    })


def kickoff_health_check(campaign_id: str = "") -> None:
    """Run a campaign health check."""
    ColdOutreachFlow().kickoff(inputs={
        "event_type":   "health_check",
        "campaign_id":  campaign_id,
    })


def plot() -> None:
    ColdOutreachFlow().plot()


if __name__ == "__main__":
    kickoff()
