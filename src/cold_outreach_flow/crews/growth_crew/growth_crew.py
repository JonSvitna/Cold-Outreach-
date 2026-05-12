"""Sentinel Growth Commander crew — hierarchical, commander-managed.

The Sentinel Growth Commander is the manager_agent: it receives the full task
list, delegates to specialists, evaluates every output, and can reject/redo
work before the flow advances. The commander does NOT appear in self.agents.

Tool assignment mirrors the architecture plan:
  Research layer     → Tavily + Firecrawl (live web intelligence)
  Risk / history     → PostgreSQL read (past profiles, suppression)
  Sequence / ops     → PostgreSQL write (record plans and sequences)
  Response handling  → PostgreSQL write (classify + persist replies)
  Notifications      → Resend + Slack + Discord (alert Sean immediately)
  Health monitoring  → PostgreSQL read (campaign metrics and trends)
"""

from __future__ import annotations

from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from cold_outreach_flow.tools.data_tools import get_data_read_tools, get_data_write_tools
from cold_outreach_flow.tools.notification_tools import get_notification_tools
from cold_outreach_flow.tools.research_tools import get_enrichment_tools, get_research_tools


@CrewBase
class GrowthCrew:
    """Outbound command crew for Sentinel-CMMC."""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ------------------------------------------------------------------
    # Research layer
    # ------------------------------------------------------------------

    @agent
    def lead_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_research_agent"],  # type: ignore[index]
            tools=get_research_tools(),
            verbose=True,
        )

    @agent
    def enrichment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["enrichment_agent"],  # type: ignore[index]
            tools=get_enrichment_tools(),
            verbose=True,
        )

    @agent
    def prospect_intelligence_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["prospect_intelligence_agent"],  # type: ignore[index]
            tools=get_research_tools(),
            verbose=True,
        )

    @agent
    def risk_context_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["risk_context_agent"],  # type: ignore[index]
            tools=get_data_read_tools(),
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Persuasion layer (LLM-only — work from context passed by commander)
    # ------------------------------------------------------------------

    @agent
    def psychology_profiling_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["psychology_profiling_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def offer_positioning_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["offer_positioning_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def cta_optimization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["cta_optimization_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def message_generation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["message_generation_agent"],  # type: ignore[index]
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Safety layer
    # ------------------------------------------------------------------

    @agent
    def compliance_guardrail_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["compliance_guardrail_agent"],  # type: ignore[index]
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Operations layer
    # ------------------------------------------------------------------

    @agent
    def outreach_sequence_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["outreach_sequence_agent"],  # type: ignore[index]
            tools=get_data_write_tools(),
            verbose=True,
        )

    @agent
    def response_interpretation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["response_interpretation_agent"],  # type: ignore[index]
            tools=get_data_write_tools(),
            verbose=True,
        )

    @agent
    def notification_escalation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["notification_escalation_agent"],  # type: ignore[index]
            tools=get_notification_tools() + get_data_write_tools(),
            verbose=True,
        )

    @agent
    def campaign_health_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["campaign_health_agent"],  # type: ignore[index]
            tools=get_data_read_tools(),
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------

    @task
    def commander_intake_task(self) -> Task:
        return Task(config=self.tasks_config["commander_intake_task"])  # type: ignore[index]

    @task
    def research_lead_task(self) -> Task:
        return Task(config=self.tasks_config["research_lead_task"])  # type: ignore[index]

    @task
    def enrichment_task(self) -> Task:
        return Task(config=self.tasks_config["enrichment_task"])  # type: ignore[index]

    @task
    def prospect_intelligence_task(self) -> Task:
        return Task(config=self.tasks_config["prospect_intelligence_task"])  # type: ignore[index]

    @task
    def risk_context_task(self) -> Task:
        return Task(config=self.tasks_config["risk_context_task"])  # type: ignore[index]

    @task
    def psychology_profile_task(self) -> Task:
        return Task(config=self.tasks_config["psychology_profile_task"])  # type: ignore[index]

    @task
    def offer_positioning_task(self) -> Task:
        return Task(config=self.tasks_config["offer_positioning_task"])  # type: ignore[index]

    @task
    def cta_optimization_task(self) -> Task:
        return Task(config=self.tasks_config["cta_optimization_task"])  # type: ignore[index]

    @task
    def message_generation_task(self) -> Task:
        return Task(config=self.tasks_config["message_generation_task"])  # type: ignore[index]

    @task
    def compliance_review_task(self) -> Task:
        return Task(config=self.tasks_config["compliance_review_task"])  # type: ignore[index]

    @task
    def sequence_plan_task(self) -> Task:
        return Task(config=self.tasks_config["sequence_plan_task"])  # type: ignore[index]

    @task
    def response_interpretation_task(self) -> Task:
        return Task(config=self.tasks_config["response_interpretation_task"])  # type: ignore[index]

    @task
    def notification_escalation_task(self) -> Task:
        return Task(config=self.tasks_config["notification_escalation_task"])  # type: ignore[index]

    @task
    def campaign_health_task(self) -> Task:
        return Task(config=self.tasks_config["campaign_health_task"])  # type: ignore[index]

    @task
    def commander_final_approval_task(self) -> Task:
        return Task(config=self.tasks_config["commander_final_approval_task"])  # type: ignore[index]

    # ------------------------------------------------------------------
    # Commander — manager_agent, not in self.agents
    # ------------------------------------------------------------------

    def _commander(self) -> Agent:
        """The Sentinel Growth Commander as hierarchical manager.

        Not decorated with @agent so CrewAI does not add it to self.agents.
        Passed directly as manager_agent on the Crew so it orchestrates all
        other agents, evaluates their outputs, and decides what to redo.
        """
        return Agent(
            config=self.agents_config["sentinel_growth_commander"],  # type: ignore[index]
            allow_delegation=True,
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Crew
    # ------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self._commander(),
            memory=True,
            verbose=True,
        )
