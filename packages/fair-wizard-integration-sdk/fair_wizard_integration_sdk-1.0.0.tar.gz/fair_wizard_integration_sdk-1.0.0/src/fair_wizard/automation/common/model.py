import typing
import uuid

from pydantic import BaseModel, Field, ConfigDict


class AuthorizedUserResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: str = 'AuthorizedUserResponse'
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email: str = Field(alias='email')
    image_url: str | None = Field(alias='imageUrl')
    affiliation: str | None = Field(alias='affiliation')
    user_group_uuids: list[uuid.UUID] = Field(alias='userGroupUuids')

    def serialize(self):
        return self.model_dump(by_alias=True)


class ForbiddenResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: str = 'ForbiddenResponse'
    message: str = Field(alias='message')

    def serialize(self):
        return self.model_dump(by_alias=True)


class ErrorResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: str = 'ErrorResponse'
    message: str

    def serialize(self):
        return self.model_dump(by_alias=True)


class HandlerContext:
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: int
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: object
    client_context: object
    _dummy_remaining_time_in_millis: int = 10000

    def get_remaining_time_in_millis(self) -> int:
        return self._dummy_remaining_time_in_millis


UserLoginResponse = AuthorizedUserResponse | ForbiddenResponse | ErrorResponse
IHandler = typing.Callable[[dict, HandlerContext], dict]
