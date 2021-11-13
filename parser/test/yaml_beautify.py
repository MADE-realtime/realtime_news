from argparse import ArgumentParser
import yaml
from string import punctuation


def remove_empty_lines(text):
    new_text = [line for line in text.split('\n') if len(line) > 0]
    new_text = ' '.join(new_text)
    return new_text


def shorten_lines(text, max_len):
    left = 0
    new_text = []
    while left < len(text):
        right = min(len(text), left + max_len)
        while right < len(text) and text[right] != ' ':
            right += 1
        new_text.append(text[left:right])
        left = right
    new_text = '\n'.join(new_text)
    return new_text


if __name__ == '__main__':
    parser = ArgumentParser(
        'yaml_beautify',
        'remove empty lines and shorten them in simple yaml file'
    )
    parser.add_argument(
        '-yaml'
    )
    args = parser.parse_args()
    with open(args.yaml, 'r') as fin:
        data = yaml.safe_load(fin)

    for key, value in data.items():
        value = remove_empty_lines(value)
        data[key] = value

    with open(args.yaml, 'w') as fout:
        yaml.dump(
            data,
            fout,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )
