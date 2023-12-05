"""
backend/tests/test_search_request_service.py

Contains the unit tests for the SearchRequestSerivce
"""
from django.test import TestCase

from backend.services import SearchRequestService


class SearchRequestServiceTests(TestCase):
    """
    SearchRequestServiceTests holds unit tests for SearchRequestSerivce
    """

    def setUp(self):
        self.service = SearchRequestService()

