import pytest
import yaml
from data_collection.parser_zoo import PARSER_ZOO
from test.util import get_abs_path, fake_response_from_file, make_short_str


def prepare_expected_out(expected_out):
    for key, value in expected_out.items():
        value = [line.strip() for line in value.split('\n') if len(line.strip()) > 0]
        value = ' '.join(value)
        expected_out[key] = value
    return expected_out


def read_yaml(yaml_path):
    yaml_path = get_abs_path(yaml_path)
    with open(yaml_path, 'r') as fin:
        yaml_data = yaml.safe_load(fin)
    return yaml_data


@pytest.mark.parametrize(
    ("html_path", "yaml_path"),
    [
        ('tass_data/tass_news1.html', 'tass_data/tass_news1.yaml'),
        ('tass_data/tass_news2.html', 'tass_data/tass_news2.yaml'),
        ('tass_data/tass_news3.html', 'tass_data/tass_news3.yaml'),
    ]
)
def test_tass_parser(html_path, yaml_path):
    news_response = fake_response_from_file(html_path)
    expected_out = read_yaml(yaml_path)
    expected_out = prepare_expected_out(expected_out)
    parser = PARSER_ZOO['tass']()
    parsed_out = parser.parse(news_response)
    for key, expected_value in expected_out.items():
        assert expected_value == parsed_out[key], (f'{key} - field parsed wrong\n'
                                                   f'"{make_short_str(expected_value)}" - expected\n'
                                                   f'"{make_short_str(parsed_out[key])}" - parsed')
