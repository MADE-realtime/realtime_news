from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http import Response, Request, XmlResponse


class ParserRSS(Spider):
    name = 'parser_rss'

    def __init__(self, start_urls=None, *args, **kwargs):
        self.start_urls = start_urls or []
        self.link_extractor = LxmlLinkExtractor(allow=(
            '.*\/rss.*',
            '.*\/feed.*'
        ))
        super(ParserRSS, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_main)

    def parse_main(self, response: Response):
        for url in self.link_extractor.extract_links(response):
            return Request(url, callback=self.parse_rss)

    def parse_rss(self, response: XmlResponse):
        pass
