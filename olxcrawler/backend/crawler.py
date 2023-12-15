"""
backend/crawler.py

Defines the logic related to the crawler object
"""
from backend.exceptions import BackendException
from backend.models import SearchRequestResultEntry, SearchRequestResult

from bs4 import BeautifulSoup
import requests
import logging

LOGGER = logging.getLogger(__name__)


class OlxCrawler:
    def __init__(self, search_request):
        self.search_request = search_request
        self.page_count = self._get_page_count()
        self.urls = self._get_following_urls()

    @staticmethod
    def _get_soup(url):
        try:
            response = requests.get(url)
            return BeautifulSoup(response.content, "html.parser")
        except (Exception, ):
            raise BackendException(f"Unable to connect to connect to resource {url}")

    @staticmethod
    def _extract_price(result):
        price = result.find_all("p", {"data-testid": "ad-price"})[0].text.split(" ")[0].replace(".", "")
        if price.isnumeric():
            return int(price)
        return None

    def _get_page_count(self):
        following_pages = self._get_soup(self.search_request.url).find_all("li",
                                                                           {"data-testid": "pagination-list-item"})
        pages = [int(x.findNext("a").text) if x.findNext("a").text.isnumeric() else None for x in following_pages]
        return 1 if len(pages) == 0 else max(pages)

    def _get_following_urls(self):
        url = self.search_request.url
        urls = [url]

        url_split = url.split("?")
        base_url = url_split[0]
        search_parameters = ""
        if len(url_split) > 1:
            search_parameters = url_split[1]

        for i in range(2, self.page_count + 1):
            urls.append(base_url + f"?page={i}" + search_parameters)
        return urls

    def _crawl_page(self, url, search_request_result):
        soup = self._get_soup(url)

        results = soup.find_all("div", {"data-cy": "l-card"})
        prices = [self._extract_price(result) for result in results]

        if len(prices) > 0:
            for price in filter(lambda x: x is not None, prices):
                search_request_result_entry = SearchRequestResultEntry()
                search_request_result_entry.price = price
                search_request_result_entry.search_request_result = search_request_result
                search_request_result_entry.full_clean()
                search_request_result_entry.save()

    def crawl(self):
        search_request_result = SearchRequestResult()
        search_request_result.search_request = self.search_request
        search_request_result.save()

        try:
            for url in self.urls:
                self._crawl_page(url, search_request_result)
        except (Exception, ) as e:
            LOGGER.warning(f"Error while crawling SearchRequest with id {self.search_request.id}")
            raise e
        LOGGER.info(f"Successfully crawled SearchRequest with id {self.search_request.id}")
