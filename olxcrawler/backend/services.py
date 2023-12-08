"""
backend/services.py

Contains the backend services
"""
import logging

import pandas as pd
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.validators import validate_email
from django.db.models.query import QuerySet
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from backend.crawler import OlxCrawler
from backend.exceptions import BackendException
from backend.models import SearchRequest, SearchRequestResult, SearchRequestResultEntry
from common.singleton import Singleton
from pandas import Series, DatetimeIndex

from webapp.enums import Aggregation

LOGGER = logging.getLogger(__name__)


class SearchRequestService(Singleton):
    """This service encapsulates functionality related to SearchRequests"""

    @staticmethod
    def create_search_request(description: str, url: str):
        """
        Creates a SearchRequest with the given description and url
        :param str description: The description of the SearchRequest
        :param str url: The url of the SearchRequest
        :return: The created search request
        :rtype: SearchRequest
        """
        sr = SearchRequest(description=description, url=url)
        sr.full_clean()
        sr.save()
        return sr

    @staticmethod
    def get_search_requests():
        """
        Returns all registered SearchRequests
        :return: Query set of all SearchRequests
        :rtype: QuerySet
        """
        return SearchRequest.objects.all()

    @staticmethod
    def get_search_request(**kwargs):
        """
        Gets a SearchRequest by the given parameters
        :param kwargs: The parameters
        :return: The SearchRequest
        :rtype: SearchRequest
        """
        return SearchRequest.objects.get(**kwargs)

    @staticmethod
    def delete_search_request_by_id(idx):
        """
        Deleters a SearchRequest by the given id
        :param int idx: The id of the SearchRequest
        :rtype: None
        """
        try:
            SearchRequest.objects.get(pk=idx).delete()
        except ObjectDoesNotExist as e:
            LOGGER.warning(f"SearchRequest with id {idx} does not exist")
            raise e

    @staticmethod
    def get_result_time_series(search_request, aggregation):
        """
        Creates a time series of the SearchRequestResults for the given SearchRequest. The aggregation method aggregates
        the prices for each SearchRequestResult.
        :param SearchRequest search_request: search request
        :param Callable aggregation: aggregation method (min, max, sum, ...)
        :return: aggregated search request result time series
        :rtype: Series
        """
        results = SearchRequestResult.objects.filter(search_request=search_request)
        entries = SearchRequestResultEntry.objects.filter(search_request_result__in=results)
        index, values = list(), list()
        for result in results:
            result_entries = list(filter(lambda x: x.search_request_result == result, entries))
            if len(result_entries) > 0:
                index.append(result.date)
                values.append(aggregation(list(map(lambda x: x.price, result_entries))))
        return Series(values, index=DatetimeIndex(index))

    @staticmethod
    def crawl_search_request(search_request):
        """
        Crawls the data for the given search request
        :param SearchRequest search_request: The search request
        :rtype: None
        """
        crawler = OlxCrawler(search_request)
        crawler.crawl()


class UserService:
    """This service encapsulates functionality related to the user management"""

    @staticmethod
    def get_user_by_id(user_id):
        """
        Gets a user by the given id
        :param int user_id: The user id
        :return: The User
        :rtype: User
        """
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist as e:
            LOGGER.warning(f"User with id {user_id} does not exist", e)
            raise e

    @staticmethod
    def update_user(user, **kwargs):
        """
        Updates the given user with the given parameters
        :param User user: The user
        :param kwargs: The parameters
        :return: the user
        :rtype: User
        """
        if kwargs.get("email"):
            validate_email(kwargs.get("email"))
            user.email = kwargs.get("email")
        if kwargs.get("password"):
            validate_password(kwargs.get("password"))
            user.set_password(kwargs.get("password"))
        user.save()


class ApiService(Singleton):
    """
    This service implements the functionality for the api endpoints. This includes service calls and creating api
    responses.
    """

    def __init__(self):
        self.sr_service = SearchRequestService()

    def delete_search_request(self, search_request):
        """
        Deletes a given search request and creates an api response
        :param SearchRequest search_request: The search request
        :return: An api response
        :rtype: Response
        """
        try:
            self.sr_service.delete_search_request_by_id(search_request.id)
            return Response({
                "message": f"Successfully deleted SearchRequest with request_id={search_request.id}",
            }, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "SearchRequest does not exist.", }, status.HTTP_400_BAD_REQUEST)
        except MultipleObjectsReturned:
            return Response({"message": f"No unique SearchRequest found for request_id={search_request.id}", },
                            status.HTTP_400_BAD_REQUEST)
        except (Exception,):
            return Response({
                "message": f"Unexpected error while deleting SearchRequest with request_id={search_request.id}",
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def crawl_search_request(self, search_request):
        """
        Crawls data for the given search request and returns a api response
        :param SearchRequest search_request: The search request
        :return: An api response
        :rtype: Response
        """
        try:
            self.sr_service.crawl_search_request(search_request)
            return Response({
                "message": f"Successfully crawled SearchRequest with request_id={search_request.id}",
            }, status.HTTP_200_OK)
        except BackendException:
            return Response({
                "message": f"Unable to connect to {search_request.url}",
            }, status.HTTP_502_BAD_GATEWAY)
        except (Exception,) as e:
            return Response({
                "message": f"Unexpected error while crawling SearchRequest with request_id={search_request.id}",
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_csv_download(self, search_request):
        try:
            data = {}
            for agg in Aggregation:
                series = self.sr_service.get_result_time_series(search_request, agg.value)
                if "datetime" not in data.keys():
                    data["datetime"] = series.index
                data[agg.name] = series

            response = HttpResponse(content_type='text/csv')
            response['X-Filename'] = f"Results_{search_request.description}.csv"
            pd.DataFrame(data).to_csv(path_or_buf=response, sep=';', float_format='%.2f', index=False, decimal=",")
            return response
        except (Exception,):
            return Response({
                "message": f"Unexpected error while creating SearchRequestResults csv from SearchRequest with "
                           f"request_id={search_request.id}", },
                status.HTTP_500_INTERNAL_SERVER_ERROR)
