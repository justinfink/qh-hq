import asyncio

from fastapi import APIRouter, BackgroundTasks, HTTPException
from sse_starlette.sse import EventSourceResponse

from app.agents.registry import all_agents, get_agent
from app.db.client import get_supabase
from app.services.event_bus import bus

router = APIRouter()


@router.get("")
async def list_agents():
    """Registry view + last-run status for each agent."""
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

    # Fire and forget; client subscribes to /stream for traces
    background.add_task(agent.execute, "manual")
    return {"status": "started", "agent": slug}


@router.get("/stream")
async def stream():
    """SSE endpoint pushing trace events from any active agent run."""
    return EventSourceResponse(bus.stream())
