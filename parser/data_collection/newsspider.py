from datetime import datetime

from scrapy.spiders import SitemapSpider
from scrapy.linkextractors import LinkExtractor


class NewsSpider(SitemapSpider):
    name = 'rta'

    def __init__(self, sitemap_urls=None, date_depth=None, *args, **kwargs):
        self.sitemap_urls = sitemap_urls or []
        self.date_depth = date_depth or datetime.today()
        super(NewsSpider, self).__init__()

    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = datetime.strptime(entry['lastmod'], '%Y-%m-%d')
            if date_time >= date_time:
                yield entry