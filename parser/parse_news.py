from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess

from data_collection.news_spider import NewsSpider
from data_collection.rss_spider import SpiderRSS


def init_arg_parser():
    parser = ArgumentParser(
        'ParseNews',
        description=('Get news data from provided '
                     'sources and store them')
    )
    parser.add_argument(
        '-spider_class',
        help='choose Spider',
        required=True
    )
    parser.add_argument(
        '-destination',
        help='provide path to store news data',
        required=True,
    )
    return parser


def prepare_kwargs(raw_kwargs):
    kwargs = dict()
    key = None
    for element in raw_kwargs:
        if element.startswith('-'):
            key = element.replace('-', '')
        elif key is not None:
            kwargs[key] = element
    return kwargs


if __name__ == '__main__':
    arg_parser = init_arg_parser()
    cli_args, raw_spider_kwargs = arg_parser.parse_known_args()

    # TODO: replace prepare_kwargs with spider_parser
    spider_kwargs = prepare_kwargs(raw_spider_kwargs)
    spider_class = locals()[cli_args.spider_class]

    crawl_proc = CrawlerProcess(settings={
        'DOWNLOAD_DELAY': 3,
        "FEEDS": {
            cli_args.destination: {"format": "json"},
        },
        'LOG_FILE': f'{cli_args.spider_class}.log',
        "FEED_EXPORT_ENCODING": 'utf-8',
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
        'EXTENSIONS': {
            'scrapy.extensions.corestats.CoreStats': 0,
            'scrapy.extensions.memusage.MemoryUsage': 0,
            'scrapy.extensions.logstats.LogStats': 0,
        }
    })
    crawl_proc.crawl(spider_class, **spider_kwargs)
    crawl_proc.start()
