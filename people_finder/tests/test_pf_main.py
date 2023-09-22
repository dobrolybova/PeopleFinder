from http import HTTPStatus

import pytest
import sqlalchemy.exc
from fastapi.testclient import TestClient
from pf_dependencies import db_handler
from pf_schemes import PeopleResponse

ivanov = {
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "age": 30,
    "email": "ivan@mail.ru",
    "msisdn": "79028384856",
    "city": "Moscow"
}
petrov = {
    "first_name": "Petr",
    "last_name": "Petrov",
    "age": 30,
    "email": "ivan@mail.ru",
    "msisdn": "79028384856",
    "city": "Moscow"
}


class FakeEmptyDbHandler:
    async def get_records(self, first_name: str | None = None,
                          last_name: str | None = None,
                          age: int | None = None,
                          email: str | None = None,
                          msisdn: str | None = None,
                          city: str | None = None):
        return []


class FakeDbHandler:
    async def get_records(self, first_name: str | None = None,
                          last_name: str | None = None,
                          age: int | None = None,
                          email: str | None = None,
                          msisdn: str | None = None,
                          city: str | None = None):
        return [PeopleResponse(**ivanov), PeopleResponse(**petrov)]


class FakeExceptionDbHandler:
    async def get_records(self, first_name: str | None = None,
                          last_name: str | None = None,
                          age: int | None = None,
                          email: str | None = None,
                          msisdn: str | None = None,
                          city: str | None = None):
        raise sqlalchemy.exc.NoResultFound


def test_find_person_wrong_request(client):
    res = client.post("/find_person")
    assert res.json() == {'detail': 'Method Not Allowed'}
    assert res.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_find_person_wrong_method(client):
    res = client.get("/some_root")
    assert res.json() == {'detail': 'Not Found'}
    assert res.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "app_with_deps, url, expected, response_status",
    [
        (
            {db_handler: FakeEmptyDbHandler},
            "/find_person",
            {'persons': []},
            HTTPStatus.OK
        ),
        (
            {db_handler: FakeDbHandler},
            "/find_person",
            {'persons': [ivanov, petrov]},
            HTTPStatus.OK
        ),
        (
            {db_handler: FakeEmptyDbHandler},
            "/find_person?qwerty",
            {'persons': []},
            HTTPStatus.OK
        ),
        (
            {db_handler: FakeDbHandler},
            "/find_person?age=30&city=Moscow",
            {'persons': [ivanov, petrov]},
            HTTPStatus.OK
        ),
        (
            {db_handler: FakeExceptionDbHandler},
            "/find_person?age=30&city=Moscow",
            {},
            HTTPStatus.BAD_REQUEST
        ),
    ],
    indirect=["app_with_deps"],
)
def test_find_person(app_with_deps, url, expected, response_status):
    cli = TestClient(app_with_deps)
    res = cli.get(url)
    assert res.json() == expected
    assert res.status_code == response_status

