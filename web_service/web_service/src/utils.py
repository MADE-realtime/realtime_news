from typing import List, DefaultDict
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
import plotly.express as px

from config import PLOTLY_IMAGES_PATH


def convert_str_to_date(str_date) -> date:
    if isinstance(str_date, date):
        return str_date
    if isinstance(str_date, datetime):
        return str_date.date()
    return datetime.strptime(str_date, '%Y-%m-%d').date()


def list_tuples_to_lists(list_tuples) -> (List, List):
    xs, ys = [x for x, y in list_tuples], [y for x, y in list_tuples]
    return xs, ys


def get_vs_plots_data(stats) -> DefaultDict:
    plots = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    plots['word_1']['by_source']['x'],  plots['word_1']['by_source']['y'] = list_tuples_to_lists(stats[0].statistics[1].stats)
    plots['word_2']['by_source']['x'],  plots['word_2']['by_source']['y'] = list_tuples_to_lists(stats[1].statistics[1].stats)
    plots['word_1']['by_day']['x'],  plots['word_1']['by_day']['y'] = list_tuples_to_lists(stats[0].statistics[2].stats)
    plots['word_2']['by_day']['x'],  plots['word_2']['by_day']['y'] = list_tuples_to_lists(stats[1].statistics[2].stats)
    return plots


def draw_by_day_plot(list_tuples, file_name) -> None:
    file_path = Path.joinpath(PLOTLY_IMAGES_PATH, file_name)
    xs, ys = list_tuples_to_lists(list_tuples)
    if xs and ys:
        fig = px.line(x=xs, y=ys, labels={'x': 'Дата'})
    else:
        fig = px.line(x=[0], y=[0], labels={'x': 'Дата'})
    fig.update_xaxes(type='category')
    fig.write_image(file=file_path,
                    width=600,
                    height=300)


def get_vk_tg_stat_plot(news_stat):
    plots = defaultdict(lambda: defaultdict(list))
    plots_x = [i for i, _ in enumerate(news_stat)]
    plots['comments']['y'] = [stat.comments for stat in news_stat]
    plots['likes']['y'] = [stat.likes for stat in news_stat]
    plots['views']['y'] = [stat.views for stat in news_stat]
    plots['reposts']['y'] = [stat.reposts for stat in news_stat]
    plots['comments']['x'] = plots_x
    plots['likes']['x'] = plots_x
    plots['views']['x'] = plots_x
    plots['reposts']['x'] = plots_x
    return plots
