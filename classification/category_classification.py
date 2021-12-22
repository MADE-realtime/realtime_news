import pickle
from pathlib import Path
from typing import List, Any

from datetime import date
from db_lib.crud import get_news_by_filters
from db_lib.models import News
from db_lib.database import SessionLocal
from sqlalchemy.orm import Session
import click

from classification.config import PATH_TO_CATEGORIES_CLASSIFICATOR


def download_model(model_path: Path = PATH_TO_CATEGORIES_CLASSIFICATOR) -> Any:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def _preprocess_messages(news_list: List[News]) -> List[str]:
    news_texts = [news.content for news in news_list]
    news_texts = [text.replace('[^\\w\\s]', '').lower() for text in news_texts]
    return news_texts


def classify_news_content(news_list: List[News], path: Path = PATH_TO_CATEGORIES_CLASSIFICATOR) -> List[str]:
    model = download_model(path)
    news_texts = _preprocess_messages(news_list)
    classes = model.predict(news_texts)
    return classes


@click.command()
@click.option("--start_date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
@click.option("--end_date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
def classify_messages(start_date: date, end_date: date, db: Session = SessionLocal()):

    """Загружаем все сообщения (пока сообщений немного) и классифицируем их с помощью модели"""

    news_list = get_news_by_filters(db, topic=None, start_date=start_date, end_date=end_date, limit=LIMIT_NEWS)
    classes = classify_news_content(news_list)
    for i in range(len(news_list)):
        news_list[i].category = classes[i]
    db.commit()


if __name__ == '__main__':
    classify_messages()