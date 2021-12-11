from argparse import ArgumentParser
import json
from datetime import datetime, timedelta, timezone

from telethon.sync import TelegramClient
from sqlalchemy.exc import IntegrityError
import time

from data_collection.util import clean_url_queries, BAD_QUERIES
from db_lib.models import SocialNetworkNews, SocialNetworkStats
from db_lib.database import SessionLocal
from db_lib import crud


def read_last_callback(client, source_path, destination_path, to_db):
    with open(source_path) as fin:
        source = json.load(fin)
    news = []
    for s in source:
        print('start: ', s['domain'])
        try:
            channel_news = read_last(client, s['tg_id'], s['domain'], to_db)
        except ValueError:
            channel_news = []
        news.extend(channel_news)
        time.sleep(1)

    with open(destination_path, 'w') as fout:
        json.dump(news, fout, ensure_ascii=False)


def split_datetime(news_datetime: datetime):
    msc_tz = timezone(timedelta(seconds=10800))
    news_datetime = datetime.fromtimestamp(news_datetime.timestamp(), tz=msc_tz)
    split = {'date': news_datetime.date(), 'time': news_datetime}
    return split


def save_to_db(item):
    item.update(**split_datetime(item['date']))
    msc_tz = timezone(timedelta(seconds=10800))
    if item['time'] > (datetime.now(tz=msc_tz) - timedelta(days=7)):
        try:
            db_item = SocialNetworkNews(**item, social_network='tg', likes=0)
            crud.create_news(SessionLocal(), db_item)
        except IntegrityError:
            pass
        db_item = SocialNetworkStats(
            post_id=item['post_id'],
            comments=item['comments'],
            likes=0,
            reposts=item['reposts'],
            views=item['views'],
            social_network='tg',
        )
        crud.create_news(SessionLocal(), db_item)


def read_last(client, chat_id, domain, to_db):
    news = []
    for msg in client.get_messages(chat_id, limit=100):
        datetime = msg.date
        text = msg.message
        if msg.media and hasattr(msg.media, 'webpage') and hasattr(msg.media.webpage, 'url'):
            url = msg.media.webpage.url
            url = clean_url_queries(url, BAD_QUERIES)
        else:
            url = None
        views = msg.views
        forwards = msg.forwards
        if msg.replies:
            replies = msg.replies.replies
        else:
            replies = 0
        news.append(
            {
                'post_id': msg.id,
                'source_name': domain,
                'date': datetime,
                'text': text,
                'link': url,
                'views': views,
                'reposts': forwards,
                'comments': replies
            }
        )
        if to_db:
            save_to_db(news[-1].copy())
            time.sleep(0.05)
        news[-1]['date'] = news[-1]['date'].isoformat()
    return news


def get_channel_id(client, source_path, destination_path):
    with open(source_path) as fin:
        source = json.load(fin)
    source = [s for s in source if s['social_media'] == 'tg']
    for s in source:
        entity = client.get_entity(s['link'])
        s['tg_id'] = entity.id
        time.sleep(1)
    with open(destination_path, 'w') as fout:
        json.dump(source, fout)


def setup_parser(parser: ArgumentParser):
    parser.add_argument(
        '-destination',
        dest='destination_path',
        help='Json path to write output',
        default='tg.json'
    )
    subparsers = parser.add_subparsers()
    get_channel_id_parser = subparsers.add_parser('get_channel_id', help='Get tg channel ids')
    get_channel_id_parser.add_argument(
        '-source',
        dest='source_path',
        help='Json path to input',
        default='source_files/social_media.json'
    )
    get_channel_id_parser.set_defaults(callback=get_channel_id)

    read_last_parser = subparsers.add_parser('get_last', help='Get last 100 msg')
    read_last_parser.add_argument(
        '-source',
        dest='source_path',
        help='Json path to input',
        default='source_files/tg_channels.json'
    )
    read_last_parser.add_argument(
        '-to_db',
        help='Write to db',
        action='store_true'
    )
    read_last_parser.set_defaults(callback=read_last_callback)
    return parser


if __name__ == '__main__':
    parser = ArgumentParser(
        'Read Telegram',
        description='Read last 100 messages'
    )
    parser = setup_parser(parser)
    cli_args = parser.parse_args()

    api_id = 12465126
    api_hash = '6f41fc346203d98715395048cff3e1eb'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    cli_args = vars(cli_args)
    callback = cli_args.pop('callback')
    callback(client, **cli_args)






    # entity = client.get_entity('https://t.me/tass_agency')
    # print(entity.stringify())  # All paratmeters
    # print(entity.id)
    # msg = client.get_messages(entity.id, limit=10)
    # print(msg[7].stringify())
