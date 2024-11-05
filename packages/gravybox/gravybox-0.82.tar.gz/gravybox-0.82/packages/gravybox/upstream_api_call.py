import asyncio
import json
import time
import traceback

from fastapi.encoders import jsonable_encoder
from httpx import ReadTimeout
from pydantic import BaseModel

from gravybox.betterstack import collect_logger
from gravybox.exceptions import GravyboxException, DataUnavailable
from gravybox.protocol import LinkRequest, Condition

logger = collect_logger()


def upstream_api_call(upstream_provider):
    """
    wrapper for all upstream api calls
    handles errors, task cancellations, metrics, and logging
    returns the result of the wrapped function, or a Condition if the wrapped function raises an exception
    """

    def decorator(function):
        async def wrapper(*args, link_request: LinkRequest = None, **kwargs):
            if link_request is None:
                raise ValueError("please pass the original link request when making a call to an upstream api")
            call_args = [arg for arg in args]
            call_kwargs = [f"{key}={value}" for key, value in kwargs.items()]
            log_extras = {
                "upstream_provider": upstream_provider,
                "upstream_call_type": function.__name__,
                "upstream_call_arguments": jsonable_encoder(call_args + call_kwargs),
                "trace_id": link_request.trace_id
            }
            logger.info("( ) calling upstream api", extra=log_extras)
            start_time = time.time()
            try:
                result: BaseModel = await function(*args, link_request=link_request, log_extras=log_extras, **kwargs)
                log_extras["result"] = result.model_dump_json()
                log_extras["condition"] = Condition.success.value
                return result
            except asyncio.CancelledError:
                log_extras["condition"] = Condition.cancelled.value
                raise
            except DataUnavailable:
                log_extras["condition"] = Condition.data_unavailable.value
                return Condition.data_unavailable
            except ReadTimeout:
                log_extras["condition"] = Condition.upstream_timeout.value
                return Condition.upstream_timeout
            except Exception as error:
                if isinstance(error, GravyboxException):
                    log_extras |= error.log_extras
                log_extras["error_str"] = str(error)
                log_extras["traceback"] = traceback.format_exc()
                log_extras["condition"] = Condition.unhandled_exception.value
                logger.error("(!) calling upstream api failed with unhandled exception", extra=log_extras)
                return Condition.unhandled_exception
            finally:
                log_extras["elapsed_time"] = time.time() - start_time
                logger.info("(*) completed upstream api call", extra=log_extras)

        return wrapper

    return decorator
