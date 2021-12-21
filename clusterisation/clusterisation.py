from typing import List

from sklearn.cluster import AgglomerativeClustering
import fasttext.util
import numpy as np

from datetime import date
from db_lib.crud import get_news_by_filters
from config import LANGUAGE_SHORT_FOR_FASTTEXT, LIMIT_NEWS
from db_lib.models import News
from db_lib.database import SessionLocal
from sqlalchemy.orm import Session
import click
import numpy


def download_language_model():
    fasttext.util.download_model(LANGUAGE_SHORT_FOR_FASTTEXT, if_exists='ignore')
    model = fasttext.load_model(f'cc.{LANGUAGE_SHORT_FOR_FASTTEXT}.300.bin')
    return model


def clean_nones_from_content(news_list: List[News]) -> List[News]:
    for i, news in enumerate(news_list):
        if news.content is None:
            news_list[i].content = news.title
    return news_list


def cluster_news_content(news_list: List[News]) -> np.ndarray:
    if not news_list:
        return numpy.array(news_list)

    model = download_language_model()
    clusterer = AgglomerativeClustering(
        n_clusters=None,
        affinity='cosine',
        linkage='complete',
        distance_threshold=0.25,
    )
    # news_list = clean_nones_from_content(news_list)
    # content_emb = [model[one_news.content] for one_news in news_list]
    title_emb = [model[one_news.title] for one_news in news_list]
    clusters = clusterer.fit_predict(title_emb)
    return clusters


@click.command()
@click.option("--start_date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
@click.option("--end_date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
def cluster_messages(start_date: date, end_date: date, db: Session = SessionLocal()):

    """Загружаем все сообщения (пока сообщений немного) и кластеризуем их с помощью кластеризатора"""

    news_list = get_news_by_filters(db, topic=None, start_date=start_date, end_date=end_date, limit=LIMIT_NEWS)
    cluster_num = cluster_news_content(news_list)
    for i in range(len(news_list)):
        news_list[i].cluster_num = cluster_num[i].item()
    db.commit()


if __name__ == '__main__':
    cluster_messages()