import time

from httpx import Request
from httpx._client import logger


def log_request(request: Request):
    request.start_time = time.time()


def log_response(response):
    request = response.request
    time_elapsed = time.time() - response.request.start_time
    logger.debug(
        f"Response event hook: {request.method} {request.url} - Status {response.status_code}, elapsed={time_elapsed * 1000}ms")

async def async_log_request(request: Request):
    request.start_time = time.time()


async def async_log_response(response):
    request = response.request
    time_elapsed = time.time() - response.request.start_time
    logger.debug(
        f"Response event hook: {request.method} {request.url} - Status {response.status_code}, elapsed={time_elapsed * 1000}ms")
