from __future__ import annotations

from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from cold_outreach_flow.tools.research_tools import get_enrichment_tools, get_research_tools


@CrewBase
class GrowthCrew:
    """Outbound command crew for Sentinel-CMMC."""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def sentinel_growth_commander(self) -> Agent:
        return Agent(config=self.agents_config["sentinel_growth_commander"], verbose=True)  # type: ignore[index]

    @agent
    def lead_research_agent(self) -> Agent:
        return Agent(config=self.agents_config["lead_research_agent"], tools=get_research_tools(), verbose=True)  # type: ignore[index]

    @agent
    def enrichment_agent(self) -> Agent:
        return Agent(config=self.agents_config["enrichment_agent"], tools=get_enrichment_tools(), verbose=True)  # type: ignore[index]

    @agent
    def prospect_intelligence_agent(self) -> Agent:
        return Agent(config=self.agents_config["prospect_intelligence_agent"], tools=get_research_tools(), verbose=True)  # type: ignore[index]

    @agent
    def risk_context_agent(self) -> Agent:
        return Agent(config=self.agents_config["risk_context_agent"], verbose=True)  # type: ignore[index]

    @agent
    def psychology_profiling_agent(self) -> Agent:
        return Agent(config=self.agents_config["psychology_profiling_agent"], verbose=True)  # type: ignore[index]

    @agent
    def offer_positioning_agent(self) -> Agent:
        return Agent(config=self.agents_config["offer_positioning_agent"], verbose=True)  # type: ignore[index]

    @agent
    def cta_optimization_agent(self) -> Agent:
        return Agent(config=self.agents_config["cta_optimization_agent"], verbose=True)  # type: ignore[index]

    @agent
    def message_generation_agent(self) -> Agent:
        return Agent(config=self.agents_config["message_generation_agent"], verbose=True)  # type: ignore[index]

    @agent
    def compliance_guardrail_agent(self) -> Agent:
        return Agent(config=self.agents_config["compliance_guardrail_agent"], verbose=True)  # type: ignore[index]

    @agent
    def outreach_sequence_agent(self) -> Agent:
        return Agent(config=self.agents_config["outreach_sequence_agent"], verbose=True)  # type: ignore[index]

    @agent
    def response_interpretation_agent(self) -> Agent:
        return Agent(config=self.agents_config["response_interpretation_agent"], verbose=True)  # type: ignore[index]

    @agent
    def notification_escalation_agent(self) -> Agent:
        return Agent(config=self.agents_config["notification_escalation_agent"], verbose=True)  # type: ignore[index]

    @agent
    def campaign_health_agent(self) -> Agent:
        return Agent(config=self.agents_config["campaign_health_agent"], verbose=True)  # type: ignore[index]

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

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
