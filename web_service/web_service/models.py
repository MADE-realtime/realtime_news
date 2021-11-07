from datetime import date, datetime
from typing import List

from pydantic import BaseModel

from config import DEFAULT_NEWS_IMAGE_URL, DEFAULT_LOGO_URL


class News(BaseModel):
    source_url: str
    title: str
    content: str
    topic: str = 'Новость'
    tags: str = 'Новость'
    date: date
    time: datetime
    source_name: str = 'Наша газета'
    image_url: str = DEFAULT_NEWS_IMAGE_URL
    logo_url: str = DEFAULT_LOGO_URL


class ListNews(BaseModel):
    news_list: List[News]
    statistics: None
