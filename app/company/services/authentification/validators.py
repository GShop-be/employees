from datetime import datetime
from typing import Any

from pydantic import BaseModel, validator

from ...models import AuthToken, RefreshToken


__all__ = [
    'AuthTokenExpirationValidate',
    'RefreshTokenExpirationValidate'
]


class AuthTokenExpirationValidate(BaseModel):
    auth_token: AuthToken

    @validator('auth_token')
    def token_expired(cls, value: AuthToken, values: dict[str, Any], **kwargs):
        if value.valid_until >= datetime.now():
            raise ValueError('Token expired.')
        return value

    class Config:
        arbitrary_types_allowed = True


class RefreshTokenExpirationValidate(BaseModel):
    refresh_token: RefreshToken

    @validator('refresh_token')
    def token_expired(cls, value: AuthToken, values: dict[str, Any], **kwargs):
        if value.valid_until >= datetime.now():
            raise ValueError('Token expired.')
        return value

    class Config:
        arbitrary_types_allowed = True
