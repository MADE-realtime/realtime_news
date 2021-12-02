import re
from argparse import ArgumentParser
from urllib.parse import urlparse

from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Response, Request

BAD_QUERIES = ['from', 'utm_source', 'utm_medium', 'utm_campaign',
               'at_medium', 'at_campaign', 'utm_term']


def setup_vk_parser(parser: ArgumentParser):
    return parser


class SpiderVK(Spider):
    name = 'vk_spider'
    api_key = '426aba55426aba55426aba559c4210f5334426a426aba5523c2eef6dfd5262c1391b9f8'

    def __init__(self, start_urls, *args, **kwargs):
        self.start_urls = start_urls
        self.vk_filter = (
            '.*vk\.com*',
        )
        self.link_extractor = LxmlLinkExtractor(
            allow=self.vk_filter,
            tags=('a', 'area', 'link')
        )
        super(SpiderVK, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            if self.check_vk_url(url):
                get_url = self.vk_get(url)
                yield Request(get_url, callback=self.parse_feed)
            else:
                yield Request(url, callback=self.parse_main)

    def parse_main(self, response: Response):
        found_rss = 0
        for link in self.link_extractor.extract_links(response):
            found_rss += 1
            get_url = self.vk_get(link.url)
            yield Request(get_url, callback=self.parse_feed)
        self.log(f'Found {found_rss} rss_links in {response.url}')

    def parse_feed(self, response: Response):
        pass

    def check_vk_url(self, url):
        for filter in self.vk_filter:
            if re.compile(filter).search(url):
                return True
        return False

    def vk_get(self, url):
        domain = urlparse(url).path[1:]
        get_url = 'https://api.vk.com/method/wall.get'
        get_url += f'?domain={domain}'
        get_url += '&count=100'
        get_url += '&access_token={self.api_key}'
        get_url += '&v=5.131'
        return get_url