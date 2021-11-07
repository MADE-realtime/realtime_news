from datetime import date, datetime


def convert_str_to_date(str_date: str) -> date:
    return datetime.strptime(str_date, '%Y-%d-%m').date()
