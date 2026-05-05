"""Background scheduler. APScheduler if available; no-op otherwise (Vercel)."""
import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    scheduler = AsyncIOScheduler()
    _ENABLED = True
except ImportError:
    logger.info("APScheduler not installed — running in serverless mode (no in-process cron)")
    _ENABLED = False

    class _Noop:
        def start(self) -> None: ...
        def shutdown(self, wait: bool = False) -> None: ...
        def add_job(self, *args: Any, **kwargs: Any) -> None: ...

    scheduler = _Noop()  # type: ignore[assignment]


def schedule_agent(agent: Any, cron_expr: str) -> None:
    if not _ENABLED:
        return

    async def _run():
        try:
            await agent.execute(trigger=f"cron:{cron_expr}")
        except Exception:
            logger.exception("Scheduled agent %s failed", agent.slug)

    scheduler.add_job(  # type: ignore[attr-defined]
        _run,
        trigger=CronTrigger.from_crontab(cron_expr),
        id=f"agent:{agent.slug}",
        replace_existing=True,
        misfire_grace_time=300,
    )
