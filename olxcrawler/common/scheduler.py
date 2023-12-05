"""
common/scheduler.py

This files contains the functionality associated with the scheduler
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from django_apscheduler.jobstores import DjangoJobStore, ConflictingIdError

from common.singleton import Singleton

from collections.abc import Callable
import logging

LOGGER = logging.getLogger()
JOB_STORE = "olx_crawler_job_store"


class Scheduler(Singleton):
    """
    This class wraps a BackgroundScheduler and enables the application to register task
    """

    def __init__(self):
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_jobstore(DjangoJobStore(), JOB_STORE)
        self._scheduler.start()

    def register_app_tasks(self, job_id, func, cron):
        """
        Registeres a task `func` to the given `job_id`. The task gets scheduled with the given `cron` expression
        :param str job_id: the job id
        :param Callable func: the task definition
        :param str cron: the cron expression
        :rtype: None
        """
        try:
            self._scheduler.add_job(func, CronTrigger.from_crontab(cron), id=job_id, jobstore=JOB_STORE)
            LOGGER.info(f"Job {job_id} successfully registered")
        except ConflictingIdError:
            LOGGER.info(f"Job {job_id} already registered")
