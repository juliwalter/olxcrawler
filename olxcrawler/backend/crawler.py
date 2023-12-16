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
        except (Exception,):
            raise BackendException(f"Unable to connect to connect to resource {url}")

    @staticmethod
    def _extract_price_for_add(ad):
        price = ad.find("p", {"data-testid": "ad-price"}).text.split(" ")[0].replace(".", "")
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

        # split the url before the search parameters for inserting page numbers
        url_split = url.split("?")
        base_url = url_split[0]
        search_parameters = ""
        if len(url_split) > 1:
            search_parameters = url_split[1]

        for i in range(2, self.page_count + 1):
            urls.append(base_url + f"?page={i}" + search_parameters)
        print(urls)
        return urls

    def _crawl_page(self, url, car_ads):
        soup = self._get_soup(url)
        ads = soup.find_all("div", {"data-cy": "l-card"})

        for ad in ads:
            title = ad.find("h6").text
            price = self._extract_price_for_add(ad)
            year_km = ad.find("div", {"class": "css-efx9z5"}).text
            car_ad = CarAd(title, price, year_km)
            if car_ad not in car_ads:
                car_ads.append(car_ad)

    def crawl(self):
        try:
            car_ads = []
            print(self.urls)
            for url in self.urls:
                # crawl twice to make it more likely to get all ads
                self._crawl_page(url, car_ads)
                self._crawl_page(url, car_ads)
        except (Exception,) as e:
            LOGGER.warning(f"Error while crawling SearchRequest with id {self.search_request.id}")
            raise e

        if len(car_ads) > 0:
            search_request_result = SearchRequestResult()
            search_request_result.search_request = self.search_request
            search_request_result.save()

            for car_ad in car_ads:
                if car_ad.price is not None:
                    entry = SearchRequestResultEntry(price=car_ad.price, search_request_result=search_request_result)
                    entry.save()

        LOGGER.info(f"Successfully crawled SearchRequest with id {self.search_request.id}")


class CarAd:
    """
    Helper class to be able to distinguish between crawled ads.
    """

    def __init__(self, title, price, year_km):
        self.title = title
        self.price = price
        self.year_km = year_km

    def __eq__(self, other):
        if isinstance(other, CarAd):
            return self.title == other.title and self.price == other.price and self.year_km == other.year_km
        return False
