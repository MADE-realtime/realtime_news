from config import TEMPLATE_NAME
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from news_extractor import DBNewsExtractor, BaseNewsExtractor
from db_lib.database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from models import News
from typing import List

app = FastAPI()
# NEWS_EXTRACTOR = PandasNewsExtractor(LENTA_MINI_DATASET_FILEPATH)
NEWS_EXTRACTOR: BaseNewsExtractor = DBNewsExtractor()

app.mount(
    "/static", StaticFiles(directory="web_service/src/static"), name="static"
)
templates = Jinja2Templates(directory="web_service/src/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/get_random_news/{num_random_news}', response_class=HTMLResponse, response_model=List[News])
def get_all_handler(request: Request, num_random_news: int, db: Session = Depends(get_db)):
    """
    Get random number news from all the time
    :return:
    """
    news_list = NEWS_EXTRACTOR.show_random_news(db, num_random_news)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list['news_list']}
    )


@app.get('/get_date/{start_date}/{end_date}', response_class=HTMLResponse, response_model=List[News])
def get_date_handler(request: Request, start_date: str, end_date: str, db: Session = Depends(get_db)):
    """
    Get news by day
    :param date:
    :return:
    """
    news_list = NEWS_EXTRACTOR.show_news_by_days(db, start_date, end_date)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list['news_list']}
    )


@app.get('/get_topic/{topic}/{start_date}/{end_date}', response_class=HTMLResponse, response_model=List[News])
def get_topic_handler(request: Request, topic: str, start_date: str, end_date: str, db: Session = Depends(get_db)):
    """
    Get news by day and topic
    :param topic:
    :return:
    """
    news_list = NEWS_EXTRACTOR.show_news_by_topic(db, topic, start_date, end_date)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list['news_list']}
    )