from http import HTTPStatus

import asynctest
import pytest
from fastapi.testclient import TestClient

from client.people_finder_client import PeopleFinderClient
from exceptions import BadGateway
from schemes import Request
from tests.conftest import application_json
from dependencies import get_people_finder_client

req_body = {"first_name": "Ivan"}
person_data_ivan = {
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "age": 30,
    "email": "ivan@mail.ru",
    "msisdn": "79028384856",
    "city": "Moscow"
}
person_data_oleg = {
    "first_name": "Oleg",
    "last_name": "Petrov",
    "age": 30,
    "email": "ivan@mail.ru",
    "msisdn": "79028384856",
    "city": "Moscow"
}


class FakeClient:
    async def find_person(self, _):
        return [person_data_ivan, person_data_oleg]


class FakeClientEmpty:
    async def find_person(self, _):
        return []


class FakeClientException:
    async def find_person(self, _):
        raise BadGateway


def test_metrics(client):
    response = client.get("/prometheus")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, json_body, content_type, expected",
    [
        (
            HTTPStatus.OK,
            {"persons": [person_data_ivan, person_data_oleg]},
            application_json,
            [person_data_ivan, person_data_oleg],
        ),
        (
            HTTPStatus.OK,
            {},
            application_json,
            [],
        ),
    ],
)
async def test_client_ok(
        mock_response, status, json_body, content_type, expected
):
    fake_request_context = asynctest.MagicMock()
    fake_request_context.return_value.__aenter__ = asynctest.CoroutineMock(
        return_value=mock_response(
            status=status, json_body=json_body, content_type=content_type
        )
    )
    fake_request_context.return_value.__aexit__ = asynctest.CoroutineMock()
    with asynctest.patch(
            "client.requester.Requester.get_session",
            new=fake_request_context,
            scope=asynctest.LIMITED,
    ):
        test_class = PeopleFinderClient("http://test_url")
        result = await test_class.find_person(Request(**req_body))
        assert result == expected


# TODO: test raise for error - ClientResponseError
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, json_body, content_type, expected",
    [
        (
            HTTPStatus.OK,
            {
                "persons": [
                    {
                        "name": "Ivan",
                    }
                ]
            },
            application_json,
            BadGateway
        ),
    ],
)
async def test_client_nok(
        mock_response, status, json_body, content_type, expected
):
    fake_request_context = asynctest.MagicMock()
    fake_request_context.return_value.__aenter__ = asynctest.CoroutineMock(
        return_value=mock_response(
            status=status, json_body=json_body, content_type=content_type
        )
    )
    fake_request_context.return_value.__aexit__ = asynctest.CoroutineMock()
    with asynctest.patch(
            "client.requester.Requester.get_session",
            new=fake_request_context,
            scope=asynctest.LIMITED,
    ):
        with pytest.raises(expected):
            test_class = PeopleFinderClient("http://test_url")
            await test_class.find_person(Request(**req_body))


@pytest.mark.parametrize(
    "url, json_res, status",
    [
        ("/some_root", {'detail': 'Not Found'}, HTTPStatus.NOT_FOUND),
        ("/find",
         {'error_code': 400,
          'user_message': "BAD_REQUEST [{'type': 'missing', 'loc': ('body',), 'msg': "
                          "'Field required', 'input': None, 'url': "
                          "'https://errors.pydantic.dev/2.1/v/missing'}]"
          },
         HTTPStatus.BAD_REQUEST
         )
    ]
)
def test_find_no_body(client, url, json_res, status):
    res = client.post(url)
    assert res.json() == json_res
    assert res.status_code == status


@pytest.mark.parametrize(
    "app_with_deps, request_data, expected, response_status",
    [
        (
            {get_people_finder_client: FakeClient},
            req_body,
            {'persons': [person_data_ivan, person_data_oleg]},
            HTTPStatus.OK
        ),
        (
            {get_people_finder_client: FakeClientEmpty},
            req_body,
            {'persons': []},
            HTTPStatus.OK
        ),
        (
            {get_people_finder_client: FakeClientException},
            req_body,
            {'errorCode': 502, 'userMessage': 'BAD GATEWAY'},
            HTTPStatus.BAD_GATEWAY
        ),
        (
            {get_people_finder_client: FakeClientException},
            {"name": "name"},
            {'error_code': 400,
             'user_message': "BAD_REQUEST [{'type': 'extra_forbidden', 'loc': ('body', "
                             "'name'), 'msg': 'Extra inputs are not permitted', 'input': "
                             "'name', 'url': "
                             "'https://errors.pydantic.dev/2.1/v/extra_forbidden'}]"},
            HTTPStatus.BAD_REQUEST
        ),
    ],
    indirect=["app_with_deps"],
)
def test_find_with_body(app_with_deps, request_data, expected, response_status):
    client = TestClient(app_with_deps)
    res = client.post('/find', json=request_data)
    assert res.json() == expected
    assert res.status_code == response_status
