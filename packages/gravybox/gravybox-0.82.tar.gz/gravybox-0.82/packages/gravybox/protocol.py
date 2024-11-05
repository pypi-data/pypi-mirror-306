from enum import Enum

from pydantic import BaseModel


class UpstreamCallParadigms(Enum):
    sequential = "sequential"
    simultaneous = "simultaneous"
    short_circuit = "short_circuit"


class Condition(Enum):
    success = "success"
    data_unavailable = "data unavailable"
    upstream_timeout = "upstream request timed out"
    unhandled_exception = "unhandled exception"
    invalid_request = "invalid request"
    cancelled = "cancelled"
    authentication_failure = "authentication failure"
    collection_failure = "collection failure"


class GravyboxRequest(BaseModel):
    pass


class GravyboxResponse(BaseModel):
    success: bool
    error: str = ""
    content: dict | None = None


class LinkRequest(GravyboxRequest):
    trace_id: str
    upstream_call_paradigm: UpstreamCallParadigms = UpstreamCallParadigms.short_circuit


class LinkResponse(GravyboxResponse):
    pass
