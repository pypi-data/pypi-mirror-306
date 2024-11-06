import typing

from fair_wizard.automation.common import UserLoginResponse, make_handler, \
    AuthorizedUserResponse, ForbiddenResponse, ErrorResponse
from fair_wizard.automation.openid.model import OpenIdUserLoggedInEvent


IOpenIdUserLoggedInFunction = typing.Callable[[OpenIdUserLoggedInEvent], UserLoginResponse]


def make_openid_user_logged_in_handler(func: IOpenIdUserLoggedInFunction):
    def func_wrapped(event, context):
        openid_event = OpenIdUserLoggedInEvent.model_validate(event)
        result = func(openid_event)

        if isinstance(result, AuthorizedUserResponse):
            return result
        if isinstance(result, ForbiddenResponse):
            return result
        if isinstance(result, ErrorResponse):
            return result
        raise ValueError(f"Unexpected response type: {type(result)}")
    return make_handler(func_wrapped)
