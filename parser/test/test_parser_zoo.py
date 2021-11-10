import os
import yaml
import pytest

from data_collection.parser_zoo import PARSER_ZOO
from test.util import get_abs_path, fake_response_from_file, make_short_str


def prepare_expected_out(expected_out):
    for key, value in expected_out.items():
        if isinstance(value, dict):
            value = prepare_expected_out(value)
        elif isinstance(value, str):
            value = [line.strip() for line in value.split('\n') if len(line.strip()) > 0]
            value = ' '.join(value)
        expected_out[key] = value
    return expected_out


def read_yaml(yaml_path):
    yaml_path = get_abs_path(yaml_path)
    with open(yaml_path, 'r') as fin:
        yaml_data = yaml.safe_load(fin)
    return yaml_data


def get_test_data(parser, folder):
    for html_fname in os.listdir(folder):
        if html_fname.endswith('html'):
            yaml_fname = html_fname.replace('html', 'yaml')
            html_path = os.path.join(folder, html_fname)
            yaml_path = os.path.join(folder, yaml_fname)
            yield parser, html_path, yaml_path


@pytest.mark.parametrize(
    ("parser", "html_path", "yaml_path"),
    [
        *get_test_data('tass', 'tass_data'),
        *get_test_data('rbc', 'rbc_data'),
        *get_test_data('ria', 'ria_data')
    ]
)
def test_tass_parser(parser, html_path, yaml_path):
    news_response = fake_response_from_file(html_path)
    expected_out = read_yaml(yaml_path)
    expected_out = prepare_expected_out(expected_out)
    parser = PARSER_ZOO[parser]
    parsed_out = parser.parse(news_response)
    assert news_response.url == parsed_out['source_url'], (f'{news_response.url} url expected but\n'
                                                           f'{parsed_out["source_url"]} url parsed')
    for key, expected_value in expected_out.items():
        trunc = False
        parsed_value = parsed_out[key]
        if isinstance(expected_value, dict):
            trunc = expected_value.get('trunc', False)
            expected_value = expected_value['data']
        if trunc:
            parsed_value = parsed_value[:len(expected_value)]
        assert expected_value == parsed_value, (f'{key} - field parsed wrong\n'
                                                   f'"{make_short_str(expected_value)}" - expected\n'
                                                   f'"{make_short_str(parsed_value)}" - parsed')
