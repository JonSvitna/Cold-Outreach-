from __future__ import annotations

import os

from crewai.flow import Flow, listen, start
from pydantic import BaseModel

from cold_outreach_flow.crews.growth_crew.growth_crew import GrowthCrew


class OutreachFlowState(BaseModel):
    company_name: str = ""
    contact_name: str = ""
    contact_role: str = ""
    company_domain: str = ""
    channel: str = ""
    sequence_position: str = ""
    primary_goal: str = ""
    known_context: str = ""
    final_plan: str = ""


class ColdOutreachFlow(Flow[OutreachFlowState]):
    """Stateful wrapper around the Sentinel outbound growth crew."""

    @start()
    def collect_inputs(self, crewai_trigger_payload: dict | None = None) -> dict:
        payload = crewai_trigger_payload or {}

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
                "Small GovCon subcontractor pursuing CMMC Level 2 readiness.",
            ),
        )

        return self._crew_inputs()

    @listen(collect_inputs)
    def run_growth_crew(self, inputs: dict) -> str:
        result = GrowthCrew().crew().kickoff(inputs=inputs)
        self.state.final_plan = result.raw
        return self.state.final_plan

    @listen(run_growth_crew)
    def finish(self, final_plan: str) -> str:
        print("Sentinel outreach plan written to output/sentinel_outreach_plan.md")
        return final_plan

    def _crew_inputs(self) -> dict:
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


def kickoff() -> None:
    ColdOutreachFlow().kickoff()


def plot() -> None:
    ColdOutreachFlow().plot()


if __name__ == "__main__":
    kickoff()

