"""
backend/tests/test_api_service.py

Contains the unit tests for the ApiService
"""
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from rest_framework import status

from backend.models import SearchRequest
from backend.services import ApiService, SearchRequestService


class ApiServiceTests(TestCase):
    """
    ApiServiceTests holds unit tests for ApiService
    """

    def setUp(self):
        self.sr_service = SearchRequestService()
        self.service = ApiService()

    def test_delete_search_request(self):
        sr = self.sr_service.create_search_request("Test description",
                                                   "https://www.olx.pt/carros-motos-e-barcos/carros/abarth/")
        response = self.service.delete_search_request(sr)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], f"Successfully deleted SearchRequest with request_id={sr.id}")
        with self.assertRaises(ObjectDoesNotExist):
            self.sr_service.get_search_request(id=sr.id)

    def test_delete_search_request_a(self):
        sr = SearchRequest(description="Test description",
                           url="https://www.olx.pt/carros-motos-e-barcos/carros/abarth/")
        response = self.service.delete_search_request(sr)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "SearchRequest does not exist.")

    # TODO: Write tests for crawl method