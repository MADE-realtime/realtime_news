import os
from scrapy.http import HtmlResponse, Request


def fake_response_from_file(file_path, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_path: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)
    file_path = get_abs_path(file_path)

    file_content = open(file_path, 'rb').read()

    response = HtmlResponse(url=url,
        request=request,
        body=file_content)
    return response


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