import re
import urllib.parse

import yaml
from bs4 import BeautifulSoup


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


def read_yaml_file(yaml_fpath):
    with open(yaml_fpath, 'r') as fin:
        yaml_data = yaml.safe_load(fin)
    return yaml_data


def regex(x):
    if isinstance(x, str):
        return re.compile(x)
    return x


def get_domain(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc


def extract_all_tags(xml_tag):
    soup = BeautifulSoup(xml_tag, 'xml')
    return [t.name for t in soup.descendants if t.name]