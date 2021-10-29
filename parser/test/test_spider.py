from datetime import datetime

from data_collection.newsspider import NewsSpider
from test.util import fake_response_from_file


def test_news_spider_find_news_ref():
    response = fake_response_from_file('tass_data/sitemap_hot.xml')
    date_depth = datetime(2021, 10, 26)
    news_spider = NewsSpider([], date_depth=date_depth)
    expected_url = ['https://tass.ru/ekonomika/12784183', 'https://tass.ru/sport/12784233']
    for e in news_spider._parse_sitemap(response):
        assert e.url in expected_url, f"{e.url} not expected in url to crawl (date_depth = {date_depth})"


