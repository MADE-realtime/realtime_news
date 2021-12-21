from sqlalchemy.orm import Session

from .models import News, SocialNetworkNews
from typing import List, Any
from datetime import date


def get_news(db: Session,
             news_id: int) -> News:
    return db.query(News).filter(News.id == news_id).first()


def get_all_news_by_id(db: Session, news_ids: List[int]) -> List[News]:
    return db.query(News).filter(News.id in news_ids)


def get_news_by_filters(db: Session,
                        topic: str,
                        start_date: date,
                        end_date: date,
                        skip: int = 0,
                        limit: int = 100) -> List[News]:
    if topic:
        return db.query(News) \
            .order_by(News.time.desc())\
            .filter(News.topic == topic) \
            .filter(News.date >= start_date) \
            .filter(News.date <= end_date) \
            .offset(skip).limit(limit).all()
    else:
        return db.query(News) \
            .order_by(News.time.desc())\
            .filter(News.date >= start_date) \
            .filter(News.date <= end_date) \
            .offset(skip).limit(limit).all()


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

def get_news_without_cluster(db: Session,
                             skip: int = 0,
                             limit: int = 1000) -> List[News]:
    return db.query(News)\
        .filter(News.cluster_num.isnot(None)) \
        .offset(skip).limit(limit).all()


def get_news_count(db: Session) -> int:
    news_count = db.query(News.id).count()
    social_news_count = db.query(SocialNetworkNews.id).count()
    return news_count + social_news_count


def create_news(db: Session, news: News):
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def save_all_news(db: Session, news_list: List[News]) -> List[News]:
    db.add_all(news_list)
    db.commit()
    db.refresh(news_list)
    return news_list
