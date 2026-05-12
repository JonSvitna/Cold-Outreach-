"""PostgreSQL read/write tools for campaign data access.

QueryTool is read-only (SELECT only).
UpsertTool is restricted to a safe allowlist of tables.
Both degrade gracefully when DATABASE_URL is absent.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

class _QueryInput(BaseModel):
    sql: str = Field(description="Read-only SELECT SQL query")
    params: List[Any] = Field(
        default=[],
        description="Positional parameters for the query (safe parameterized queries)",
    )


class PostgreSQLQueryTool(BaseTool):
    name: str = "Query Campaign Database"
    description: str = (
        "Run a read-only SELECT query against the PostgreSQL campaign database. "
        "Use to look up lead state, sequence status, past responses, suppression list, "
        "campaign metrics, activity logs, and prompt memory. SELECT only."
    )
    args_schema: Type[BaseModel] = _QueryInput

    def _run(self, sql: str, params: List[Any] = []) -> str:
        if not sql.strip().upper().startswith("SELECT"):
            return "Only SELECT queries are permitted by this tool."
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            return "DATABASE_URL not set — database query skipped."
        try:
            import psycopg
            with psycopg.connect(db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, params or [])
                    rows = cur.fetchall()
                    if not cur.description:
                        return "No rows returned."
                    cols = [d.name for d in cur.description]
                    result = [dict(zip(cols, row)) for row in rows]
                    return json.dumps(result, default=str, indent=2)
        except Exception as exc:
            return f"Query error: {exc}"


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------

_ALLOWED_WRITE_TABLES = frozenset({
    "leads",
    "responses",
    "escalation_events",
    "notifications",
    "activity_logs",
    "suppression_list",
    "outreach_sequences",
})


class _UpsertInput(BaseModel):
    table: str = Field(
        description=(
            "Target table. Allowed: leads, responses, escalation_events, "
            "notifications, activity_logs, suppression_list, outreach_sequences."
        )
    )
    data: Dict[str, Any] = Field(description="Column-to-value mapping for the record")
    conflict_target: str = Field(
        default="",
        description=(
            "Column(s) for ON CONFLICT, e.g. 'id' or 'email, domain'. "
            "Leave empty to use DO NOTHING."
        ),
    )


class PostgreSQLUpsertTool(BaseTool):
    name: str = "Write to Campaign Database"
    description: str = (
        "Insert or upsert a record into the campaign database. "
        "Use to record new leads, log responses, create escalation events, "
        "queue notifications, append activity logs, or add suppression entries."
    )
    args_schema: Type[BaseModel] = _UpsertInput

    def _run(
        self,
        table: str,
        data: Dict[str, Any],
        conflict_target: str = "",
    ) -> str:
        if table not in _ALLOWED_WRITE_TABLES:
            return (
                f"Table '{table}' is not in the allowed write list: "
                f"{sorted(_ALLOWED_WRITE_TABLES)}"
            )
        if not data:
            return "No data provided — nothing to write."
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            return "DATABASE_URL not set — write skipped."
        try:
            import psycopg
            cols = list(data.keys())
            vals = list(data.values())
            col_str = ", ".join(cols)
            placeholders = ", ".join(["%s"] * len(cols))
            conflict_clause = (
                f"({conflict_target}) DO UPDATE SET "
                + ", ".join(f"{c} = EXCLUDED.{c}" for c in cols if c != conflict_target)
                if conflict_target
                else "DO NOTHING"
            )
            sql = (
                f"INSERT INTO {table} ({col_str}) VALUES ({placeholders}) "
                f"ON CONFLICT {conflict_clause}"
            )
            with psycopg.connect(db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, vals)
                conn.commit()
            return f"Record written to {table}."
        except Exception as exc:
            return f"Write error: {exc}"


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------

def get_data_read_tools() -> list:
    """Read-only database access."""
    return [PostgreSQLQueryTool()]


def get_data_write_tools() -> list:
    """Read + write database access."""
    return [PostgreSQLQueryTool(), PostgreSQLUpsertTool()]
