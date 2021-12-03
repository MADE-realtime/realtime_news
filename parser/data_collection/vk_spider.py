import re
from argparse import ArgumentParser
from urllib.parse import urlparse

from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Response, Request, TextResponse
from scrapy.shell import inspect_response

from data_collection.util import read_urls_file


def setup_vk_parser(parser: ArgumentParser):
    parser.add_argument(
        '-start_urls',
        help='Path to file with urls',
        dest='start_urls_fpath',
        type=str,
        required=True,
    )
    parser.set_defaults(setup_kwargs=setup_vk_kwargs, spider=SpiderVK)
    return parser


def setup_vk_kwargs(start_urls_fpath):
    start_urls = read_urls_file(start_urls_fpath)
    kwargs = {
        'start_urls': start_urls,
    }
    return kwargs


class SpiderVK(Spider):
    name = 'vk_spider'
    api_key = '426aba55426aba55426aba559c4210f5334426a426aba5523c2eef6dfd5262c1391b9f8'

    def __init__(self, start_urls, *args, **kwargs):
        self.start_urls = start_urls
        self.vk_filter = (
            '/.*\/vk\.com\/[^\/]+$',
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
        self.log(f'Found {found_rss} vk link in {response.url}')

    def parse_feed(self, response: TextResponse):
        wall = response.json()['response']['items']
        for post in wall:
            if self.is_bad(post):
                continue
            item = {
                'post_id': post['id'],
                'text': post['text'],
                'date': post['date'],  # timestamp
                'comments_count': post['comments']['count'],
                'likes': post['likes']['count'],
                'reposts': post['reposts']['count'],
                'views': post['views']['count'],
            }
            yield item
        inspect_response(response, self)

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
        get_url += f'&access_token={self.api_key}'
        get_url += '&v=5.131'
        return get_url

    def is_bad(self, post):
        return False


# filter pinned
# id
# text
# comments['count']
# likes['can_like', 'count']
# reposts['count']