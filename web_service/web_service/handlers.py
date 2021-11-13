from config import LENTA_MINI_DATASET_FILEPATH, TEMPLATE_NAME
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from news_extractor_classes import PandasNewsExtractor

app = FastAPI()
NEWS_CSV_EXTRACTOR = PandasNewsExtractor(LENTA_MINI_DATASET_FILEPATH)

app.mount(
    "/static", StaticFiles(directory="web_service/web_service/static"), name="static"
)
templates = Jinja2Templates(directory="web_service/web_service/templates")


@app.get('/', response_class=HTMLResponse)
def get_random_handler(request: Request):
    """
    Generate initial page with random news
    # TODO: generate good news in first page
    :param request:
    :return:
    """
    news_list = NEWS_CSV_EXTRACTOR.show_random_news(num_random_news=10)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list.dict()['news_list']}
    )


@app.get('/get_random_news/', response_class=HTMLResponse)
def get_all_handler(request: Request, number: int):
    """
    Get random number news from all the time
    :return:
    """
    news_list = NEWS_CSV_EXTRACTOR.show_random_news(num_random_news=number)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list.dict()['news_list']}
    )


@app.get('/get_date/', response_class=HTMLResponse)
def get_date_handler(request: Request, start_date: str, end_date: str):
    """
    Get news by day
    :param date:
    :return:
    """
    news_list = NEWS_CSV_EXTRACTOR.show_news_by_days(start_date, end_date)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list.dict()}
    )


@app.get('/get_topic/', response_class=HTMLResponse)
def get_topic_handler(request: Request, topic: str, start_date: str, end_date: str):
    """
    Get news by day and topic
    :param topic:
    :return:
    """
    news_list = NEWS_CSV_EXTRACTOR.show_news_by_topic(topic, start_date, end_date)
    return templates.TemplateResponse(
        TEMPLATE_NAME, {"request": request, 'news': news_list.dict()}
    )
