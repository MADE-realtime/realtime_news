import re
from abc import ABC, abstractmethod
from scrapy.http import HtmlResponse
PARSER_ZOO = {}


def add_to_zoo(name):
    def add_wrapper(parser_to_add):
        PARSER_ZOO[name] = parser_to_add()
        return parser_to_add
    return add_wrapper


class BaseParser(ABC):
    @abstractmethod
    def parse(self, response: HtmlResponse):
        pass

    @staticmethod
    def join_css_parsed(response, pattern):
        text = [re.sub("<[^>]*>", '', part) for part in response.css(pattern).getall()]
        text = [part.strip() for part in text]
        text = ' '.join(text)
        text = text.replace('\n', '').strip()
        return text


@add_to_zoo('tass')
class TassParser(BaseParser):
    def parse(self, response: HtmlResponse):
        title = self.join_css_parsed(response, '.news-header__title')
        title_post = self.join_css_parsed(response, '.news-header__lead')
        text = self.join_css_parsed(response, 'h2 , #news p')

        parsed_item = {
            'title': title,
            'title_post': title_post,
            'text': text,
        }
        return parsed_item


@add_to_zoo('rbc')
class RBCParser(BaseParser):
    def parse(self, response: HtmlResponse):
        title = self.join_css_parsed(response, '.js-rbcslider-article:nth-child(10) .js-slide-title')
        title_post = self.join_css_parsed(response, '.article__text__overview span')
        text = self.join_css_parsed(response, '.article__text__overview~ p')

        parsed_item = {
            'title': title,
            'title_post': title_post,
            'text': text,
        }
        return parsed_item
