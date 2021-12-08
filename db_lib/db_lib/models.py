from sqlalchemy import Column, Integer, String, Date, DateTime
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
