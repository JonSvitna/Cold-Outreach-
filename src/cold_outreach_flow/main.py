"""Sentinel Growth Commander — event-driven agentic flow.

Three entry points map to three business events:

  new_lead          Full pipeline: research → positioning → message → compliance
                    → sequence plan → notifications. Commander manages all agents.

  response_received Classify an inbound reply, log it, escalate to Sean if needed.

  health_check      Query campaign metrics, detect issues, alert Sean if critical.

Trigger via env var or payload:
  EVENT_TYPE=new_lead           (default)
  EVENT_TYPE=response_received
  EVENT_TYPE=health_check
"""

from __future__ import annotations

import os

from crewai import Agent, Crew, Process, Task
from crewai.flow import Flow, listen, router, start
from pydantic import BaseModel

from cold_outreach_flow.crews.growth_crew.growth_crew import GrowthCrew
from cold_outreach_flow.tools.data_tools import get_data_write_tools
from cold_outreach_flow.tools.notification_tools import get_notification_tools


# ---------------------------------------------------------------------------
# Flow state
# ---------------------------------------------------------------------------

class OutreachFlowState(BaseModel):
    # Routing
    event_type: str = "new_lead"

    # new_lead fields
    company_name: str = ""
    contact_name: str = ""
    contact_role: str = ""
    company_domain: str = ""
    channel: str = ""
    sequence_position: str = ""
    primary_goal: str = ""
    known_context: str = ""

    # response_received fields
    inbound_reply: str = ""
    reply_from_email: str = ""
    reply_message_id: str = ""

    # health_check fields
    campaign_id: str = ""
    health_check_scope: str = "all"  # all | domain | sequences | responses

    # Shared output
    final_plan: str = ""
    escalation_required: bool = False
    escalation_summary: str = ""


# ---------------------------------------------------------------------------
# Flow
# ---------------------------------------------------------------------------

