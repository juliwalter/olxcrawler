"""
backend/urls.py

Contains the backend end points
"""
from django.urls import path

from backend.views import request_delete, request_crawl

urlpatterns = [
    path("api/request/<int:request_id>/delete", request_delete, name="request_delete", ),
    path("api/request/<int:request_id>/crawl", request_crawl, name="request_crawl", ),
]
