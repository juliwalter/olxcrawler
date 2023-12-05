"""
backend/admin.py

This files registers the model in the admin space
"""
from django.contrib import admin

from backend.models import SearchRequest, SearchRequestResult, SearchRequestResultEntry

admin.site.register(SearchRequest)
admin.site.register(SearchRequestResult)
admin.site.register(SearchRequestResultEntry)
