from datetime import date, datetime


def convert_str_to_date(str_date) -> date:
    if isinstance(str_date, date) or isinstance(str_date, datetime):
        return str_date.date()
    return datetime.strptime(str_date, '%Y-%d-%m').date()
