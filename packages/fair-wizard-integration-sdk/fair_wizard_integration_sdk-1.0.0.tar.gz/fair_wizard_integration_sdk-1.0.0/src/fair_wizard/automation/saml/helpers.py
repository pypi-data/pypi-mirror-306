from .model import SamlUserLoggedInEvent


def get_first_name(saml_event: SamlUserLoggedInEvent) -> str | None:
    """
    Extracts the first name from the SAML event.

    :param saml_event: SAML event
    :return: first name if found, None otherwise
    """
    for statement in saml_event.assertion.attribute_statement:
        if (statement.friendly_name == "givenName" or
                statement.name == "urn:oid:2.5.4.42"):
            return statement.value
    return None


def get_last_name(saml_event: SamlUserLoggedInEvent) -> str | None:
    """
    Extracts the last name from the SAML event.

    :param saml_event: SAML event
    :return: last name if found, None otherwise
    """
    for statement in saml_event.assertion.attribute_statement:
        if (statement.friendly_name == "surname" or
                statement.friendly_name == "sn" or
                statement.name == "urn:oid:2.5.4.4"):
            return statement.value
    return None


def get_email(saml_event: SamlUserLoggedInEvent) -> str | None:
    """
    Extracts the email from the SAML event.

    :param saml_event: SAML event
    :return: email if found, None otherwise
    """
    for statement in saml_event.assertion.attribute_statement:
        if (statement.friendly_name == "email" or
                statement.friendly_name == "mail" or
                statement.name == "urn:oid:0.9.2342.19200300.100.1.3" or
                statement.name == "urn:oid:1.2.840.113549.1.9.1"):
            return statement.value
    return None
