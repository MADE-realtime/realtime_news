from data_collection.parser_zoo import PARSER_ZOO


def test_tass_parser():
    html_page = ...
    parser = PARSER_ZOO['tass']()
    parser.parse(html_page)