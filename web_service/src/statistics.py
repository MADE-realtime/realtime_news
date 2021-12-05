from abc import ABC, abstractmethod
from collections import defaultdict

import numpy as np
from typing import Dict, List
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words

from config import LANGUAGE, MIN_NGRAM_FREQ
from models import ListNews, News, StatisticsModels


class Statistics(ABC):
    """
    Basic class for statistics
    """

    @abstractmethod
    def predict(self, news: List[News], *args, **kwargs) -> StatisticsModels:
        pass


class NgramsBuilder(Statistics):
    def __init__(self):
        self.builder = CountVectorizer(
            ngram_range=(2, 4), stop_words=get_stop_words(LANGUAGE)
        )
        self.name = 'Ngrams'

    def predict(self, news: List[News], *args, **kwargs) -> StatisticsModels:
        news_texts = [one_news.content for one_news in news if one_news.content]
        if not news_texts:
            return StatisticsModels(type=self.name, stats=[('none', 0)])
        frequencies = np.array(
            np.sum(self.builder.fit_transform(news_texts).todense(), axis=0)
        )[0]
        vocab = {indice: term for term, indice in self.builder.vocabulary_.items()}
        sorted_args = np.argsort(frequencies)[::-1]
        ans_list = []
        for i_word in sorted_args:
            if frequencies[i_word] >= MIN_NGRAM_FREQ:
                ans_list.append((vocab[i_word], frequencies[i_word]))
        return StatisticsModels(type=self.name, stats=ans_list)


class StatisticsByResource(Statistics):
    """Класс для подсчёта количества ресурсов, которые встретились в выборке новостей"""
    def __init_(self):
        self.name = 'stats_by_day'

    def predict(self, news: List[News], *args, **kwargs) -> StatisticsModels:
        news_counter = defaultdict(int)
        for one_news in news:
            news_counter[one_news.source_name] += 1
        news_counter_list = []
        for source_name, count in news_counter.items():
            news_counter_list.append((source_name, count))
        return StatisticsModels(type=self.name, stats=news_counter)


class ByDayCounter(Statistics):
    """Класс для подсчёта количества упоминаний по дням"""
    def __init_(self):
        self.name = 'count_by_day'

    def predict(self, news: List[News], *args, **kwargs) -> StatisticsModels:
        news_counter = defaultdict(int)
        for one_news in news:
            news_counter[one_news.date] += 1
        news_counter_list = []
        for date, count in news_counter.items():
            news_counter_list.append((date, count))
        return StatisticsModels(type=self.name, stats=news_counter)