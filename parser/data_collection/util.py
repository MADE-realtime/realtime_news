import yaml


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