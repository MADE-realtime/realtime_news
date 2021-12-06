from argparse import ArgumentParser
import json

from telethon.sync import TelegramClient
import time

from data_collection.util import clean_url_queries, BAD_QUERIES


def read_last_callback(client, source_path, destination_path):
    with open(source_path) as fin:
        source = json.load(fin)
    news = []
    for s in source:
        print('start: ', s['domain'])
        try:
            channel_news = read_last(client, s['tg_id'], s['domain'])
        except ValueError:
            channel_news = []
        news.extend(channel_news)
        time.sleep(0.5)

    with open(destination_path, 'w') as fout:
        json.dump(news, fout, ensure_ascii=False)


def read_last(client, chat_id, domain):
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
                'source_name': domain,
                'datetime': datetime.isoformat(),
                'text': text,
                'url': url,
                'views': views,
                'forwards': forwards,
                'replies': replies
            }
        )
    return news


def get_channel_id(client, source_path, destination_path):
    with open(source_path) as fin:
        source = json.load(fin)
    source = [s for s in source if s['social_media'] == 'tg']
    for s in source:
        entity = client.get_entity(s['link'])
        s['tg_id'] = entity.id
    with open(destination_path, 'w') as fout:
        json.dump(source, fout)


def setup_parser(parser: ArgumentParser):
    parser.add_argument(
        '-to_db',
        help='Write to db',
        action='store_true'
    )
    parser.add_argument(
        '-destination',
        help='Json path to write output',
        default='tg.json'
    )
    parser.add_argument(
        '-source',
        help='Json path to input',
        default='source_files/social_media.json'
    )
    subparsers = parser.add_subparsers()
    get_channel_id_parser = subparsers.add_parser('get_channel_id', help='Get tg channel ids')
    get_channel_id_parser.set_defaults(callback=get_channel_id)

    read_last_parser = subparsers.add_parser('get_last', help='Get last 100 msg')
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

    cli_args.callback(client, cli_args.source, cli_args.destination)






    # entity = client.get_entity('https://t.me/tass_agency')
    # print(entity.stringify())  # All paratmeters
    # print(entity.id)
    # msg = client.get_messages(entity.id, limit=10)
    # print(msg[7].stringify())
