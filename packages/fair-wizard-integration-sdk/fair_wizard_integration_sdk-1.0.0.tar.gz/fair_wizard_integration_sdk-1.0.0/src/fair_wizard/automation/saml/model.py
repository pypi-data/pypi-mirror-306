import datetime

from pydantic import BaseModel, Field


class SubjectConfirmation(BaseModel):
    method: str = Field(alias='subjectConfirmationMethod')
    address: str = Field(alias='subjectConfirmationAddress')
    notOnOrAfter: datetime.datetime = Field(alias='subjectConfirmationNotOnOrAfter')
    recipient: str = Field(alias='subjectConfirmationRecipient')


class NameID(BaseModel):
    qualifier: str | None = Field(alias='nameIDQualifier')
    sp_name_qualifier: str | None = Field(alias='nameIDSPNameQualifier')
    sp_provided_id: str | None = Field(alias='nameIDSPProvidedID')
    format: str | None = Field(alias='nameIDFormat')
    value: str = Field(alias='nameIDValue')


class Subject(BaseModel):
    confirmations: list[SubjectConfirmation] = Field(alias='subjectConfirmations')
    name_id: NameID = Field(alias='subjectNameID')


class AudienceRestriction(BaseModel):
    audience: list[str] = Field(alias='audienceRestrictionAudience')


class Conditions(BaseModel):
    no_before: datetime.datetime = Field(alias='conditionsNotBefore')
    not_on_or_after: datetime.datetime = Field(alias='conditionsNotOnOrAfter')
    audience_restrictions: list[AudienceRestriction] = Field(alias='conditionsAudienceRestrictions')


class AuthnStatement(BaseModel):
    instant: datetime.datetime = Field(alias='authnStatementInstant')
    session_index: str = Field(alias='authnStatementSessionIndex')
    locality: str = Field(alias='authnStatementLocality')


class AssertionAttribute(BaseModel):
    name: str = Field(alias='attributeName')
    friendly_name: str | None = Field(alias='attributeFriendlyName')
    name_format: str = Field(alias='attributeNameFormat')
    value: str = Field(alias='attributeValue')


class Assertion(BaseModel):
    id: str = Field(alias='assertionId')
    issued: datetime.datetime = Field(alias='assertionIssued')
    issuer: str = Field(alias='assertionIssuer')
    subject: Subject = Field(alias='assertionSubject')
    conditions: Conditions = Field(alias='assertionConditions')
    authn_statement: AuthnStatement = Field(alias='assertionAuthnStatement')
    attribute_statement: list[AssertionAttribute] = Field(alias='assertionAttributeStatement')


class SamlUserLoggedInEvent(BaseModel):
    assertion: Assertion = Field(alias='assertion')
