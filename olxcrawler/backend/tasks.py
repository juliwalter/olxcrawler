"""
backend/tests.py

Contains the backend timer tasks
"""
from backend.services import SearchRequestService

sr_service = SearchRequestService()


def crawl_data_for_search_requests():
    """
    This task crawls prices for all SearchRequests
    :rtype: None
    """
    requests = sr_service.get_search_requests()
    for request in requests:
        try:
            sr_service.crawl_search_request(search_request=request)
        except (Exception,):
            # Do nothing the service logs
            pass
