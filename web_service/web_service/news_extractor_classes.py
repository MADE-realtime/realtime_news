from abc import ABC, abstractmethod
from pathlib import Path


import pandas as pd
from models import ListNews, News
from utils import convert_str_to_date


class BaseNewsExtractor(ABC):
    """
    Предполагается использовать этот класс как прародитель для всех
    остальных при обращении к разным источникам данных
    """

    @abstractmethod
    def show_random_news(self):
        """
        Метод для показа нескольких случаных новостей
        """
        pass

    @abstractmethod
    def show_news_by_day(self):
        """
        Метод для показа новостей за конкретный день
        """
        pass

    @abstractmethod
    def show_news_by_topic(self):
        """
        Метод для показа новостей по определённой теме
        """
        pass


class PandasNewsExtractor(BaseNewsExtractor):
    def __init__(self, path_to_df: Path):
        self.source_df = pd.read_csv(path_to_df, parse_dates=['date'])

    def show_random_news(self, num_random_news: int = 10) -> ListNews:
        df_random = self.source_df.sample(n=num_random_news)
        news_list = self._convert_df_to_list_news(df_random)
        return news_list

    def show_news_by_day(self, selected_date: str = '1991-12-05') -> ListNews:
        selected_date = convert_str_to_date(selected_date)
        df_date = self.source_df[self.source_df['date'] == selected_date]
        news_list = self._convert_df_to_list_news(df_date)
        return news_list

    def show_news_by_topic(self, topic: str) -> ListNews:
        df_topic = self.source_df[self.source_df['topic'] == topic]
        news_list = self._convert_df_to_list_news(df_topic)
        return news_list

    @staticmethod
    def _convert_df_to_list_news(self, selected_df: pd.DataFrame) -> ListNews:
        news_list = [None] * len(selected_df)
        for i, row in selected_df.iterrows():
            news_list[i] = self._convert_row_to_news(row)
        news_list_dict = {'news_list': news_list}
        return ListNews(**news_list_dict)

    @staticmethod
    def _convert_row_to_news(row) -> News:
        news_dict = {
            'url': row['url'],
            'title': row['title'],
            'text': row['text'],
            'topic': row['topic'],
            'tags': row['tags'],
            'date': row['date'],
        }
        return News(**news_dict)
