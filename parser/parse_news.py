from argparse import ArgumentParser


def callback(news_args):
    source_list = read_source_file(news_args.source_file)
    agg_data = process_source_list(source_list)
    store_data(agg_data, news_args.destination)


def init_arg_parser():
    parser = ArgumentParser(
        'ParseNews',
        description=('Get news data from provided '
                     'sources and store them')
    )
    parser.add_argument(
        '-source_file',
        help='provide source file with urls to search news in',
        required=True,
    )
    parser.add_argument(
        '-destination',
        help='provide path to store news data',
        required=True,
    )
    return parser


def read_source_file(source_file):
    return []


def get_data_from(source):
    pass


def process_source_list(source_list):
    agg_data = [get_data_from(source) for source in source_list]
    return []


def store_data(data, destination):
    pass


if __name__ == '__main__':
    arg_parser = init_arg_parser()
    args = arg_parser.parse_args()
    args.callback(args)
