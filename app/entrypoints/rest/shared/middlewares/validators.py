from typing import Any
from datetime import datetime

from asymetric_jwt import AsymmetricJwt, InvalidSignature
from pydantic import BaseModel, validator

from settings import Settings


__all__ = [
    'AuthTokenValidator'
]


class AuthTokenValidator(BaseModel):
    token: str

    @validator('token')
    def validate_auth_token(cls, value: str, values: dict[str, Any], **kwargs):
        jwt_util = AsymmetricJwt(public_key=Settings.PUBLIC_KEY)

        try:
            payload = jwt_util.decode(value)
        except InvalidSignature:
            raise ValueError('Invalid signature.')

        valid_ts = payload.get('valid_until')

        if valid_ts < datetime.now().timestamp():
            raise ValueError('Auth token expired.')