class ColdOutreachFlow(Flow[OutreachFlowState]):
    """Stateful event-driven wrapper around the Sentinel agent crews."""

    # ------------------------------------------------------------------
    # Entry point — load inputs, determine route
    # ------------------------------------------------------------------

    @start()
    def load_inputs(self, crewai_trigger_payload: dict | None = None) -> str:
        payload = crewai_trigger_payload or {}

        self.state.event_type = payload.get(
            "event_type", os.getenv("EVENT_TYPE", "new_lead")
        )

        # new_lead
        self.state.company_name = payload.get(
            "company_name", os.getenv("COMPANY_NAME", "Example Defense Manufacturing")
        )
        self.state.contact_name = payload.get(
            "contact_name", os.getenv("CONTACT_NAME", "Pat Prospect")
        )
        self.state.contact_role = payload.get(
            "contact_role", os.getenv("CONTACT_ROLE", "COO")
        )
        self.state.company_domain = payload.get(
            "company_domain", os.getenv("COMPANY_DOMAIN", "example.com")
        )
        self.state.channel = payload.get("channel", os.getenv("CHANNEL", "email"))
        self.state.sequence_position = payload.get(
            "sequence_position", os.getenv("SEQUENCE_POSITION", "day_1")
        )
        self.state.primary_goal = payload.get(
            "primary_goal",
            os.getenv(
                "PRIMARY_GOAL",
                "Book a 15-minute discovery call for the 90-day Sentinel-CMMC pilot.",
            ),
        )
        self.state.known_context = payload.get(
            "known_context",
            os.getenv(
                "KNOWN_CONTEXT",
                "Small GovCon subcontractor pursuing CMMC Level 2 readiness; "
                "likely using spreadsheets for readiness tracking.",
            ),
        )

        # response_received
        self.state.inbound_reply = payload.get(
            "inbound_reply", os.getenv("INBOUND_REPLY", "")
        )
        self.state.reply_from_email = payload.get(
            "reply_from_email", os.getenv("REPLY_FROM_EMAIL", "")
        )
        self.state.reply_message_id = payload.get(
            "reply_message_id", os.getenv("REPLY_MESSAGE_ID", "")
        )

        # health_check
        self.state.campaign_id = payload.get(
            "campaign_id", os.getenv("CAMPAIGN_ID", "")
        )
        self.state.health_check_scope = payload.get(
            "health_check_scope", os.getenv("HEALTH_CHECK_SCOPE", "all")
        )

        return self.state.event_type

    # ------------------------------------------------------------------
    # Router — dispatch to the correct flow path
    # ------------------------------------------------------------------

    @router(load_inputs)
    def dispatch(self, event_type: str) -> str:
        if event_type == "response_received":
            return "response_received"
        if event_type == "health_check":
            return "health_check"
        return "new_lead"

    # ------------------------------------------------------------------
    # Path 1: new_lead — full hierarchical pipeline
    # ------------------------------------------------------------------

    @listen("new_lead")
    def process_new_lead(self) -> str:
        result = GrowthCrew().crew().kickoff(inputs=self._lead_inputs())
        self.state.final_plan = result.raw
        print(
            f"\nSentinel outreach plan written to output/sentinel_outreach_plan.md\n"
            f"Final state: {self.state.event_type}"
        )
        return self.state.final_plan

    # ------------------------------------------------------------------
    # Path 2: response_received — classify reply, log it, escalate if needed
    # ------------------------------------------------------------------

    @listen("response_received")
    def process_response(self) -> str:
        crew_instance = GrowthCrew()

        response_crew = Crew(
            agents=[
                crew_instance.response_interpretation_agent(),
                crew_instance.notification_escalation_agent(),
            ],
            tasks=[
                crew_instance.response_interpretation_task(),
                crew_instance.notification_escalation_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )

        result = response_crew.kickoff(inputs=self._response_inputs())
        self.state.final_plan = result.raw

        if any(
            word in result.raw.lower()
            for word in ("interested", "pricing", "technical", "legal", "compliance")
        ):
            self.state.escalation_required = True
            self.state.escalation_summary = result.raw[:500]

        print(
            f"\nResponse processed."
            f" Escalation required: {self.state.escalation_required}"
        )
        return self.state.final_plan

    # ------------------------------------------------------------------
    # Path 3: health_check — campaign monitoring + alert if critical
    # ------------------------------------------------------------------

    @listen("health_check")
    def run_health_check(self) -> str:
        crew_instance = GrowthCrew()

        health_crew = Crew(
            agents=[
                crew_instance.campaign_health_agent(),
                crew_instance.notification_escalation_agent(),
            ],
            tasks=[
                crew_instance.campaign_health_task(),
                crew_instance.notification_escalation_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )

        result = health_crew.kickoff(inputs=self._health_inputs())
        self.state.final_plan = result.raw
        print(f"\nHealth check complete.")
        return self.state.final_plan

    # ------------------------------------------------------------------
    # Input helpers
    # ------------------------------------------------------------------

    def _lead_inputs(self) -> dict:
        return {
            "company_name": self.state.company_name,
            "contact_name": self.state.contact_name,
            "contact_role": self.state.contact_role,
            "company_domain": self.state.company_domain,
            "channel": self.state.channel,
            "sequence_position": self.state.sequence_position,
            "primary_goal": self.state.primary_goal,
            "known_context": self.state.known_context,
        }

    def _response_inputs(self) -> dict:
        return {
            "company_name": self.state.company_name,
            "contact_name": self.state.contact_name,
            "contact_role": self.state.contact_role,
            "company_domain": self.state.company_domain,
            "channel": self.state.channel,
            "sequence_position": self.state.sequence_position,
            "inbound_reply": self.state.inbound_reply,
            "reply_from_email": self.state.reply_from_email,
            "reply_message_id": self.state.reply_message_id,
            "primary_goal": self.state.primary_goal,
            "known_context": self.state.known_context,
        }

    def _health_inputs(self) -> dict:
        return {
            "company_name": self.state.company_name,
            "campaign_id": self.state.campaign_id,
            "health_check_scope": self.state.health_check_scope,
            "contact_name": self.state.contact_name,
            "contact_role": self.state.contact_role,
            "company_domain": self.state.company_domain,
            "channel": self.state.channel,
            "sequence_position": self.state.sequence_position,
            "primary_goal": self.state.primary_goal,
            "known_context": self.state.known_context,
        }


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def kickoff() -> None:
    ColdOutreachFlow().kickoff()


def kickoff_response(
    inbound_reply: str,
    company_name: str = "",
    contact_name: str = "",
    reply_from_email: str = "",
) -> None:
    """Convenience entry point for processing an inbound reply."""
    ColdOutreachFlow().kickoff(inputs={
        "event_type": "response_received",
        "inbound_reply": inbound_reply,
        "company_name": company_name,
        "contact_name": contact_name,
        "reply_from_email": reply_from_email,
    })


def kickoff_health_check(campaign_id: str = "", scope: str = "all") -> None:
    """Convenience entry point for a campaign health check."""
    ColdOutreachFlow().kickoff(inputs={
        "event_type": "health_check",
        "campaign_id": campaign_id,
        "health_check_scope": scope,
    })


def plot() -> None:
    ColdOutreachFlow().plot()


if __name__ == "__main__":
    kickoff()
