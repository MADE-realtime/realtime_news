from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .models import News, SocialNetworkNews, SocialNetworkStats
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


def get_social_network_news(db: Session,
                            news_id: int) -> SocialNetworkNews:
    return db.query(SocialNetworkNews) \
        .filter(SocialNetworkNews.id == news_id).first()


def get_social_network_stats(db: Session,
                             post_id: int,
                             social_network: str) -> SocialNetworkStats:
    return db.query(SocialNetworkStats) \
        .filter(SocialNetworkStats.post_id == post_id)\
        .filter(SocialNetworkStats.social_network == social_network)\
        .all()


def get_social_network_stats_by_domain(db: Session,
                                       domain: str) -> SocialNetworkStats:
    join_expression = (SocialNetworkStats.post_id == SocialNetworkNews.post_id) & \
                      (SocialNetworkStats.social_network == SocialNetworkNews.social_network)
    query = [
        func.max(SocialNetworkStats.comments).label('comments'),
        func.max(SocialNetworkStats.reposts).label('reposts'),
        func.max(SocialNetworkStats.views).label('views'),
        func.max(SocialNetworkStats.likes).label('likes'),
    ]
    return db.query(query) \
        .join(SocialNetworkNews, join_expression)\
        .filter(SocialNetworkNews.source_name == domain)\
        .group_by(
            SocialNetworkStats.post_id,
            SocialNetworkNews.date,
            SocialNetworkNews.social_network
        )\
        .all()


def create_news(db: Session, news: News):
    db.add(news)
    db.commit()
    db.refresh(news)
    return news
