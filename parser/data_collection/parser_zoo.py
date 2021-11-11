import re
from abc import ABC, abstractmethod
from html.parser import HTMLParser

from scrapy.http import HtmlResponse
PARSER_ZOO = {}


def add_to_zoo(name):
    def add_wrapper(parser_to_add):
        PARSER_ZOO[name] = parser_to_add()
        return parser_to_add
    return add_wrapper


class AttrParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = attrs


class BaseParser(ABC):
    @abstractmethod
    def parse(self, response: HtmlResponse):
        pass

    @staticmethod
    def join_css_parsed(response, pattern):
        text = [re.sub("<[^>]*>", '', part) for part in response.css(pattern).getall()]
        text = [part.strip() for part in text]
        text = [part for part in text if part]
        text = ' '.join(text)
        text = text.replace('\n', '').strip()
        text = text.replace('\xa0', ' ')
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
            'source_url': response.url,
        }
        return parsed_item


@add_to_zoo('rbc')
class RBCParser(BaseParser):
    def parse(self, response: HtmlResponse):
        parsed_item = {}
        for i in range(10, 12):
            title = self.join_css_parsed(response, f'.js-rbcslider-article:nth-child({i}) .js-slide-title')
            if not title:
                continue
            title_post = self.join_css_parsed(response, '.article__text__overview span')
            text = self.join_css_parsed(response, f'.js-rbcslider-article:nth-child({i}) p')
            image_url = self.parse_image(response, i)

            parsed_item = {
                'title': title,
                'title_post': title_post,
                'text': text,
                'image_url': image_url
            }
            break
        parsed_item['source_url'] = response.url
        return parsed_item

    @staticmethod
    def parse_image(response: HtmlResponse, idx):
        css_select = f'.js-rbcslider-article:nth-child({idx}) .article__main-image__image'
        selected_tags = response.css(css_select).getall()
        if len(selected_tags) == 0:
            return ''
        img_tag = selected_tags[0]
        attr_parser = AttrParser()
        attr_parser.feed(img_tag)
        img_url = dict(attr_parser.attrs)['srcset'].split(' ')[0]
        return img_url


@add_to_zoo('ria')
class RIAParser(BaseParser):
    def parse(self, response: HtmlResponse):
        title = self.join_css_parsed(response, '.m-active .article__title')
        title_post = self.join_css_parsed(response, '.m-active .article__second-title')
        text = self.join_css_parsed(response, '.layout-article:nth-child(1) .article__text')
        image_url = self.parse_image(response)

        parsed_item = {
            'title': title,
            'title_post': title_post,
            'text': text,
            'source_url': response.url,
            'image_url': image_url,
        }
        return parsed_item

    @staticmethod
    def parse_image(response: HtmlResponse):
        css_select = '.layout-article:nth-child(1) .photoview__open img'
        selected_tags = response.css(css_select).getall()
        if len(selected_tags) == 0:
            return ''
        img_tag = selected_tags[0]
        attr_parser = AttrParser()
        attr_parser.feed(img_tag)
        img_url = dict(attr_parser.attrs)['srcset'].split(' ')[0]
        return img_url

