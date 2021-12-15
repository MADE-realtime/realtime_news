from datetime import date, datetime
from typing import List, Tuple

from config import DEFAULT_LOGO_URL, DEFAULT_NEWS_IMAGE_URL
from pydantic import BaseModel
from typing import Optional


class News(BaseModel):
    id: int = None
    source_url: str = None
    title: str = None
    content: str = None
    topic: str = None
    tags: str = None
    date: Optional[date]
    time: Optional[datetime]
    source_name: str = None
    image_url: str = None
    logo_url: str = None

    class Config:
        orm_mode = True


class StatisticsModels(BaseModel):
    type: str
    stats: List[Tuple[str, int]]


class ListNews(BaseModel):
    news_list: List[News]
    statistics: List[StatisticsModels]
