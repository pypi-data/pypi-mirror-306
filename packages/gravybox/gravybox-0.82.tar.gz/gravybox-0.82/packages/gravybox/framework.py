import json
import time
import traceback
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from httpx import ReadTimeout
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from gravybox.betterstack import collect_logger
from gravybox.exceptions import GravyboxException, DataUnavailable, CollectionFailure
from gravybox.protocol import Condition, GravyboxResponse
from gravybox.requests import AsyncRequestManager

logger = collect_logger()


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    logger.info("( ) starting FastAPI server")
    AsyncRequestManager.initialize()
    try:
        yield
    finally:
        await AsyncRequestManager.shutdown()
    logger.info("(*) shutting down FastAPI server")


class ThresholdEndpoint(BaseHTTPMiddleware):
    def __init__(self, app, threshold_key=None):
        self.threshold_key = threshold_key
        super().__init__(app)

    async def dispatch(self, request, call_next):
        request_key = request.headers.get("x-api-key")
        if request_key == self.threshold_key:
            return await call_next(request)
        else:
            logger.warning("(!) authentication failed", extra={"client_host": request.client.host})
            return JSONResponse(
                status_code=403,
                content=GravyboxResponse(
                    success=False,
                    error=Condition.authentication_failure.value
                ).model_dump()
            )


class LoggingEndpoint(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        request.state.log_extras = {
            "endpoint": request.scope["path"]
        }
        try:
            payload = await request.json()
            request.state.log_extras["request_json"] = json.dumps(payload)
            request.state.trace_id = payload.get("trace_id", str(uuid.uuid4()))
            request.state.log_extras["trace_id"] = request.state.trace_id
        except Exception as error:
            request.state.log_extras["error_str"] = str(error)
            request.state.log_extras["condition"] = Condition.invalid_request.value
            logger.error("(!) failed to parse request", extra=request.state.log_extras)
            return JSONResponse(
                status_code=400,
                content=GravyboxResponse(
                    success=False,
                    error=request.state.log_extras["condition"]
                ).model_dump()
            )
        logger.info("( ) endpoint receiving request", extra=request.state.log_extras)
        start_time = time.time()
        try:
            response = await call_next(request)
            if "condition" not in request.state.log_extras:
                request.state.log_extras["condition"] = Condition.success.value
        except Exception as error:
            if isinstance(error, GravyboxException):
                request.state.log_extras |= error.log_extras
            request.state.log_extras["error_str"] = str(error)
            request.state.log_extras["traceback"] = traceback.format_exc()
            request.state.log_extras["condition"] = Condition.unhandled_exception.value
            logger.error("(!) endpoint failed with unhandled exception", extra=request.state.log_extras)
            response = JSONResponse(
                status_code=500,
                content=GravyboxResponse(success=False, error=request.state.log_extras["condition"]).model_dump()
            )
        finally:
            request.state.log_extras["status_code"] = response.status_code
            request.state.log_extras["elapsed_time"] = time.time() - start_time
            logger.info("(*) endpoint emitting response", extra=request.state.log_extras)
            return response


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(LoggingEndpoint)

    @app.exception_handler(ReadTimeout)
    async def upstream_timeout_handler(request: Request, error: ReadTimeout):
        request.state.log_extras["condition"] = Condition.upstream_timeout.value
        return JSONResponse(
            status_code=500,
            content=GravyboxResponse(success=False, error=request.state.log_extras["condition"]).model_dump()
        )

    @app.exception_handler(DataUnavailable)
    async def data_unavailable_handler(request: Request, error: DataUnavailable):
        request.state.log_extras["condition"] = Condition.data_unavailable.value
        return JSONResponse(
            status_code=200,
            content=GravyboxResponse(success=False, error=request.state.log_extras["condition"]).model_dump()
        )

    @app.exception_handler(CollectionFailure)
    async def collection_failure_handler(request: Request, error: CollectionFailure):
        request.state.log_extras["condition"] = Condition.collection_failure.value
        return JSONResponse(
            status_code=500,
            content=GravyboxResponse(success=False, error=request.state.log_extras["condition"]).model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, error: RequestValidationError):
        request.state.log_extras["condition"] = Condition.invalid_request.value
        return JSONResponse(
            status_code=422,
            content=GravyboxResponse(success=False, error=request.state.log_extras["condition"]).model_dump()
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, error: HTTPException):
        request.state.log_extras["condition"] = error.detail
        return JSONResponse(
            status_code=error.status_code,
            content=GravyboxResponse(success=False, error=request.state.log_extras["condition"]).model_dump()
        )

    return app
