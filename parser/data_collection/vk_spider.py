import re
from argparse import ArgumentParser
from urllib.parse import urlparse

from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Response, Request, TextResponse

from data_collection.util import read_urls_file, clean_url_queries, BAD_QUERIES


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
            yield Request(url, callback=self.parse_main)

    def parse_main(self, response: Response):
        found_rss = 0
        domain = urlparse(response.url).netloc
        for link in self.link_extractor.extract_links(response):
            found_rss += 1
            get_url = self.vk_get(link.url)
            yield Request(get_url, callback=self.parse_vk_feed, cb_kwargs={'domain': domain})
        self.log(f'Found {found_rss} vk link in {response.url}')

    def parse_vk_feed(self, response: TextResponse, domain):
        wall = response.json()['response']['items']
        for post in wall:
            if self.is_bad(post):
                continue

            links = re.findall(r'(https?://\S+)', post['text'])
            links = [clean_url_queries(l, BAD_QUERIES) for l in links]
            item = {
                'post_id': post['id'],
                'text': post['text'],
                'date': post['date'],  # timestamp
                'comments_count': post['comments']['count'],
                'likes': post['likes']['count'],
                'reposts': post['reposts']['count'],
                'views': post['views']['count'],
                'link': links,
                'domain': domain
            }
            yield item

    def check_vk_url(self, url):
        for filter in self.vk_filter:
            if re.compile(filter).search(url):
                return True
        return False

    def vk_get(self, vk_url):
        domain = urlparse(vk_url).path[1:]
        get_url = 'https://api.vk.com/method/wall.get'
        get_url += f'?domain={domain}'
        get_url += '&count=100'
        get_url += f'&access_token={self.api_key}'
        get_url += '&v=5.131'
        return get_url

    def is_bad(self, post):
        is_pinned = post.get('is_pinned', False)
        is_add = post['marked_as_ads']
        return is_pinned or is_add
