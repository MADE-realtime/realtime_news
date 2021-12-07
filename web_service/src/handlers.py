from typing import List, Optional

from config import FAVICON_PATH, TEMPLATE_NAME, SEARCH_TEMPLATE_NAME
from datetime import datetime
from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import ListNews, News
from news_extractor import BaseNewsExtractor, DBNewsExtractor
from sqlalchemy.orm import Session

from db_lib.database import SessionLocal

app = FastAPI()
# NEWS_EXTRACTOR = PandasNewsExtractor(LENTA_MINI_DATASET_FILEPATH)
NEWS_EXTRACTOR: BaseNewsExtractor = DBNewsExtractor()

app.mount("/static", StaticFiles(directory="web_service/src/static"), name="static")
templates = Jinja2Templates(directory="web_service/src/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    '/',
    response_class=HTMLResponse,
    response_model=ListNews,
)
async def main_handler(request: Request,
                       topic: Optional[str] = None,
                       start_date: Optional[str] = '1991-05-12',
                       end_date: Optional[str] = None,
                       number: Optional[int] = 10,
                       db: Session = Depends(get_db)
                       ):
    """
    Get random number news by filters
    :return:
    """
    if not end_date:
        end_date = datetime.date(datetime.now())
    news_list = NEWS_EXTRACTOR.show_news_by_filters(db, topic, end_date, start_date, number)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list.news_list, 'stats': news_list.statistics}
    )


@app.get(
    '/search',
    response_class=HTMLResponse,
    response_model=ListNews,
)
async def main_handler(request: Request,
                       word_1: str,
                       word_2: str,
                       db: Session = Depends(get_db)
                       ):
    """
    Get statistics of some word in news
    :return:
    """
    news_infos = []
    for word in (word_1, word_2):
        news_infos.append(NEWS_EXTRACTOR.show_news_by_regex(db, word))
    return templates.TemplateResponse(
        SEARCH_TEMPLATE_NAME, {"request": request, 'news': news_infos[0].news_list, 'stats': news_infos[0].statistics}
    )
    # TODO: Роберт, нужно тут добавить возвращение статистик по обоим словам

@app.get(
    '/get_random_news/{num_random_news}',
    response_class=HTMLResponse,
    response_model=ListNews,
)
def get_all_handler(
    request: Request, num_random_news: int, db: Session = Depends(get_db)
):
    """
    Get random number news from all the time
    :return:
    """
    news_list = NEWS_EXTRACTOR.show_random_news(db, num_random_news)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list.news_list, 'stats': news_list.statistics}
    )


@app.get(
    '/get_date/{start_date}/{end_date}',
    response_class=HTMLResponse,
    response_model=ListNews,
)
def get_date_handler(
    request: Request, start_date: str, end_date: str, db: Session = Depends(get_db)
):
    """
    Get news by day
    :param date:
    :return:
    """
    news_list = NEWS_EXTRACTOR.show_news_by_days(db, start_date, end_date)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list.news_list, 'stats': news_list.statistics}
    )


@app.get(
    '/get_topic/{topic}/{start_date}/{end_date}',
    response_class=HTMLResponse,
    response_model=ListNews,
)
def get_topic_handler(
    request: Request,
    topic: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
):
    """
    Get news by day and topic
    :param topic:
    :return:
    """
    news_list = NEWS_EXTRACTOR.show_news_by_topic(db, topic, start_date, end_date)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list.news_list, 'stats': news_list.statistics}
    )


@app.get('/favicon.ico', response_class=FileResponse, include_in_schema=False)
async def favicon():
    return FAVICON_PATH
