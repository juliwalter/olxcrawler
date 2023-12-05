"""
backend/apps.py

Defines the backend configuration
"""
from django.apps import AppConfig
from django.conf import settings


# TODO: Add external database instead of sqlite
# TODO: Make application deployable with docker

class BackendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend"

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from common.scheduler import Scheduler
            from backend.tasks import crawl_data_for_search_requests
            scheduler = Scheduler()
            scheduler.register_app_tasks("task_crawlCarPrices", crawl_data_for_search_requests, "34 17 * * *")
