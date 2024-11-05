import asyncio

from httpx import ReadTimeout
from pydantic import BaseModel

from gravybox.exceptions import DataUnavailable
from gravybox.protocol import LinkRequest
from gravybox.upstream_api_call import upstream_api_call, logger


class TestTaskResult(BaseModel):
    field_one: str | None = None
    field_two: int | None = None
    field_three: bool | None = None


@upstream_api_call("testkit")
async def sleeping_coroutine(sleep_time: int,
                             field_one: str,
                             field_two: int,
                             field_three: bool = False,
                             link_request: LinkRequest = None,
                             log_extras: dict = None):
    logger.info("sleeping coroutine started sleeping", extra=log_extras)
    await asyncio.sleep(sleep_time)
    logger.info("sleeping coroutine finished sleeping", extra=log_extras)
    result = TestTaskResult(field_one=field_one, field_two=field_two, field_three=field_three)
    return result


@upstream_api_call("testkit")
async def failing_coroutine(sleep_time: int,
                            field_one: str,
                            field_two: int,
                            field_three: bool = False,
                            link_request: LinkRequest = None,
                            log_extras: dict = None):
    logger.info("failing coroutine started sleeping", extra=log_extras)
    await asyncio.sleep(sleep_time)
    logger.info("failing coroutine finished sleeping", extra=log_extras)
    raise RuntimeError("failing task failed as expected")


@upstream_api_call("testkit")
async def data_unavailable_coroutine(sleep_time: int,
                                     field_one: str,
                                     field_two: int,
                                     field_three: bool = False,
                                     link_request: LinkRequest = None,
                                     log_extras: dict = None):
    logger.info("data unavailable coroutine started sleeping", extra=log_extras)
    await asyncio.sleep(sleep_time)
    logger.info("data unavailable coroutine finished sleeping", extra=log_extras)
    raise DataUnavailable()


@upstream_api_call("testkit")
async def upstream_timeout_coroutine(sleep_time: int,
                                     field_one: str,
                                     field_two: int,
                                     field_three: bool = False,
                                     link_request: LinkRequest = None,
                                     log_extras: dict = None):
    logger.info("upstream timeout coroutine started sleeping", extra=log_extras)
    await asyncio.sleep(sleep_time)
    logger.info("upstream timeout coroutine finished sleeping", extra=log_extras)
    raise ReadTimeout("upstream timeout coroutine timed out")
