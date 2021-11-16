from sqlalchemy import Column, Integer, String, Date, DateTime
from .database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String)
    title = Column(String)
    content = Column(String)
    topic = Column(String, default='Новость')
    tags = Column(String, default='Новость')
    date = Column(Date)
    time = Column(DateTime)
    source_name = Column(String, default='Наша газета')
    image_url = Column(String)
    logo_url = Column(String)
