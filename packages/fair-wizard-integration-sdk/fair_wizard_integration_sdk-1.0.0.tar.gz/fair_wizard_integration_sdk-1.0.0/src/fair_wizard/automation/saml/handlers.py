from fair_wizard.automation.common import UserLoginResponse, AuthorizedUserResponse, ErrorResponse
from fair_wizard.automation.saml.helpers import get_first_name, get_last_name, get_email
from fair_wizard.automation.saml.model import SamlUserLoggedInEvent


def handle_saml_user_logged_in(saml_event: SamlUserLoggedInEvent) -> UserLoginResponse:
    """
    Default *handle* function for "SAML User Logged In" event.

    :param saml_event: incoming :py:class:`SamlUserLoggedInEvent` event
    :return: resulting :py:type:`UserLoginResponse` response
    """
    first_name = get_first_name(saml_event)
    last_name = get_last_name(saml_event)
    email = get_email(saml_event)
    if first_name is None or last_name is None or email is None:
        return ErrorResponse(
            message='Missing required attributes in SAML response',
        )
    return AuthorizedUserResponse(
        first_name=first_name,
        last_name=last_name,
        email=email,
        image_url=None,
        affiliation=None,
        user_group_uuids=[],
    )
