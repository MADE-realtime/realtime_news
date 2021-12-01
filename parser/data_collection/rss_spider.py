import re
from argparse import ArgumentParser

from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.linkextractors import IGNORED_EXTENSIONS
from scrapy.http import Response, Request, XmlResponse

from data_collection.util import read_urls_file, read_yaml_file, regex, get_domain, extract_all_tags
from db_lib.db_lib.models import News
from db_lib.db_lib.database import SessionLocal
from db_lib.db_lib import crud


def setup_rs_parser(parser: ArgumentParser):
    parser.add_argument(
        '-start_urls',
        help='Path to file with urls',
        dest='start_urls_fpath',
        type=str,
        required=True,
    )
    parser.add_argument(
        '-rss_parser',
        help='Path to yaml file with parser',
        dest='rss_parser_fpath',
        type=str,
        required=True,
    )
    parser.set_defaults(setup_kwargs=setup_rs_kwargs, spider=SpiderRSS)
    return parser


def setup_rs_kwargs(start_urls_fpath, rss_parser_fpath):
    start_urls = read_urls_file(start_urls_fpath)
    rss_parser = read_yaml_file(rss_parser_fpath)
    kwargs = {
        'start_urls': start_urls,
        'rss_parser': rss_parser,
    }
    return kwargs


class SpiderRSS(Spider):
    name = 'parser_rss'

    def __init__(self, start_urls, raw_parser_zoo, *args, **kwargs):
        self.start_urls = start_urls
        self.rss_parser_zoo = self.create_zoo_rules(raw_parser_zoo)
        ignore_extensions = IGNORED_EXTENSIONS.copy()
        ignore_extensions.remove('rss')
        self.rss_filter = (
            '.*\/rss.*',
            '.*\/feed.*',
            '.*\.rss'
        )
        self.link_extractor = LxmlLinkExtractor(
            allow=self.rss_filter,
            deny_extensions=ignore_extensions,
            tags=('a', 'area', 'link')
        )
        super(SpiderRSS, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            if self.check_rss_url(url):
                yield Request(url, callback=self.parse_rss_xml)
            else:
                yield Request(url, callback=self.parse_main)

    def parse_main(self, response: Response):
        found_rss = 0
        for link in self.link_extractor.extract_links(response):
            found_rss += 1
            yield Request(link.url, callback=self.parse_rss_xml)
        self.log(f'Found {found_rss} rss_links in {response.url}')

    def parse_rss_xml(self, response: XmlResponse):
        domain = get_domain(response.url)
        for rss_item in response.xpath('//item'):
            parser_name, parser = self.find_parser(response.url)
            self.log(f'parse {response.url} with {parser_name} parser')
            yield {
                'domain': domain,
                **self.parse_rss_item(rss_item, parser),
                'tags': extract_all_tags(rss_item.get())
            }

    @staticmethod
    def parse_rss_item(rss_item, parser):
        parsed_data = dict()
        for field, xpath_list in parser.items():
            if isinstance(xpath_list, str):
                xpath_list = [xpath_list]
            assert isinstance(xpath_list, list), 'Expected list type in xpath'
            field_data = None
            for xpath in xpath_list:
                selected_data = rss_item.xpath(xpath).getall()
                if len(selected_data) == 1:
                    field_data = selected_data[0]
                elif len(selected_data) > 1:
                    field_data = selected_data
                if field_data:
                    break
            parsed_data[field] = field_data
        return parsed_data

    def find_parser(self, response_url):
        for parser_name, (rule, parser) in self.rss_parser_zoo.items():
            if rule.search(response_url):
                return parser_name, parser

    @staticmethod
    def create_zoo_rules(parser_zoo):
        new_parser_zoo = dict()
        for parser_name, parser in parser_zoo.items():
            parser_rule = regex(parser_name)
            new_parser_zoo[parser_name] = (parser_rule, parser)
        return new_parser_zoo

    def check_rss_url(self, url):
        for filter in self.rss_filter:
            if re.compile(filter).search(url):
                return True
        return False


class DatabaseAdapter(SpiderRSS):
    def __init__(self, *args, **kwargs):
        super(DatabaseAdapter, self).__init__(*args, **kwargs)
        self.legal_keys = [
            ('title', dummy_func),
            ('title_post', dummy_func),
            ('content', dummy_func),
            ('source_url', dummy_func),
            ('image_url', dummy_func),
            ('date', self.get_date),
            ('topic', self.get_time),
        ]

    def parse_rss_xml(self, response: XmlResponse):
        for item in super(DatabaseAdapter, self).parse_rss_xml(response):
            db_item = self.prepare_item(item)
            db_item = crud.create_news(SessionLocal(), db_item)
            return db_item

    def prepare_item(self, item):
        preproc_item = {}
        for key, preproc in self.legal_keys:
            value = item.get(key, None)
            if value is not None:
                value = preproc(value)
            preproc_item[key] = value
        db_item = News(**preproc_item)
        return db_item

    @staticmethod
    def get_date(rss_date):
        return rss_date

    @staticmethod
    def get_time(rss_time):
        return rss_time


def dummy_func(x):
    return x
