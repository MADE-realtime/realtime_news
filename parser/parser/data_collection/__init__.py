from data_collection.news_spider import setup_ns_parser
from data_collection.rss_spider import setup_rs_parser, setup_rs_db_parser
from data_collection.yandex_spider import setup_ys_parser
from data_collection.vk_spider import setup_vk_parser, setup_vk_db_parser
from data_collection.social_media_spider import setup_sm_parser


SPIDER_PARSERS = {
    # parser_name: (help_string, setup_parser)
    'news': ('Parse news from sitemaps', setup_ns_parser),
    'rss': ('Parse news from rss', setup_rs_parser),
    'yandex': ('Parse smi url from yandex news page', setup_ys_parser),
    'rss_db': ('Parse news from rss to db', setup_rs_db_parser),
    'vk': ('Parse news from vk', setup_vk_parser),
    'vk_db': ('Parse news from vk to db', setup_vk_db_parser),
    'social_media': ('Parse links to different social media', setup_sm_parser)
}
