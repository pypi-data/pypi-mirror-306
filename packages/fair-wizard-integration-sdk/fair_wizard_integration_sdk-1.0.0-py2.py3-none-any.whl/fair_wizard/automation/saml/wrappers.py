import typing

from ..common import UserLoginResponse, make_handler
from .model import SamlUserLoggedInEvent


ISAMLUserLoggedInFunction = typing.Callable[[SamlUserLoggedInEvent], UserLoginResponse]


def make_saml_user_logged_in_handler(func: ISAMLUserLoggedInFunction):
    def func_wrapped(event, context):
        saml_event = SamlUserLoggedInEvent.model_validate(event)
        return func(saml_event)
    return make_handler(func_wrapped)
