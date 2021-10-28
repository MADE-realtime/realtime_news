from datetime import date
from typing import List

from pydantic import BaseModel


class News(BaseModel):
    url: str
    title: str
    text: str
    topic: str
    tags: str
    date: date


class ListNews(BaseModel):
    news_list: List[News]
    statistics: None
