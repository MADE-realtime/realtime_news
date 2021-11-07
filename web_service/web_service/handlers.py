from config import LENTA_DATASET_FILEPATH

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from news_extractor_classes import PandasNewsExtractor

app = FastAPI()
NEWS_CSV_EXTRACTOR = PandasNewsExtractor(LENTA_DATASET_FILEPATH)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


@app.get('/get_random_news/{number}')
def get_all_handler(number: int):
    """
    Get random number news from all the time
    :return:
    """
    news_list = NEWS_CSV_EXTRACTOR.show_random_news(num_random_news=number)
    return news_list.dict()
    # return templates.TemplateResponse("item.html", news_list.dict())


# @app.get('/get_date/{start_date}_{end_date}')
# def get_date_handler(start_date: str, end_date: str):
#     """
#     Get news by day
#     :param date:
#     :return:
#     """
#     news_list = NEWS_CSV_EXTRACTOR.show_news_by_days(start_date, end_date)
#     return templates.TemplateResponse("item.html", news_list.dict())
#
#
# @app.get('/get_topic/{topic}_{start_date}_{end_date}')
# def get_topic_handler(topic: str, start_date: str, end_date: str):
#     """
#     Get news by day and topic
#     :param topic:
#     :return:
#     """
#     news_list = NEWS_CSV_EXTRACTOR.show_news_by_topic(topic, start_date, end_date)
#     return templates.TemplateResponse("item.html", news_list.dict())
