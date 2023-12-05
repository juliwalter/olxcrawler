"""
backend/model.py

This file contains all model definitions
"""
from django.db import models

from backend.validators import validate_olx_url


class SearchRequest(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=80)
    url = models.CharField(max_length=500, null=False, validators=[validate_olx_url])


class SearchRequestResult(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    search_request = models.ForeignKey(SearchRequest, on_delete=models.CASCADE, null=False)


class SearchRequestResultEntry(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.FloatField()
    search_request_result = models.ForeignKey(SearchRequestResult, on_delete=models.CASCADE, null=False)
