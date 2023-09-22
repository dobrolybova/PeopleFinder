import pytest
from fastapi.testclient import TestClient
from pf_main import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def app_with_deps(request: pytest.FixtureRequest) -> app:
    param: dict = request.param
    for k, v in param.items():
        app.dependency_overrides[k] = v
    yield app
    app.dependency_overrides = {}
