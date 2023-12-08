"""
webapp/views.py

This files contains webapp end point definitions
"""
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from rest_framework.request import Request

from webapp.services import SearchRequestWebservice, UserWebservice
from webapp.enums import Aggregation

search_request_webservice = SearchRequestWebservice()
user_service = UserWebservice()


@login_required
def index(request):
    """
    This method renders the index view of the web application
    :param Request request: the wsgi request
    :return: Index view
    :rtype: HttpResponse
    """
    return render(request, "webapp/index.html", context={})


@login_required
def search_request(request):
    """
    Renders the search request view and creates a search request in case of post method from the given request
    parameters
    :param Request request: wsgi request
    :return: Search request view
    :rtype: HttpResponse
    """
    context = {
        "requests": search_request_webservice.get_search_requests()
    }
    if request.method == "POST":
        try:
            search_request_webservice.create_search_request_from_request(request)
        except ValidationError as e:
            context["validation"] = e.messages[0]
    return render(request, "webapp/request.html", context=context)


@login_required
def search_result(request):
    """
    Renders the search request result view and creates a plot for the selected search request results in case of a post
    request
    :param Request request: the wsgi request
    :return: Search request result view
    :rtype: HttpResponse
    """
    context = {
        "requests": search_request_webservice.get_search_requests(),
        "aggregations": [agg.name for agg in Aggregation],
        "plot_requested": request.method == "POST",
    }
    if request.method == "POST":
        context["plot_div"] = search_request_webservice.create_plot_from_request(request)
    return render(request, "webapp/result.html", context=context)


@login_required
def profile(request):
    """
    Renders the profile view and updates the user information based on the given request parameters in case of a post
    request
    :param Request request:
    :return: Profile view
    :rtype: HttpResponse
    """
    context = {}
    if request.method == "POST":
        try:
            user_service.update_user(request)
        except ValidationError as e:
            context["validation"] = e.messages[0]
    return render(request, "webapp/profile.html", context=context)
