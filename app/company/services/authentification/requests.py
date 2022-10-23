from pydantic import BaseModel, EmailStr


__all__ = [
    'AuthRequest',
    'RefreshTokenRequest',
    'RevokeToken'
]


class AuthRequest(BaseModel):
    email: EmailStr
    password: str
    user_agent_str: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    auth_token: str
    user_agent_str: str


class RevokeToken(BaseModel):
    token: str
