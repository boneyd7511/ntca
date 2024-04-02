from .jobs import NewBranch
from nautobot.core.celery import register_jobs

register(NewBranch)
