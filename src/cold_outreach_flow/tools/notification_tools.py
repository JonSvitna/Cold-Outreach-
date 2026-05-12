"""Notification and escalation tools — Resend email, Slack, Discord.

All tools degrade gracefully: if the required env var is absent the agent
receives an explanatory string and continues without crashing the run.
"""

from __future__ import annotations

import os
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Resend email alert
# ---------------------------------------------------------------------------

class _AlertInput(BaseModel):
    subject: str = Field(description="Short alert subject line")
    body: str = Field(description="Alert body — plain text or light HTML")
    priority: str = Field(
        default="normal",
        description="Priority level: normal, high, or urgent",
    )


class ResendAlertTool(BaseTool):
    name: str = "Send Email Alert to Sean"
    description: str = (
        "Send an immediate email alert to Sean. Use for hot leads, pricing requests, "
        "compliance concerns, technical discussions, unsubscribe events, campaign "
        "failures, or any event that requires human attention now."
    )
    args_schema: Type[BaseModel] = _AlertInput

    def _run(self, subject: str, body: str, priority: str = "normal") -> str:
        api_key = os.getenv("RESEND_API_KEY")
        if not api_key:
            return "RESEND_API_KEY not set — email alert not sent."
        alert_email = os.getenv("ALERT_EMAIL", "seanmurrill@gmail.com")
        from_email = os.getenv("FROM_EMAIL", "sentinel@vulnaguard.io")
        try:
            import resend
            resend.api_key = api_key
            resp = resend.Emails.send({
                "from": from_email,
                "to": [alert_email],
                "subject": f"[Sentinel {priority.upper()}] {subject}",
                "html": (
                    f"<div style='font-family:monospace;white-space:pre-wrap'>{body}</div>"
                ),
            })
            return f"Alert sent. Message ID: {resp.get('id', 'unknown')}"
        except Exception as exc:
            return f"Email alert failed: {exc}"


# ---------------------------------------------------------------------------
# Slack webhook
# ---------------------------------------------------------------------------

class _WebhookInput(BaseModel):
    message: str = Field(description="Message text to post to the channel")


class SlackWebhookTool(BaseTool):
    name: str = "Post Slack Alert"
    description: str = (
        "Post a notification to the Sentinel Slack channel. "
        "Use for hot leads, escalation events, and campaign status updates."
    )
    args_schema: Type[BaseModel] = _WebhookInput

    def _run(self, message: str) -> str:
        url = os.getenv("SLACK_WEBHOOK_URL")
        if not url:
            return "SLACK_WEBHOOK_URL not set — Slack alert skipped."
        try:
            import httpx
            resp = httpx.post(url, json={"text": message}, timeout=10)
            if resp.status_code == 200:
                return "Slack alert sent."
            return f"Slack error {resp.status_code}: {resp.text}"
        except Exception as exc:
            return f"Slack alert failed: {exc}"


# ---------------------------------------------------------------------------
# Discord webhook
# ---------------------------------------------------------------------------

class DiscordWebhookTool(BaseTool):
    name: str = "Post Discord Alert"
    description: str = (
        "Post a notification to the Sentinel Discord channel. "
        "Use for escalation events and campaign status updates."
    )
    args_schema: Type[BaseModel] = _WebhookInput

    def _run(self, message: str) -> str:
        url = os.getenv("DISCORD_WEBHOOK_URL")
        if not url:
            return "DISCORD_WEBHOOK_URL not set — Discord alert skipped."
        try:
            import httpx
            resp = httpx.post(url, json={"content": message}, timeout=10)
            if resp.status_code in (200, 204):
                return "Discord alert sent."
            return f"Discord error {resp.status_code}: {resp.text}"
        except Exception as exc:
            return f"Discord alert failed: {exc}"


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def get_notification_tools() -> list:
    """Email + Slack + Discord alert tools."""
    return [ResendAlertTool(), SlackWebhookTool(), DiscordWebhookTool()]
