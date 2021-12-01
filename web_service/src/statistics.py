from abc import ABC, abstractmethod

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words

from config import LANGUAGE
from models import ListNews, StatisticsModels


class Statistics(ABC):
    """
    Basic class for statistics
    """

    @abstractmethod
    def predict(self, news: ListNews) -> StatisticsModels:
        pass


class NgramsBuilder(Statistics):
    def __init__(self):
        self.builder = CountVectorizer(
            ngram_range=(2, 4), stop_words=get_stop_words(LANGUAGE)
        )
        self.name = 'Ngrams'

    def predict(self, news: ListNews) -> StatisticsModels:
        news_texts = [one_news['contents'] for one_news in news]
        frequencies = np.array(
            np.sum(self.builder.fit_transform(news_texts).todense(), axis=0)
        )[0]
        vocab = self.builder.vocabulary_
        sorted_args = np.argsort(frequencies)[::-1]
        ans_list = []
        for word_i in sorted_args:
            if frequencies[word_i] > 1:
                ans_list.append((vocab[word_i], word_i))
        return StatisticsModels(**{'type': self.name, 'stats': ans_list})
