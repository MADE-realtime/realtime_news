from datetime import datetime
from scrapy.http import Response, Request

from data_collection.newsspider import NewsSpider
from test.util import get_abs_path


def test_news_spider_find_news_ref():
    response = fake_response_from_file('tass_data/sitemap_hot.xml')
    date_depth = datetime(2021, 10, 26)
    news_spider = NewsSpider([], date_depth=date_depth)
    expected_url = ['https://tass.ru/ekonomika/12784183', 'https://tass.ru/sport/12784233']
    for e in news_spider._parse_sitemap(response):
        assert e.url in expected_url, f"{e.url} not expected in url to crawl (date_depth = {date_depth})"


def fake_response_from_file(file_path, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_path: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)
    file_path = get_abs_path(file_path)

    file_content = open(file_path, 'rb').read()

    response = Response(url=url,
        request=request,
        body=file_content)
    response.encoding = 'utf-8'
    return response