from bs4 import BeautifulSoup
from scrapy.http import Request, HtmlResponse
from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from data_collection.util import read_file


class YandexNewsSpider(Spider):
    name = 'yandex_smi_spider'

    def __init__(self, yandex_page_path, *args, **kwargs):
        super(YandexNewsSpider, self).__init__(*args, **kwargs)
        self.yandex_page = read_file(yandex_page_path)
        self.link_extractor = LxmlLinkExtractor(
            restrict_css='.smi__group'
        )

    def start_requests(self):
        soup = BeautifulSoup(self.yandex_page, 'html')
        for smi_tag in soup.find_all('div', class_='smi__group'):
            yandex_smi_url = smi_tag.find('a').attrs['href']
            yield Request(yandex_smi_url, callback=self.parse_smi_page)

    @staticmethod
    def parse_smi_page(response: HtmlResponse):
        smi_url = response.xpath('//dl[@class="smi__website"]//a/@href').get()
        return {'url': smi_url}
