"""
backend/views.py

Contains the backend end point definitions
"""
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from backend.models import SearchRequest
from backend.services import ApiService

api_service = ApiService()


@api_view(("DELETE",))
def request_delete(request, request_id):
    """
    Endpoint definition for `api/request/<request_id>/delete`. When calling this endpoint the SearchRequest with
    request_id gets deleted
    :param Request request: the wsgi request
    :param int request_id: parameter for the SearchRequest id
    :return: Response object containg information about request
    """
    search_request = get_object_or_404(SearchRequest, pk=request_id)
    return api_service.delete_search_request(search_request)


@api_view(("PUT",))
def request_crawl(request, request_id):
    """
    Endpoint definition for `api/request/<request_id>/crawl`. When calling this endpoint the SearchRequest with
    request_id gets crawled
    :param Request request: the wsgi request
    :param int request_id: parameter for the SearchRequest id
    :return: Response object containg information about request
    """
    search_request = get_object_or_404(SearchRequest, pk=request_id)
    return api_service.crawl_search_request(search_request)


@api_view(("GET",))
def download_csv(request, request_id):
    """
    Endpoint definition for `api/request/<request_id>/download`. When calling this endpoint the results for the
    SearchRequest with request_id gets downloaded in csv
    :param Request request: wsgi request
    :param int request_id: parameter for the SearchRequest id
    :return: Response object containg information about request
    """
    search_request = get_object_or_404(SearchRequest, pk=request_id)
    return api_service.get_csv_download(search_request)
