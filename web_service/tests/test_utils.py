from datetime import datetime

import pytest

from ..web_service.utils import convert_str_to_date


@pytest.mark.parametrize(
    'test_input,expected'[
        ('1991-12-05', datetime.date(1991, 12, 5)),
        ('2021-02-12', datetime.date(2021, 2, 12)),
        ('2000-01-01', datetime.date(2000, 1, 1)),
    ]
)
def test_convert_str_to_date(test_input, expected):
    converted_str = convert_str_to_date(test_input)
    assert converted_str == expected
