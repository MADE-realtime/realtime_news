import re
from argparse import ArgumentParser
from urllib.parse import urlparse

from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Response, Request

from data_collection.util import read_urls_file


def setup_sm_parser(parser: ArgumentParser):
    parser.add_argument(
        '-start_urls',
        help='Path to file with urls',
        dest='start_urls_fpath',
        type=str,
        required=True,
    )
    parser.set_defaults(setup_kwargs=setup_sm_kwargs, spider=SocialMediaParser)
    return parser


def setup_sm_kwargs(start_urls_fpath):
    start_urls = read_urls_file(start_urls_fpath)
    kwargs = {
        'start_urls': start_urls,
    }
    return kwargs


class SocialMediaParser(Spider):
    name = 'sm_spider'

    def __init__(self, start_urls, *args, **kwargs):
        self.start_urls = start_urls
        self.sm_filter = {
            re.compile('.*\/vk\.com\/[^\/]+$'): 'vk',
            re.compile('.*\/t\.me\/[^\/]+$'): 'tg',
            re.compile('.*\/tgclick.com/[^\/]+$'): 'tg'
        }
        self.link_extractor = LxmlLinkExtractor(
            allow=self.sm_filter.keys(),
            tags=('a', 'area', 'link')
        )
        super(SocialMediaParser, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_main)

    def parse_main(self, response: Response):
        found_rss = 0
        domain = urlparse(response.url).netloc
        for link in self.link_extractor.extract_links(response):
            found_rss += 1
            social_media = self.get_social_media(link.url)
            yield {'domain': domain, 'link': link.url, 'social_media': social_media}
        self.log(f'Found {found_rss} vk link in {response.url}')

    def get_social_media(self, url):
        for pattern, social_media in self.sm_filter.items():
            if pattern.search(url):
                return social_media
