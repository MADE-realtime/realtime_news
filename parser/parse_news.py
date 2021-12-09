from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess

from data_collection import SPIDER_PARSERS


def init_arg_parser():
    parser = ArgumentParser(
        'ParseNews',
        description=('Get news data from provided '
                     'sources and store them')
    )
    parser.add_argument(
        '-destination',
        help='Path to store news data',
        required=True,
    )
    subparsers = parser.add_subparsers()
    for parser_name, (help_str, setup_parser) in SPIDER_PARSERS.items():
        spider_parser = subparsers.add_parser(parser_name, help=help_str)
        spider_parser = setup_parser(spider_parser)
        spider_parser.add_argument(
            '-logfile',
            help='Path to write logs',
            default=f'{parser_name}.log'
        )
    return parser


if __name__ == '__main__':
    arg_parser = init_arg_parser()
    cli_args = arg_parser.parse_args()
    cli_args = vars(cli_args)

    crawl_proc = CrawlerProcess(settings={
        'DOWNLOAD_DELAY': 3,
        "FEEDS": {
            cli_args.pop('destination'): {"format": "json"},
        },
        'LOG_FILE': f'{cli_args.pop("logfile")}',
        "FEED_EXPORT_ENCODING": 'utf-8',
        # TODO: pip install scrapy-user-agents
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        },
        'EXTENSIONS': {
            'scrapy.extensions.corestats.CoreStats': 0,
            'scrapy.extensions.memusage.MemoryUsage': 0,
            'scrapy.extensions.logstats.LogStats': 0,
        }
    })

    spider_class = cli_args.pop('spider')
    setup_kwargs = cli_args.pop('setup_kwargs')
    spider_kwargs = setup_kwargs(**cli_args)
    crawl_proc.crawl(spider_class, **spider_kwargs)
    crawl_proc.start()
