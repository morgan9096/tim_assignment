from functools import wraps
from typing import Callable

import requests

from utils.logger import log


def _try_5_times(function_: Callable) -> Callable:
    @wraps(function_)
    def wrapper(*args, **kwargs):
        for attempt in range(1, 5+1):
            response = function_(*args, **kwargs)
            if response.ok:
                return response
            log.error(f'Attempt: {attempt} failed. Try to get response for {args} again')

    return wrapper

@_try_5_times
def collect_get_response(url: str) -> requests.Response | None:
    return requests.get(url=url)


@_try_5_times
def collect_post_response(url: str, data: dict)-> requests.Response | None:
    return requests.post(url=url, data=data)
