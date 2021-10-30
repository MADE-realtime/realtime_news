from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess

from data_collection.newsspider import NewsSpider


def init_arg_parser():
    parser = ArgumentParser(
        'ParseNews',
        description=('Get news data from provided '
                     'sources and store them')
    )
    parser.add_argument(
        '-urls_file',
        help='provide source file with sitemap urls to search news in',
        required=True,
    )
    parser.add_argument(
        '-rules_file',
        help='provide rules file with domain-parser mapping',
        required=True,
    )
    parser.add_argument(
        '-destination',
        help='provide path to store news data',
        required=True,
    )
    return parser


def read_file(fpath):
    with open(fpath, 'r') as fin:
        fdata = fin.read()
    return fdata


def read_urls_file(url_fpath):
    raw_data = read_file(url_fpath)
    urls = [line.strip() for line in raw_data.split('\n')]
    return urls


def read_rule_file(rules_fpath):
    raw_data = read_file(rules_fpath)
    rules = [line.strip().split() for line in raw_data.split('\n')]
    return rules


if __name__ == '__main__':
    arg_parser = init_arg_parser()
    news_args = arg_parser.parse_args()

    sitemap_urls = read_urls_file(news_args.urls_file)
    domain_rules = read_rule_file(news_args.rules_file)

    crawl_proc = CrawlerProcess(settings={
        'DOWNLOAD_DELAY': 3,
        "FEEDS": {
            news_args.destination: {"format": "json"},
        },
        "FEED_EXPORT_ENCODING": 'utf-8',
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
    })
    crawl_proc.crawl(NewsSpider, sitemap_urls, domain_rules)
    crawl_proc.start()