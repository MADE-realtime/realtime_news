import os


def get_abs_path(file_path):
    if not file_path[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_path)
    return file_path


def make_short_str(obj, max_length=30):
    str_obj = str(obj)
    if len(str_obj) > max_length:
        str_obj = f'{str_obj[:max_length]}...'
    return str_obj