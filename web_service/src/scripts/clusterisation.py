from typing import List

from sklearn.cluster import AgglomerativeClustering
import fasttext.util
import numpy as np

from db_lib.db_lib.crud import get_all_news
# from db_lib.db_lib.models import News
from web_service.src.config import LANGUAGE_SHORT_FOR_FASTTEXT, LIMIT_NEWS
from web_service.src.models import News
from web_service.src.news_extractor import clean_nones_from_content


def download_language_model():
    fasttext.util.download_model(LANGUAGE_SHORT_FOR_FASTTEXT, if_exists='ignore')
    model = fasttext.load_model(f'cc.{LANGUAGE_SHORT_FOR_FASTTEXT}.300.bin')
    return model


def cluster_news_content(news_list: List[News]) -> np.ndarray:
    model = download_language_model()
    clusterer = AgglomerativeClustering(
        n_clusters=None,
        affinity='cosine',
        linkage='complete',
        distance_threshold=0.25,
    )
    news_list = clean_nones_from_content(news_list)
    content_emb = [model[one_news.content] for one_news in news_list]
    clusters = clusterer.fit_predict(content_emb)
    return clusters


def write_clusters_num_to_db(cluster_num: np.ndarray):
    ...


def cluster_messages():
    '''Загружаем все сообщения (пока сообщений немного) и кластеризуем их с помощью кластеризатора'''
    news_list = get_all_news(limin=LIMIT_NEWS)
    cluster_num = cluster_news_content(news_list)
    write_clusters_num_to_db(cluster_num)


if __name__ == '__main__':
    cluster_messages()