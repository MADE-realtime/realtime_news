from sqlalchemy.orm import Session

from .models import News
from typing import List
from datetime import date


def get_news(db: Session,
             news_id: int) -> News:
    return db.query(News).filter(News.id == news_id).first()


def get_news_by_filters(db: Session,
                        topic: str,
                        start_date: date,
                        end_date: date,
                        skip: int = 0,
                        limit: int = 100) -> List[News]:
    # TODO: допилить фильтрацию:
    # TODO: если topic == None, то игнорируется
    if topic and start_date and end_date:
        return db.query(News) \
            .filter(News.topic == topic) \
            .filter(News.date >= start_date) \
            .filter(News.date <= end_date) \
            .offset(skip).limit(limit).all()
    else:
        return db.query(News).offset(skip).limit(limit).all()


def get_single_news(db: Session,
                    news_id: int) -> News:
    return db.query(News).get(news_id)


def get_n_last_news(db: Session,
                    skip: int = 0,
                    limit: int = 100) -> List[News]:
    return db.query(News).order_by(News.id.desc()).offset(skip).limit(limit).all()


def get_all_news(db: Session,
                 skip: int = 0,
                 limit: int = 100) -> List[News]:
    return db.query(News).offset(skip).limit(limit).all()


def get_news_by_topic_and_date(db: Session,
                               topic: str,
                               start_date: date,
                               end_date: date,
                               skip: int = 0,
                               limit: int = 100) -> List[News]:
    return db.query(News).filter(News.topic == topic).offset(skip).limit(limit).all()


def get_news_by_date(db: Session,
                     topic: str,
                     start_date: date,
                     end_date: date,
                     skip: int = 0,
                     limit: int = 100) -> List[News]:
    return db.query(News) \
        .filter(News.topic == topic) \
        .filter(News.time >= start_date) \
        .filter(News.time <= end_date) \
        .offset(skip).limit(limit).all()


def create_news(db: Session, news: News):
    db.add(news)
    db.commit()
    db.refresh(news)
    return news
