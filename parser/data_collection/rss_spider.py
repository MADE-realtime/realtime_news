import re
from argparse import ArgumentParser

from dateutil import parser as date_parser
from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.linkextractors import IGNORED_EXTENSIONS
from scrapy.http import Response, Request, XmlResponse

from data_collection.util import (
    read_urls_file,
    read_yaml_file,
    regex,
    get_domain,
    extract_all_tags,
    clean_url_queries,
    is_comment_url
)
from db_lib.models import News
from db_lib.database import SessionLocal
from db_lib import crud

BAD_QUERIES = ['from', 'utm_source', 'utm_medium', 'utm_campaign',
               'at_medium', 'at_campaign', 'utm_term']


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


def setup_rs_db_parser(parser: ArgumentParser):
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
    parser.set_defaults(setup_kwargs=setup_rs_kwargs, spider=DatabaseAdapter)
    return parser


def setup_rs_kwargs(start_urls_fpath, rss_parser_fpath):
    start_urls = read_urls_file(start_urls_fpath)
    rss_parser = read_yaml_file(rss_parser_fpath)
    kwargs = {
        'start_urls': start_urls,
        'raw_parser_zoo': rss_parser,
    }
    return kwargs


class SpiderRSS(Spider):
    name = 'rss_spider'

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
            parsed_item = self.parse_rss_item(rss_item, parser)
            if self.filter_item(parsed_item):
                parsed_item['source_url'] = clean_url_queries(parsed_item['source_url'], BAD_QUERIES)
                yield {
                    'domain': domain,
                    **parsed_item,
                    'tags': extract_all_tags(rss_item.get())
                }
            else:
                self.log(f'Filtered: {parsed_item}')

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

    def filter_item(self, parsed_item):
        if parsed_item.get('source_url', None) is None:
            return False
        return not is_comment_url(parsed_item['source_url'])


class DatabaseAdapter(SpiderRSS):
    def __init__(self, *args, **kwargs):
        super(DatabaseAdapter, self).__init__(*args, **kwargs)
        self.legal_keys = [
            'title',
            'title_post',
            'content',
            'source_url',
            'image_url',
            'topic',
        ]

    def parse_rss_xml(self, response: XmlResponse):
        for item in super(DatabaseAdapter, self).parse_rss_xml(response):
            db_item = self.prepare_item(item)
            db_item = crud.create_news(SessionLocal(), db_item)
            return db_item

    def prepare_item(self, item):
        preproc_item = {key: item.get(key, None) for key in self.legal_keys}
        preproc_item.update(**self.split_datetime(item.get('datetime', None)))
        db_item = News(**preproc_item)
        return db_item

    def split_datetime(self, news_datetime):
        split = {}
        news_datetime = date_parser.parse(news_datetime)
        split['date'] = news_datetime.date()
        split['time'] = news_datetime.time()
        return split

