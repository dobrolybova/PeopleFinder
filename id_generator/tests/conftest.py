import json

import asynctest
import pytest
from fastapi.testclient import TestClient

from main import app


application_json = "application/json"
application_octet_stream = "application/octet-stream"


@pytest.fixture()
def srv():
    return app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="function")
def mock_response():
    def prepare_response(status=200, json_body=None, content_type=application_json):
        fake_response = asynctest.CoroutineMock()
        if not json_body:
            json_body = {}

        fake_response.return_value.bool = True
        fake_response.json = asynctest.CoroutineMock(return_value=json_body)
        fake_response.text = asynctest.CoroutineMock(return_value=json.dumps(json_body))
        fake_response.status = status
        fake_response.content_type = content_type
        return fake_response

    return prepare_response


@pytest.fixture
def app_with_deps(request: pytest.FixtureRequest) -> app:
    param: dict = request.param
    for k, v in param.items():
        app.dependency_overrides[k] = v
    yield app
    app.dependency_overrides = {}
