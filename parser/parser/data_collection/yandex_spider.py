from argparse import ArgumentParser

from bs4 import BeautifulSoup
from scrapy.http import Request, HtmlResponse
from scrapy.spiders import Spider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from data_collection.util import read_file


def setup_ys_parser(parser: ArgumentParser):
    parser.add_argument(
        '-yandex_page',
        help='Path to html file from yandex news bd',
        dest='yandex_page_path',
        type=str,
        required=True
    )
    parser.set_defaults(setup_kwargs=setup_ys_kwargs, spider=YandexNewsSpider)
    return parser


def setup_ys_kwargs(yandex_page_path):
    yandex_page = read_file(yandex_page_path)
    kwargs = {'yandex_page': yandex_page}
    return kwargs


class YandexNewsSpider(Spider):

    name = 'yandex_smi_spider'

    def __init__(self, yandex_page, *args, **kwargs):
        super(YandexNewsSpider, self).__init__(*args, **kwargs)
        self.yandex_page = yandex_page
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


