from datetime import date, datetime
from typing import List, Tuple

from pydantic import BaseModel
from typing import Optional


class News(BaseModel):
    id: int = None
    source_url: str = None
    title: str = None
    content: str = None
    topic: str = None
    tags: Optional[List[str]] = None
    date: Optional[date]
    time: Optional[datetime]
    source_name: str = None
    image_url: str = None
    logo_url: str = None
    cluster_num: Optional[int] = None
    category: Optional[str] = None

    class Config:
        orm_mode = True


class StatisticsModels(BaseModel):
    type: str
    stats: List[Tuple[str, int]]


class ListNews(BaseModel):
    news_list: List[News]
    statistics: List[StatisticsModels]


class Cluster(BaseModel):
    cluster_id: int
    news: List[News]
    topic: List[str]
    tags: List[str]
    statistics: List[StatisticsModels]
