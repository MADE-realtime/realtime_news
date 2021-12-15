from pathlib import Path

LANGUAGE = 'russian'
LENTA_DATASET_FILEPATH = Path('data/lenta-ru-news.csv')
LENTA_MINI_DATASET_FILEPATH = Path('data/lenta-ru-news-mini.csv')
DEFAULT_NEWS_IMAGE_URL = 'https://topspb.tv/media/768x432/programs_covers/novosti.png'
DEFAULT_LOGO_URL = 'https://image.flaticon.com/icons/png/512/21/21601.png'
MIN_NGRAM_FREQ = 2
LIMIT_NEWS = 10_000
TEMPLATE_NAME = 'index.html'
SEARCH_TEMPLATE_NAME = 'search.html'
FAVICON_PATH = Path('web_service/src/static/img/favicon.ico')
PLOTLY_HTML_PATH = Path('web_service/src/templates/plotly')
PLOTLY_IMAGES_PATH = Path('web_service/src/static/plotly')
