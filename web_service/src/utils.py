from typing import List
from datetime import date, datetime
from pathlib import Path
import plotly.express as px

from config import PLOTLY_HTML_PATH


def convert_str_to_date(str_date) -> date:
    if isinstance(str_date, date):
        return str_date
    if isinstance(str_date, datetime):
        return str_date.date()
    return datetime.strptime(str_date, '%Y-%d-%m').date()


def list_tuples_to_lists(list_tuples) -> (List, List):
    xs, ys = [x for x, y in list_tuples], [y for x, y in list_tuples]
    return xs, ys


def draw_by_day_plot(list_tuples, file_name) -> None:
    file_path = Path.joinpath(PLOTLY_HTML_PATH, file_name)
    xs, ys = list_tuples_to_lists(list_tuples)
    fig = px.line(x=xs, y=ys)
    fig.write_html(file=file_path, include_plotlyjs="cdn", include_mathjax="cdn", full_html=False)
