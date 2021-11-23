import re
import urllib.parse

from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Response, Request, XmlResponse

from data_collection.util import read_urls_file, read_yaml_file


class SpiderRSS(Spider):
    name = 'parser_rss'

    def __init__(self, start_urls_fpath, rss_parser_fpath, *args, **kwargs):
        self.start_urls = read_urls_file(start_urls_fpath)
        raw_parser_zoo = read_yaml_file(rss_parser_fpath)
        self.rss_parser_zoo = self.create_zoo_rules(raw_parser_zoo)
        self.link_extractor = LxmlLinkExtractor(allow=(
            '.*\/rss.*',
            '.*\/feed.*'
        ))
        super(SpiderRSS, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_main)

    def parse_main(self, response: Response):
        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse_rss_xml)

    def parse_rss_xml(self, response: XmlResponse):
        domain = get_domain(response.url)
        for rss_item in response.xpath('//item'):
            parser_name, parser = self.find_parser(response.url)
            self.log(f'parse {response.url} with {parser_name} parser')
            yield {'domain': domain, **self.parse_rss_item(rss_item, parser)}

    @staticmethod
    def parse_rss_item(rss_item, parser):
        parsed_data = dict()
        for field, xpath in parser.items():
            field_data = rss_item.xpath(xpath).getall()
            if len(field_data) == 1:
                field_data = field_data[0]
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


def regex(x):
    if isinstance(x, str):
        return re.compile(x)
    return x


def get_domain(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc
