"""Background scheduler. Wires agents to cron triggers."""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def schedule_agent(agent, cron_expr: str) -> None:
    """Register an agent on a cron schedule.

    Cron format: standard 5-field "minute hour day month dow".
    """
    async def _run():
        try:
            await agent.execute(trigger=f"cron:{cron_expr}")
        except Exception:
            logger.exception("Scheduled agent %s failed", agent.slug)

    scheduler.add_job(
        _run,
        trigger=CronTrigger.from_crontab(cron_expr),
        id=f"agent:{agent.slug}",
        replace_existing=True,
        misfire_grace_time=300,
    )
