from pydantic import BaseModel


__all__ = [
    'AuthResponse'
]


class AuthResponse(BaseModel):
    auth_token: str
    refresh_token: str
