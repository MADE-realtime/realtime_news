from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import pandas as pd
import random
from models import ListNews, News
from typing import Dict
from utils import convert_str_to_date

from sqlalchemy.orm import Session

from db_lib import crud
from db_lib.database import SessionLocal


class BaseNewsExtractor(ABC):
    """
    Предполагается использовать этот класс как прародитель для всех
    остальных при обращении к разным источникам данных
    """

    @abstractmethod
    def show_random_news(self, db: Session, num_random_news: int) -> ListNews:
        """
        Метод для показа нескольких случаных новостей
        """
        pass

    @abstractmethod
    def show_news_by_days(self, db: Session, start_date: str, end_date: str):
        """
        Метод для показа новостей за конкретный день
        """
        pass

    @abstractmethod
    def show_news_by_topic(self, db: Session, topic: str, start_date: str, end_date: str):
        """
        Метод для показа новостей по определённой теме
        """
        pass

    @abstractmethod
    def show_news_by_filters(self, db: Session, topic: str, end_date: str, start_date: str, num_random_news: int):
        """
        Метод для показа новостей по заданным фильтрам
        """
        pass


class PandasNewsExtractor(BaseNewsExtractor):
    def __init__(self, path_to_df: Path):
        self.source_df = pd.read_csv(path_to_df, parse_dates=['date'])
        self.source_df['date'] = self.source_df['date'].map(lambda x: x.date())

    def show_random_news(self, num_random_news: int = 10) -> ListNews:
        df_random = self.source_df.sample(n=num_random_news)
        news_list = self._convert_df_to_list_news(df_random)
        return news_list

    def show_news_by_days(
            self,
            start_date: str = '1991-05-12',
            end_date: str = '1991-05-12',
    ) -> ListNews:
        start_date = convert_str_to_date(start_date)
        end_date = convert_str_to_date(end_date)
        df_date = self.source_df[
            (self.source_df['date'] >= start_date)
            & (self.source_df['date'] <= end_date)
            ]
        news_list = self._convert_df_to_list_news(df_date)
        return news_list

    def show_news_by_topic(
            self,
            topic: str = 'Футбол',
            start_date: str = '1991-05-12',
            end_date: str = '1991-05-12',
    ) -> ListNews:
        start_date = convert_str_to_date(start_date)
        end_date = convert_str_to_date(end_date)
        df_topic = self.source_df[
            (self.source_df['topic'] == topic)
            & (self.source_df['date'] >= start_date)
            & (self.source_df['date'] <= end_date)
            ]
        news_list = self._convert_df_to_list_news(df_topic)
        return news_list

    def _convert_df_to_list_news(self, selected_df: pd.DataFrame) -> ListNews:
        news_list = [None] * len(selected_df)
        for i, (_, row) in enumerate(selected_df.iterrows()):
            news_list[i] = self._convert_row_to_news(row)
        news_list_dict = {'news_list': news_list}
        # TODO here one can add interesting statistics
        news_list_dict['statistics'] = None
        return ListNews(**news_list_dict)

    @staticmethod
    def _convert_row_to_news(row) -> News:
        news_dict = {
            'source_url': row['url'],
            'title': row['title'],
            'content': row['text'],
            'topic': row['topic'],
            'tags': row['tags'],
            'date': row['date'],
            'time': datetime.combine(row['date'], datetime.min.time()),
        }
        return News(**news_dict)


class DBNewsExtractor(BaseNewsExtractor):

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def show_random_news(self, db: Session, num_random_news: int = 10) -> Dict:
        return {'news_list': random.choices(crud.get_all_news(db), k=num_random_news),
                'statistics': None}

    def show_news_by_days(self,
                          db,
                          start_date: str = '1991-05-12',
                          end_date: str = '1991-05-12') -> Dict:
        return {'news_list': crud.get_news_by_date(db, convert_str_to_date(start_date), convert_str_to_date(end_date)),
                'statistics': None}

    def show_news_by_topic(self,
                           db,
                           topic: str = 'Футбол',
                           start_date: str = '1991-05-12',
                           end_date: str = '1991-05-12') -> Dict:
        return {'news_list': crud.get_news_by_topic_and_date(db, topic,
                                                             convert_str_to_date(start_date),
                                                             convert_str_to_date(end_date)),
                'statistics': None}

    def show_news_by_filters(self,
                             db: Session,
                             topic: str,
                             end_date: str,
                             start_date: str = '1991-05-12',
                             num_random_news: int = 10,
                             ) -> Dict:
        news_list = crud.get_news_with_filters(db, topic, start_date, end_date)
        news_list_len = len(news_list)
        if num_random_news > news_list_len:
            num_random_news = news_list_len
        return {'news_list': random.choices(news_list, k=num_random_news),
                'statistics': None}
