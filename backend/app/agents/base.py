"""Base agent: defines the protocol every agent in the fleet implements.

An agent is a callable unit that:
  - subscribes to a trigger (cron, signal arrival, manual)
  - emits structured trace events (so the frontend can stream them)
  - persists results to the DB
  - reports its own run metadata for observability
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from anthropic import AsyncAnthropic

from app.config import settings
from app.db.client import get_supabase

logger = logging.getLogger(__name__)


@dataclass
class TraceEvent:
    ts: datetime
    kind: str  # "thought" | "tool_call" | "tool_result" | "decision" | "error" | "complete"
    label: str
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "ts": self.ts.isoformat(),
            "kind": self.kind,
            "label": self.label,
            "detail": self.detail,
        }


@dataclass
class RunContext:
    run_id: str
    agent_slug: str
    trigger: str
    started_at: datetime
    trace: list[TraceEvent] = field(default_factory=list)
    signals_ingested: int = 0
    implications_generated: int = 0
    tokens_input: int = 0
    tokens_output: int = 0

    def emit(self, kind: str, label: str, **detail: Any) -> TraceEvent:
        ev = TraceEvent(ts=datetime.now(timezone.utc), kind=kind, label=label, detail=detail)
        self.trace.append(ev)
        logger.info("[%s] %s: %s", self.agent_slug, kind, label)
        # Write to in-memory bus so the frontend SSE endpoint can stream it
        from app.services.event_bus import bus
        asyncio.create_task(bus.publish({
            "type": "agent_trace",
            "run_id": self.run_id,
            "agent_slug": self.agent_slug,
            **ev.to_dict(),
        }))
        return ev


class Agent(ABC):
    slug: str
    name: str
    role: str
    description: str
    model: str = "claude-haiku-4-5-20251001"

    def __init__(self) -> None:
        self.anthropic = AsyncAnthropic(api_key=settings.anthropic_api_key)

    @abstractmethod
    async def run(self, ctx: RunContext, **kwargs: Any) -> dict[str, Any]:
        """Execute the agent's work. Return a summary dict."""
        ...

    async def execute(
        self,
        trigger: str = "manual",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Wrap a single agent run with persistence + lifecycle tracking."""
        run_id = str(uuid4())
        ctx = RunContext(
            run_id=run_id,
            agent_slug=self.slug,
            trigger=trigger,
            started_at=datetime.now(timezone.utc),
        )

        agent_id = await self._ensure_registered()
        await self._persist_run_start(run_id, agent_id, trigger)

        ctx.emit("started", f"{self.name} starting", trigger=trigger)
        t0 = time.perf_counter()

        try:
            output = await self.run(ctx, **kwargs)
            ctx.emit("complete", "Run complete", **{
                "duration_s": round(time.perf_counter() - t0, 2),
                "signals_ingested": ctx.signals_ingested,
                "implications_generated": ctx.implications_generated,
            })
            await self._persist_run_complete(run_id, agent_id, ctx, output, status="success")
            return {"run_id": run_id, "status": "success", **output}
        except Exception as exc:
            logger.exception("Agent %s failed", self.slug)
            ctx.emit("error", str(exc))
            await self._persist_run_complete(
                run_id, agent_id, ctx, {"error": str(exc)}, status="failed",
                error_message=str(exc),
            )
            return {"run_id": run_id, "status": "failed", "error": str(exc)}

    async def _ensure_registered(self) -> str:
        sb = get_supabase()
        existing = sb.table("agents").select("id").eq("slug", self.slug).execute()
        if existing.data:
            return existing.data[0]["id"]
        inserted = sb.table("agents").insert({
            "slug": self.slug,
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "model": self.model,
        }).execute()
        return inserted.data[0]["id"]

    async def _persist_run_start(self, run_id: str, agent_id: str, trigger: str) -> None:
        sb = get_supabase()
        sb.table("agent_runs").insert({
            "id": run_id,
            "agent_id": agent_id,
            "trigger": trigger,
            "status": "running",
        }).execute()

    async def _persist_run_complete(
        self,
        run_id: str,
        agent_id: str,
        ctx: RunContext,
        output: dict,
        status: str,
        error_message: str | None = None,
    ) -> None:
        sb = get_supabase()
        sb.table("agent_runs").update({
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "trace": [ev.to_dict() for ev in ctx.trace],
            "output_summary": json.dumps(output, default=str)[:2000],
            "signals_ingested": ctx.signals_ingested,
            "implications_generated": ctx.implications_generated,
            "tokens_input": ctx.tokens_input,
            "tokens_output": ctx.tokens_output,
            "error_message": error_message,
        }).eq("id", run_id).execute()
        sb.table("agents").update({
            "last_run_at": datetime.now(timezone.utc).isoformat(),
            "last_run_status": status,
        }).eq("id", agent_id).execute()
