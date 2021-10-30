import os.path
import re
import datetime
from unittest.mock import MagicMock, patch
from dicttoxml import dicttoxml

from data_collection.newsspider import NewsSpider
from data_collection.parser_zoo import PARSER_ZOO
from test.util import fake_response_from_file


def test_news_spider_find_news_ref():
    response = fake_response_from_file('tass_data/sitemap_hot.xml', url='http://www.example.com/sitemap.xml')
    date_depth = datetime.datetime(2021, 10, 26, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)))
    news_spider = NewsSpider([], [], date_depth=date_depth)
    expected_url = ['https://tass.ru/ekonomika/12784183', 'https://tass.ru/sport/12784233']
    for news_response in news_spider._parse_sitemap(response):
        assert news_response.url in expected_url, f"{news_response.url} not expected in url to crawl (date_depth = {date_depth})"


def test_news_spider_use_parser_in_response(tmpdir):
    sitemap_rules = []
    url_domains = []
    for i in range(3):
        example_name = f'example{i}'
        domain = f'{example_name}.ru'
        url_domains.append(domain)
        PARSER_ZOO[example_name] = MagicMock()
        sitemap_rules.append((domain, example_name))
    xml = create_example_sitemap_xml(url_domains)
    with open(os.path.join(tmpdir, 'example_sitemap.xml'), 'wb') as fout:
        fout.write(xml)

    example_request = fake_response_from_file(os.path.join(tmpdir, 'example_sitemap.xml'))
    date_depth = datetime.datetime(2021, 10, 26, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)))
    news_spider = NewsSpider([], sitemap_rules, date_depth=date_depth)
    for news_response in news_spider._parse_sitemap(example_request):
        parser_name = re.findall('example.', news_response.url)[0]
        expected_callback = PARSER_ZOO[parser_name].parse
        assert news_response.callback == expected_callback, (f"expected {parser_name} parse method")


def create_example_sitemap_xml(url_domains):
    sitemap_xml = []
    for url_domain, url_ending in zip(url_domains, ['/sport/12784233', '/ekonomika/12784183', '/ekonomika/12784189']):
        url_xml = {
            'loc': f'https://www.{url_domain}{url_ending}',
            'lastmod': '2021-10-27T21:13:58+03:00',
        }
        sitemap_xml.append({'url': url_xml})
    xml = dicttoxml(sitemap_xml, root='urlset')
    return xml

