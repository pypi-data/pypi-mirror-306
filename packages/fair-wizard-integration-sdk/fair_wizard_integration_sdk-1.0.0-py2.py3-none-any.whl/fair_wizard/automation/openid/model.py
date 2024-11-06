from pydantic import BaseModel, Field


class IdToken(BaseModel):
    """
    Model for ID token of OpenID
    """
    iss: str = Field(alias='iss')
    sub: str = Field(alias='sub')
    aud: list[str] = Field(alias='aud')
    exp: int = Field(alias='exp')
    iat: int = Field(alias='iat')
    nonce: str | None = Field(alias='nonce', default=None)
    other_claims: dict = Field(alias='otherClaims', default={})


class OpenIdUserLoggedInEvent(BaseModel):
    """
    Model for "OpenID User Logged In" event
    """
    access_token: str = Field(alias='accessToken')
    token_type: str = Field(alias='tokenType')
    id_token: IdToken = Field(alias='idToken')
    id_token_jwt: str = Field(alias='idTokenJwt')
    expires_in: int = Field(alias='expiresIn')
    refresh_token: str | None = Field(alias='refreshToken', default=None)
