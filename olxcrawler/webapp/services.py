"""
webapp/services.py

This files contains webapp services
"""
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.request import Request

from backend.services import SearchRequestService, UserService
from common.singleton import Singleton
from webapp.exceptions import WebappException
from webapp.enums import Aggregation

from plotly.offline import plot


class SearchRequestWebservice(Singleton):
    """Service that encapsulates functionalities related to search request on the webapp side"""

    def __init__(self):
        self._search_request_service = SearchRequestService()

    def create_search_request_from_request(self, request):
        """
        Creates a SearchRequest from post request parameters `url` and `description`
        :param Request request: wsgi request
        :rtype: None
        :raises: ValidationError, WebappException
        """
        try:
            url = request.POST["url"]
            description = request.POST["description"]
            self._search_request_service.create_search_request(description, url)
        except ValidationError as e:
            raise e
        except MultiValueDictKeyError as e:
            raise WebappException("Missing request parameter `url` or `description in post request`") from e
        except (Exception,) as e:
            raise WebappException("An unexpected error occurred - please contact admin") from e

    def get_search_requests(self):
        """
        Fetches all existing SearchRequests and returns them
        :return: All existing SearchRequests
        :rtype: QuerySet
        """
        return self._search_request_service.get_search_requests()

    def create_plot_from_request(self, request):
        """
        Creates a html graph for the SearchRequestResults related to the SearchRequest with id equal to the post request
        parameter `request_id`
        :param Request request: wsgi request
        :return: search request result graph as html
        :rtype: str
        :raises: WebappException
        """
        try:
            idx = int(request.POST["request_id"])
            search_request = self._search_request_service.get_search_request(pk=idx)
            aggregation = Aggregation[request.POST["aggregation"]]
            series = self._search_request_service.get_result_time_series(search_request, aggregation.value)
            return self._create_graph(series, aggregation)
        except MultiValueDictKeyError as e:
            raise WebappException("Missing request parameter `request_id` or `aggregation` in post request`") from e
        except ObjectDoesNotExist as e:
            raise WebappException(f"The requests SearchRequest with id {idx} does not exist") from e
        except (Exception,) as e:
            raise WebappException("An unexpected error occurred - please contact admin") from e

    @staticmethod
    def _create_y_axis_title(aggregation):
        if aggregation == Aggregation.COUNT:
            return aggregation.name.lower()
        return f"{aggregation.name.lower()} price in €"

    @staticmethod
    def _create_graph(series, aggregation):
        figure = {
            'data': [{
                'x': series.index,
                'y': series.values,
                'type': 'scatter',
                'mode': 'markers+lines'
            }],
            'layout': {
                'xaxis': {
                    'title': 'time',
                    'autorange': True
                },
                'yaxis': {
                    'title': SearchRequestWebservice._create_y_axis_title(aggregation),
                    'autorange': True
                },
            },
        }
        return plot(figure, output_type='div')


class UserWebservice(Singleton):
    """Service that encapsulates functionalities related to user management on the webapp side"""

    def __init__(self):
        self._user_service = UserService()

    def update_user(self, request):
        """
        Updates the request context user with the request parameters `email` and `password`
        :param Request request: wsgi request
        :rtype: None
        :raises: ValidationError, WebappException
        """
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            self._user_service.update_user(request.user, email=email, password=password)
        except ValidationError as e:
            raise e
        except MultiValueDictKeyError as e:
            raise WebappException("Missing request parameter `email` or `password in post request`") from e
        except (Exception,) as e:
            raise WebappException("An unexpected error occurred - please contact admin") from e
