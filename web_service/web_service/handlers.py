from config import LENTA_DATASET_FILEPATH
from fastapi import FastAPI
from news_extractor_classes import PandasNewsExtractor

app = FastAPI()
NEWS_CSV_EXTRACTOR = PandasNewsExtractor(LENTA_DATASET_FILEPATH)


@app.get('/get_random_news/{number}')
def get_all_handler(number: int):
    """
    Get random number news from all the time
    :return:
    """
    news_list = NEWS_CSV_EXTRACTOR.show_random_news(num_random_news=number)
    return news_list


@app.get('/get_date/{date}')
def get_date_handler(date: str):
    """
    Get news by day
    :param date:
    :return:
    """
    news_list = NEWS_CSV_EXTRACTOR.show_news_by_day(date)
    return news_list


@app.get('/get_topic/{topic}_{date}')
def get_topic_handler(topic: str):
    """
    Get news by day and topic
    :param topic:
    :return:
    """
    news_list = NEWS_CSV_EXTRACTOR.show_news_by_topic(topic=topic)
    return news_list
