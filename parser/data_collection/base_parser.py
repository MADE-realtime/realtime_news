from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def scrap_from(self, news_source):
        pass

    @abstractmethod
    def parse_page(self, html_page):
        pass

    @abstractmethod
    def follow_link(self, link_url):
        pass
