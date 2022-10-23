from fastapi import APIRouter, Request, Response, Header, Cookie
from pydantic import BaseModel

from settings import Settings

from app.company import AuthRequest, AuthResponse, RefreshTokenRequest, RevokeToken


__all__ = [
    'auth_router'
]


auth_router = APIRouter(prefix='/login')


class AuthRequestBody(BaseModel):
    email: str
    password: str


@auth_router.post('/auth', response_model=AuthResponse)
async def auth(
    request: Request,
    response: Response,
    body: AuthRequestBody,
    user_agent: str = Header()
):
    company = request.state.company

    result = await company.auth.auth(AuthRequest(
        email=body.email,
        password=body.password,
        user_agent_str=user_agent
    ))

    response.set_cookie(Settings.AUTH_TOKEN_STORE_NAME, result.auth_token)
    response.set_cookie(Settings.REFRESH_TOKEN_STORE_NAME, result.refresh_token)

    return result


@auth_router.post('/refresh', response_model=AuthResponse)
async def refresh(
    request: Request,
    response: Response,

    auth_token: str = Cookie(alias=Settings.AUTH_TOKEN_STORE_NAME),
    refresh_token: str = Cookie(alias=Settings.REFRESH_TOKEN_STORE_NAME),
    user_agent: str = Header()
):
    company = request.state.company

    result = await company.auth.refresh(RefreshTokenRequest(
        refresh_token=refresh_token,
        auth_token=auth_token,
        user_agent_str=user_agent
    ))

    response.set_cookie(Settings.AUTH_TOKEN_STORE_NAME, result.auth_token)
    response.set_cookie(Settings.REFRESH_TOKEN_STORE_NAME, result.refresh_token)

    return result


@auth_router.post('/logout', status_code=200)
async def revoke(
    request: Request,
    response: Response,

    auth_token: str = Cookie(alias=Settings.AUTH_TOKEN_STORE_NAME),
):
    company = request.state.company

    await company.auth.revoke(RevokeToken(
        token=auth_token
    ))

    response.delete_cookie(Settings.AUTH_TOKEN_STORE_NAME)
    response.delete_cookie(Settings.REFRESH_TOKEN_STORE_NAME)
