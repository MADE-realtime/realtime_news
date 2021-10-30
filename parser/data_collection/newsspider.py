from datetime import datetime

from scrapy.spiders import SitemapSpider

from data_collection.parser_zoo import PARSER_ZOO


class NewsSpider(SitemapSpider):
    name = 'rta'

    def __init__(self, sitemap_urls=None, sitemap_rules=None, date_depth=None, *args, **kwargs):
        self.sitemap_urls = sitemap_urls or []
        self.sitemap_rules = [(domain, PARSER_ZOO[parser_name].parse) for domain, parser_name in sitemap_rules]

        self.date_depth = date_depth or datetime.today()
        super(NewsSpider, self).__init__(*args, **kwargs)

    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = datetime.strptime(entry['lastmod'], '%Y-%m-%d')
            if date_time >= date_time:
                yield entry