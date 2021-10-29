import re
from scrapy.http import HtmlResponse
PARSER_ZOO = {}


def add_to_zoo(name):
    def add_wrapper(parser_to_add):
        PARSER_ZOO[name] = parser_to_add()
        return parser_to_add
    return add_wrapper


@add_to_zoo('tass')
class TassParser:
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

    def join_css_parsed(self, response, pattern):
        text = [part.strip() for part in response.css(pattern).getall()]
        text = ' '.join(text)
        text = re.sub("<[^>]*>", '', text)
        text = text.replace('\n', '').strip()
        return text