import asyncio
import json
from typing import AsyncIterator

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from app.agents.registry import all_agents, get_agent
from app.db.client import get_supabase
from app.services.event_bus import bus

router = APIRouter()


@router.get("")
async def list_agents():
    sb = get_supabase()
    db_rows = sb.table("agents").select("*").execute().data
    by_slug = {r["slug"]: r for r in db_rows}
    out = []
    for a in all_agents():
        db = by_slug.get(a.slug, {})
        out.append({
            "slug": a.slug,
            "name": a.name,
            "role": a.role,
            "description": a.description,
            "model": a.model,
            "is_active": db.get("is_active", True),
            "schedule_cron": db.get("schedule_cron"),
            "last_run_at": db.get("last_run_at"),
            "last_run_status": db.get("last_run_status"),
        })
    return {"agents": out}


@router.get("/runs")
async def list_runs(limit: int = 25):
    sb = get_supabase()
    rows = sb.table("agent_runs").select(
        "id,trigger,started_at,completed_at,status,signals_ingested,implications_generated,"
        "tokens_input,tokens_output,output_summary,error_message,"
        "agent:agents(slug,name,role,model)"
    ).order("started_at", desc=True).limit(limit).execute().data
    return {"runs": rows}


@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    sb = get_supabase()
    rows = sb.table("agent_runs").select(
        "*,agent:agents(slug,name,role,model)"
    ).eq("id", run_id).execute().data
    if not rows:
        raise HTTPException(404, "run not found")
    return rows[0]


@router.post("/{slug}/run")
async def run_agent(slug: str, background: BackgroundTasks):
    try:
        agent = get_agent(slug)
    except KeyError:
        raise HTTPException(404, f"unknown agent: {slug}")
    background.add_task(agent.execute, "manual")
    return {"status": "started", "agent": slug}


@router.get("/stream")
async def stream():
    """SSE endpoint pushing trace events. Falls back to a polite no-op stream
    when sse-starlette isn't installed (e.g. Vercel serverless)."""
    try:
        from sse_starlette.sse import EventSourceResponse  # type: ignore
        return EventSourceResponse(bus.stream())
    except ImportError:
        async def _noop() -> AsyncIterator[bytes]:
            yield b'data: {"type":"info","message":"SSE not available in this environment; agent runs are persisted to DB"}\n\n'

        return StreamingResponse(_noop(), media_type="text/event-stream")
