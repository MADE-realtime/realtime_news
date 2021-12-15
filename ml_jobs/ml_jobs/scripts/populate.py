from pathlib import Path
from db_lib.models import News
from db_lib.database import SessionLocal
from typing import List
import pandas as pd
from datetime import datetime


LENTA_MINI_DATASET_FILEPATH = Path('data/lenta-ru-news-mini.csv')

def populate_db():
    db = SessionLocal()
    source_df = pd.read_csv(LENTA_MINI_DATASET_FILEPATH, parse_dates=['date'])
    records = _convert_df_to_list_news(source_df)
    db.add_all(records)
    db.commit()


def _convert_df_to_list_news(selected_df: pd.DataFrame) -> List[News]:
    news_list = []
    for i, (_, row) in enumerate(selected_df.iterrows()):
        news_list.append(_convert_row_to_news(row))
    return news_list


def _convert_row_to_news(row) -> News:
    news_dict = {
        'source_url': row['url'],
        'title': row['title'],
        'content': row['text'],
        'topic': row['topic'],
        'tags': row['tags'],
        'date': row['date'],
        'time': datetime.combine(row['date'], datetime.min.time()),
    }
    return News(**news_dict)


if __name__ == '__main__':
    populate_db()