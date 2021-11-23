import datetime

from scrapy.spiders import SitemapSpider

from data_collection.parser_zoo import PARSER_ZOO
from data_collection.util import read_urls_file, read_rule_file


class NewsSpider(SitemapSpider):
    name = 'rta'

    def __init__(self, sitemap_urls_fpath=None, sitemap_rules_fpath=None, date_depth=None, *args, **kwargs):
        sitemap_urls = read_urls_file(sitemap_urls_fpath)
        sitemap_rules = read_rule_file(sitemap_rules_fpath)
        self.sitemap_urls = sitemap_urls or []
        self.sitemap_rules = [(domain, PARSER_ZOO[parser_name].parse) for domain, parser_name in sitemap_rules]

        self.date_depth = date_depth or self.get_date_beggining()
        super(NewsSpider, self).__init__(*args, **kwargs)

    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = datetime.datetime.strptime(entry['lastmod'], '%Y-%m-%dT%H:%M:%S%z')
            if date_time >= self.date_depth:
                yield entry

    @staticmethod
    def get_date_beggining():
        today = datetime.datetime.today()
        today = datetime.datetime(today.year, today.month, today.day,
                                  tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)))
        return today