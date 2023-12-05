"""
webapp/urls.py

This files contains webapp end points
"""
from django.urls import path
from django.contrib.auth import logout

from webapp.views import index, search_request, search_result, profile

urlpatterns = [
    path("", index, name="index", ),
    path("request", search_request, name="search_request", ),
    path("result", search_result, name="search_result", ),
    path("profile", profile, name="profile", ),
    path("logout", logout, name="logout", ),
]
