from datetime import datetime, timedelta, timezone
from argparse import ArgumentParser

from scrapy.spiders import SitemapSpider

from data_collection.parser_zoo import PARSER_ZOO
from data_collection.util import read_urls_file, read_rule_file


def setup_ns_parser(parser: ArgumentParser):
    parser.add_argument(
        '-sitemap_urls',
        help='Path to file with sitemap urls',
        dest='sitemap_urls_fpath',
        type=str,
        required=True,
    )
    parser.add_argument(
        '-sitemap_rules',
        help='Path to file with rules to match parsers',
        dest='sitemap_rules_fpath',
        type=str,
        required=True,
    )
    parser.add_argument(
        '-date_depth',
        help='Date depth as kwargs for timedelta',
        dest='date_depth_raw',
        type=str,
        required=True,
    )
    parser.set_defaults(setup_kwargs=setup_ns_kwargs, spider=NewsSpider)
    return parser


def setup_ns_kwargs(sitemap_urls_fpath, sitemap_rules_fpath, date_depth_raw):
    sitemap_urls = read_urls_file(sitemap_urls_fpath)
    sitemap_rules = read_rule_file(sitemap_rules_fpath)
    date_depth = str_to_timedelta(date_depth_raw)
    kwargs = {
        'sitemap_urls': sitemap_urls,
        'sitemap_rules': sitemap_rules,
        'date_depth': date_depth,
    }
    return kwargs


class NewsSpider(SitemapSpider):
    name = 'rta'

    def __init__(self, sitemap_urls=None, sitemap_rules=None, date_depth=None, *args, **kwargs):
        self.sitemap_urls = sitemap_urls or []
        self.sitemap_rules = [(domain, PARSER_ZOO[parser_name].parse) for domain, parser_name in sitemap_rules]

        self.date_depth = self.get_date_beggining(date_depth)
        super(NewsSpider, self).__init__(*args, **kwargs)

    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = datetime.strptime(entry['lastmod'], '%Y-%m-%dT%H:%M:%S%z')
            if date_time >= self.date_depth:
                yield entry

    @staticmethod
    def get_date_beggining(date_depth):
        today = datetime.now(tz=timezone(timedelta(seconds=10800)))
        if date_depth is None:
            today = datetime(today.year, today.month, today.day,
                                      tzinfo=today.tzinfo)
        else:
            assert isinstance(date_depth, timedelta)
            today = today - date_depth
        return today


def str_to_timedelta(date_depth_raw):
    date_depth = timedelta(**eval(f'dict({date_depth_raw})'))
    return date_depth
