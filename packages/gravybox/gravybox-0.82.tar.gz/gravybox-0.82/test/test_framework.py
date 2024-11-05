import httpx
import pytest
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.testclient import TestClient

from gravybox.exceptions import DataUnavailable
from gravybox.framework import create_app, ThresholdEndpoint
from gravybox.protocol import LinkRequest, LinkResponse, Condition

app = create_app()
threshold_key = "supersecret"
valid_headers = {"x-api-key": threshold_key}

app.add_middleware(ThresholdEndpoint, threshold_key=threshold_key)


class TestModel(BaseModel):
    value_one_plus_one: int
    opposite_of_value_two: bool


class TestRequest(LinkRequest):
    value_one: int
    value_two: bool


class TestResponse(LinkResponse):
    content: TestModel | None


@app.post("/success")
async def success_endpoint(link_request: TestRequest) -> TestResponse:
    result = TestModel(
        value_one_plus_one=link_request.value_one + 1,
        opposite_of_value_two=not link_request.value_two
    )
    return TestResponse(success=True, content=result)


@app.post("/failure")
async def failing_endpoint(link_request: TestRequest) -> TestResponse:
    raise RuntimeError("failing endpoint failed as expected")


@app.post("/data_unavailable")
async def data_unavailable_endpoint(link_request: TestRequest) -> TestResponse:
    raise DataUnavailable()


@app.post("/timeout")
async def timeout_endpoint(link_request: TestRequest) -> TestResponse:
    raise httpx.ReadTimeout("timeout endpoint timed out")


@app.post("/http_exception")
async def http_exception_endpoint(link_request: TestRequest) -> TestResponse:
    raise HTTPException(status_code=404, detail="not found")


@pytest.mark.asyncio
async def test_no_api_key():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="success", value_one=3, value_two=False)
        response = client.post("/success", json=jsonable_encoder(test_request))
        assert response.status_code == 403
        response_model = TestResponse.model_validate(response.json())
        assert response_model.success is False
        assert response_model.error == Condition.authentication_failure.value


@pytest.mark.asyncio
async def test_invalid_api_key():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="success", value_one=3, value_two=False)
        response = client.post("/success", json=jsonable_encoder(test_request), headers={"x-api-key": "nonsense"})
        assert response.status_code == 403
        response_model = TestResponse.model_validate(response.json())
        assert response_model.success is False
        assert response_model.error == Condition.authentication_failure.value


@pytest.mark.asyncio
async def test_framework_no_payload():
    with TestClient(app) as client:
        response = client.post("/success", headers=valid_headers)
        assert response.status_code == 400
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == Condition.invalid_request.value
        assert test_response.content is None


@pytest.mark.asyncio
async def test_framework_no_trace_id_on_link_request():
    with TestClient(app) as client:
        test_request = {
            "value_one": 3,
            "value_two": False
        }
        response = client.post("/success", json=test_request, headers=valid_headers)
        assert response.status_code == 422
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == Condition.invalid_request.value
        assert test_response.content is None


@pytest.mark.asyncio
async def test_framework_malformed_payload():
    with TestClient(app) as client:
        test_request = {
            "trace_id": "malformed_payload",
            "value_one": 3
        }
        response = client.post("/success", json=test_request, headers=valid_headers)
        assert response.status_code == 422
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == Condition.invalid_request.value
        assert test_response.content is None


@pytest.mark.asyncio
async def test_framework_success():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="success", value_one=3, value_two=False)
        response = client.post("/success", json=jsonable_encoder(test_request), headers=valid_headers)
        assert response.status_code == 200
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is True
        assert test_response.error == ""
        assert test_response.content.value_one_plus_one == 4
        assert test_response.content.opposite_of_value_two is True


@pytest.mark.asyncio
async def test_framework_data_unavailable():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="data unavailable", value_one=3, value_two=False)
        response = client.post("/data_unavailable", json=jsonable_encoder(test_request), headers=valid_headers)
        assert response.status_code == 200
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == Condition.data_unavailable.value
        assert test_response.content is None


@pytest.mark.asyncio
async def test_framework_timeout():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="timeout", value_one=3, value_two=False)
        response = client.post("/timeout", json=jsonable_encoder(test_request), headers=valid_headers)
        assert response.status_code == 500
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == Condition.upstream_timeout.value
        assert test_response.content is None


@pytest.mark.asyncio
async def test_framework_failure():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="failure", value_one=3, value_two=False)
        response = client.post("/failure", json=jsonable_encoder(test_request), headers=valid_headers)
        assert response.status_code == 500
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == Condition.unhandled_exception.value
        assert test_response.content is None


@pytest.mark.asyncio
async def test_framework_http_error():
    with TestClient(app) as client:
        test_request = TestRequest(trace_id="failure", value_one=3, value_two=False)
        response = client.post("/http_exception", json=jsonable_encoder(test_request), headers=valid_headers)
        assert response.status_code == 404
        test_response = TestResponse.model_validate(response.json())
        assert test_response.success is False
        assert test_response.error == "not found"
        assert test_response.content is None
