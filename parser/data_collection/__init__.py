from data_collection.news_spider import setup_ns_parser
from data_collection.rss_spider import setup_rs_parser
from data_collection.yandex_spider import setup_ys_parser


SPIDER_PARSERS = {
    # parser_name: (help_string, setup_parser)
    'news': ('Parse news from sitemaps', setup_ns_parser),
    'rss': ('Parse news from rss', setup_rs_parser),
    'yandex': ('Parse smi url from yandex news page', setup_ys_parser)
}