import re
import urllib.parse

from bs4 import BeautifulSoup
from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.linkextractors import IGNORED_EXTENSIONS
from scrapy.http import Response, Request, XmlResponse

from data_collection.util import read_urls_file, read_yaml_file


class SpiderRSS(Spider):
    name = 'parser_rss'

    def __init__(self, start_urls_fpath, rss_parser_fpath, *args, **kwargs):
        self.start_urls = read_urls_file(start_urls_fpath)
        raw_parser_zoo = read_yaml_file(rss_parser_fpath)
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


def extract_all_tags(xml_tag):
    soup = BeautifulSoup(xml_tag, 'xml')
    return [t.name for t in soup.descendants if t.name]


def regex(x):
    if isinstance(x, str):
        return re.compile(x)
    return x


def get_domain(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc
