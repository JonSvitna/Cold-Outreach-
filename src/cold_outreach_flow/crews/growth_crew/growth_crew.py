from __future__ import annotations

from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class GrowthCrew:
    """Outbound growth crew for Sentinel-CMMC."""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def lead_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_researcher"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def prospect_intelligence_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["prospect_intelligence_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def offer_positioning_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["offer_positioning_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def message_generation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["message_generation_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def compliance_guardrail_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["compliance_guardrail_agent"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def sequence_manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sequence_manager_agent"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def research_lead_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_lead_task"],  # type: ignore[index]
        )

    @task
    def prospect_intelligence_task(self) -> Task:
        return Task(
            config=self.tasks_config["prospect_intelligence_task"],  # type: ignore[index]
        )

    @task
    def offer_positioning_task(self) -> Task:
        return Task(
            config=self.tasks_config["offer_positioning_task"],  # type: ignore[index]
        )

    @task
    def message_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["message_generation_task"],  # type: ignore[index]
        )

    @task
    def compliance_review_task(self) -> Task:
        return Task(
            config=self.tasks_config["compliance_review_task"],  # type: ignore[index]
        )

    @task
    def sequence_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config["sequence_plan_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

