"""
backend/urls.py

Contains the backend end points
"""
from django.urls import path

from backend.views import request_delete, request_crawl, download_csv

urlpatterns = [
    path("api/request/<int:request_id>/delete", request_delete, name="request_delete", ),
    path("api/request/<int:request_id>/crawl", request_crawl, name="request_crawl", ),
    path("api/request/<int:request_id>/download", download_csv, name="request_download", ),
]
