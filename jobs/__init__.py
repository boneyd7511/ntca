from . import *

#from nautobot.apps.jobs import register_jobs
from nautobot.core.celery import register_jobs

register_jobs(NewBranch)
