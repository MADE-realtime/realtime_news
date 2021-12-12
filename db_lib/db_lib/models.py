from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    UniqueConstraint
)
from .database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String, unique=True, index=True)
    title = Column(String)
    content = Column(String)
    topic = Column(String)
    tags = Column(String)
    date = Column(Date)
    time = Column(DateTime)
    source_name = Column(String)
    image_url = Column(String)
    logo_url = Column(String)
    title_post = Column(String)


class SocialNetworkNews(Base):
    __tablename__ = "social_network_news"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer)
    text = Column(String)
    date = Column(Date)
    time = Column(DateTime)
    comments = Column(Integer)
    likes = Column(Integer)
    reposts = Column(Integer)
    views = Column(Integer)
    link = Column(String)
    source_name = Column(String)
    social_network = Column(String)
    __table_args__ = (
        UniqueConstraint(
            'social_network',
            'post_id',
            name='_sn_post_id_uc'
        ),
    )


class SocialNetworkStats(Base):
    __tablename__ = "social_network_stats"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer)
    comments = Column(Integer)
    likes = Column(Integer)
    reposts = Column(Integer)
    views = Column(Integer)
    social_network = Column(String)


class RequestInfo(Base):
    __tablename__ = "request_info"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    method = Column(String)
    host = Column(String)
    user_agent = Column(String)
