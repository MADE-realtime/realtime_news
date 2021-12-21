import random
import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd
from models import ListNews, News
from sqlalchemy.orm import Session
from utils import convert_str_to_date

from config import LIMIT_NEWS
from db_lib import crud
from db_lib.database import SessionLocal
from statistics import NgramsBuilder, StatisticsByResource, ByDayCounter, CategoriesClassificator


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
    def show_news_by_topic(
            self, db: Session, topic: str, start_date: str, end_date: str
    ):
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

    @abstractmethod
    def show_news_by_regex(self, db: Session, word: str, mode: str, cnt: int):
        """
        Метод для поиска новостей по регулярному выражению
        """
        pass

    @abstractmethod
    def show_single_news(self, db: Session, news_id: int):
        """
        Метод для показа новости по id
        """
        pass

    def show_vk_tg_news(self, db, news_id):
        pass

    def show_vk_tg_stat(self, db, post_id, social_network):
        pass


class PandasNewsExtractor(BaseNewsExtractor):
    def __init__(self, path_to_df: Path):
        self.source_df = pd.read_csv(path_to_df, parse_dates=['date'])
        self.source_df['date'] = self.source_df['date'].map(lambda x: x.date())

    def show_random_news(self, num_random_news: int = 10, **kwargs) -> ListNews:
        df_random = self.source_df.sample(n=num_random_news)
        news_list = self._convert_df_to_list_news(df_random)
        return news_list

    def show_news_by_days(
            self,
            start_date: str = '1991-05-12',
            end_date: str = '1991-05-12',
            **kwargs,
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
            **kwargs,
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

    def show_random_news(self, db: Session, num_random_news: int = 10) -> ListNews:
        news_list = random.choices(crud.get_all_news(db), k=num_random_news)
        return ListNews(
            **{'news_list': news_list, 'statistics': [
                NgramsBuilder().predict(news_list, )
            ]}
        )

    def show_news_by_days(
            self, db, start_date: str = '1991-05-12', end_date: str = '1991-05-12'
    ) -> ListNews:
        news_list = crud.get_news_by_date(
            db, convert_str_to_date(start_date), convert_str_to_date(end_date)
        )
        return ListNews(
            **{'news_list': news_list, 'statistics': [
                NgramsBuilder().predict(news_list)
            ]}
        )

    def show_news_by_topic(
            self,
            db,
            topic: str = 'Футбол',
            start_date: str = '1991-05-12',
            end_date: str = '1991-05-12',
    ) -> ListNews:
        news_list = crud.get_news_by_topic_and_date(
            db, topic, convert_str_to_date(start_date), convert_str_to_date(end_date)
        )
        return ListNews(
            **{'news_list': news_list, 'statistics': [
                NgramsBuilder().predict(news_list, )
            ]}
        )

    def show_news_by_filters(
            self,
            db: Session,
            topic: str,
            end_date: str,
            start_date: str = '1991-05-12',
            num_news: int = 10,
    ) -> ListNews:
        news_list = crud.get_news_by_filters(db,
                                             topic=topic,
                                             start_date=convert_str_to_date(start_date),
                                             end_date=convert_str_to_date(end_date),
                                             limit=num_news)
        # news_list_len = len(news_list)
        # if num_news > news_list_len:
        #     num_news = news_list_len
        # news_list = random.choices(news_list, k=num_random_news)
        news_list = _clean_img_urls(news_list)

        # Не менять порядок в statistics
        return ListNews.parse_obj(
            {
                'news_list': news_list,
                'statistics': [
                    NgramsBuilder().predict(news_list),
                    StatisticsByResource().predict(news_list),
                    ByDayCounter().predict(news_list),
                ]
            }
        )

    def show_news_by_regex(self, db: Session, word: str, mode: str = 'full', cnt: int = 2) -> ListNews:
        if word:
            news_list = crud.get_n_last_news(db, limit=LIMIT_NEWS)
        else:
            news_list = crud.get_all_news(db, limit=0)
        word_re = rf'\b{word}\b'
        if mode == 'full':
            selected_news = [
                one_news for one_news in news_list if re.search(word_re, _one_news_to_string(one_news), flags=re.IGNORECASE)
            ]
        else:
            news_list = clean_nones_from_content(news_list)
            selected_news = [
                one_news for one_news in news_list if re.search(word_re, str(one_news.content), flags=re.IGNORECASE)
            ]
        selected_news = _clean_img_urls(selected_news)

        # Не менять порядок в statistics
        return ListNews.parse_obj(
            {
                'news_list': selected_news,
                'statistics': [
                    NgramsBuilder().predict(selected_news, cnt),
                    StatisticsByResource().predict(selected_news),
                    ByDayCounter().predict(selected_news),
                ]
            }
        )

    def show_single_news(self, db: Session, news_id: int) -> Dict:
        single_news = crud.get_single_news(db, news_id)
        single_news.image_url = _remove_extra_link(single_news.image_url)
        return {
            'single_news': single_news,
        }

    def show_vk_tg_news(self, db: Session, news_id: int) -> Dict:
        vk_tg_news = crud.get_social_network_news(db, news_id)
        return {
            'single_news': vk_tg_news,
        }

    def show_vk_tg_stat(self, db: Session, post_id: int, social_network: str):
        vk_tg_stat = crud.get_social_network_stats(db, post_id, social_network)  # List[SocialNetworkStats]
        return vk_tg_stat



def _to_str(text):
    return '' if text is None else str(text)


def _one_news_to_string(one_news: News) -> str:
    return _to_str(one_news.title) + ' ' + _to_str(one_news.content)


def clean_nones_from_content(news_list: List[News]) -> List[News]:
    for i, news in enumerate(news_list):
        if news.content is None:
            news_list[i].content = news.title
    return news_list


def _clean_img_urls(news_list: List[News]) -> List[News]:
    for i, news in enumerate(news_list):
        news_list[i].image_url = _remove_extra_link(news_list[i].image_url)
    return news_list


def _remove_extra_link(links: str) -> str:
    if links:
        return links.lstrip('{').rstrip('}').split(',')[0]
