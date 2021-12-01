from sqlalchemy.orm import Session

from .models import News
from typing import List
from datetime import date


def get_news(db: Session,
             news_id: int) -> News:
    return db.query(News).filter(News.id == news_id).first()


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
    return db.query(News)\
        .filter(News.topic == topic)\
        .filter(News.time >= start_date)\
        .filter(News.time <= end_date)\
        .offset(skip).limit(limit).all()


def create_news(db: Session, news: News):
    db.add(news)
    db.commit()
    db.refresh(news)
    return news
