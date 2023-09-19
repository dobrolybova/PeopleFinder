from http import HTTPStatus
from typing import Any, Optional, Type

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class CommonExceptionFormat(BaseModel):
    user_message: Optional[Any] = Field(default="")
    error_code: Optional[Any] = Field(default="")

    class Config:
        allow_population_by_field_name = True


class ServiceError(Exception):
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR
    data_fields = [
        "userMessage",
        "errorCode",
    ]

    def __init__(self, **kwargs):
        self.userMessage = kwargs.get(
            "user_message", self.http_status.__dict__.get("_name_").replace("_", " ")
        )
        self.errorCode = kwargs.get("error_code", self.http_status.value)
        super(ServiceError, self).__init__()

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k in self.data_fields}

    def str(self):
        return f"{self.__class__.__name__} from {self.__module__}"


class InternalServerError(ServiceError):
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR


class BadGateway(ServiceError):
    http_status = HTTPStatus.BAD_GATEWAY


def service_error_exc_handler(_: Request, exc: ServiceError) -> JSONResponse:
    return JSONResponse(status_code=exc.http_status, content=exc.to_dict())


def request_validation_exc_handler(
        _: Request, exc: RequestValidationError
) -> JSONResponse:
    error_format = CommonExceptionFormat(user_message=HTTPStatus.BAD_REQUEST.name + " " + str(exc.errors()),
                                         error_code=HTTPStatus.BAD_REQUEST.value).model_dump(by_alias=True)
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content=error_format)


def exc_handler(_: Request, exc: Type[Exception]) -> JSONResponse:
    error_format = CommonExceptionFormat(
        user_message=HTTPStatus.INTERNAL_SERVER_ERROR.name + " " + exc.__class__.__name__,
        error_code=HTTPStatus.INTERNAL_SERVER_ERROR.value).model_dump(by_alias=True)
    return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=error_format)
