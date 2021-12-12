from functools import wraps
from urllib.parse import unquote
from db_lib.models import RequestInfo
from db_lib import crud


def session_log(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        db = kwargs['db']

        db_item = RequestInfo(
            url=unquote(str(request.url)),
            method=str(request.method),
            host=str(request.client.host),
            user_agent=str(request.headers['user-agent']),
        )
        crud.create_news(db, db_item)

        return await handler(*args, **kwargs)
    return wrapper
