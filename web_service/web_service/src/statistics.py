import pickle
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from stop_words import get_stop_words
from wordcloud import WordCloud

from web_service.web_service.src.config import LANGUAGE, MIN_NGRAM_FREQ, CLASS_OF_NEWS, \
    PATH_TO_CATEGORIES_CLASSIFICATOR, WORDCLOUD_IMAGE_NAME, PATH_TO_SAVE_IMAGE
from web_service.web_service.src.models import ListNews, News, StatisticsModels


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

    def predict(self, news: List[News], cnt: int = 0, *args, **kwargs) -> StatisticsModels:
        news_texts = [one_news.content for one_news in news if one_news.content]
        news_texts = self._cut_non_cyrillic_characters(news_texts)
        self.build_word_count_image(news_texts, cnt)
        if not news_texts:
            return StatisticsModels(type=self.name, stats=[('none', 0)])
        frequencies = np.array(
            np.sum(self.builder.fit_transform(news_texts).todense(), axis=0)
        )[0]
        vocab = {indice: term for term, indice in self.builder.vocabulary_.items()}
        sorted_args = np.argsort(frequencies)[::-1]
        ans_list = []
        for i_word in sorted_args:
            if frequencies[i_word] >= MIN_NGRAM_FREQ and self._has_cyrillic(vocab[i_word]):
                ans_list.append((vocab[i_word], frequencies[i_word]))
        return StatisticsModels(type=self.name, stats=ans_list)

    @staticmethod
    def _cut_non_cyrillic_characters(news_texts: List[str]) -> List[str]:
        CLEANR = re.compile('<.*?>')
        news_texts = [re.sub(CLEANR, '', text) for text in news_texts]
        news_texts = [re.sub(r'[a-zA-Z]', '', text) for text in news_texts]
        news_texts = [text for text in news_texts if text != '']
        return news_texts

    @staticmethod
    def _has_cyrillic(text):
        return bool(re.search('[а-яА-Я]', text))

    @staticmethod
    def build_word_count_image(news_texts: List[str], cnt: int = 2) -> None:
        wordcloud = WordCloud(
            stopwords=get_stop_words(LANGUAGE)
        ).generate(text=''.join(news_texts))
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(PATH_TO_SAVE_IMAGE / Path(f'{WORDCLOUD_IMAGE_NAME}_{cnt}.png'))
        return None


class StatisticsByResource(Statistics):
    """Класс для подсчёта количества ресурсов, которые встретились в выборке новостей"""
    def __init__(self):
        self.name = 'stats_by_day'

    def predict(self, news: List[News], *args, **kwargs) -> StatisticsModels:
        news_counter = defaultdict(int)
        for one_news in news:
            if one_news.source_name:
                news_counter[one_news.source_name] += 1
        news_counter_list = sorted(news_counter.items(), key=lambda kv: kv[1], reverse=True)

        return StatisticsModels(type=self.name, stats=news_counter_list)


class ByDayCounter(Statistics):
    """Класс для подсчёта количества упоминаний по дням"""
    def __init__(self):
        self.name = 'count_by_day'

    def predict(self, news: List[News], *args, **kwargs) -> StatisticsModels:
        news_counter = defaultdict(int)
        for one_news in news:
            if one_news.date:
                news_counter[one_news.date.strftime("%d.%m.%Y")] += 1
        news_counter_list = sorted(news_counter.items(), key=lambda kv: datetime.strptime(kv[0], '%d.%m.%Y'))

        return StatisticsModels(type=self.name, stats=news_counter_list)


class CategoriesClassificator(Statistics):
        def __init__(self, path_to_classifier: Path = PATH_TO_CATEGORIES_CLASSIFICATOR):
            with open(path_to_classifier, 'rb') as file:
                self.builder = pickle.load(file)
            self.name = 'news_categories'
            self.class_news = CLASS_OF_NEWS

        def predict(self, news: List[News], *args, **kwargs) -> StatisticsModels:
            news_texts = [one_news.content for one_news in news if one_news.content]
            news_texts = self._preprocessing(news_texts)
            if not news_texts:
                return StatisticsModels(type=self.name, stats='')
            ans_list = self.builder.predict(news_texts)
            ans_list = [
                (
                    self.class_news[np.where(ans == 1)[0][0]], i
                ) for i, ans in enumerate(ans_list)
            ]

            return StatisticsModels(type=self.name, stats=ans_list)
    
        @staticmethod
        def _preprocessing(news_texts: List[str]) -> List[str]:
            news_texts = [text.replace('[^\\w\\s]', '').lower() for text in news_texts]
            return news_texts
