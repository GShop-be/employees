import hashlib
import uuid
import datetime

import jwt
from user_agents import parse

from settings import Settings
from db_entities.session_maker import SessionMaker
from repositories.local import LocalRepository
from communications.errors import NotFoundError, BaseError
from asymetric_jwt import AsymmetricJwt

from .requests import AuthRequest, RefreshTokenRequest, RevokeToken
from .responses import AuthResponse
from .validators import RefreshTokenExpirationValidate, AuthTokenExpirationValidate

from ...models import Employe, AuthToken, RefreshToken


__all__ = [
    'AuthService'
]


class AuthService:
    def __init__(
        self,
        session_maker: SessionMaker,
    ):
        self._session_maker = session_maker

        self._multi_repository = LocalRepository(self._session_maker)
        self._jwt_tool = AsymmetricJwt(Settings.PRIVATE_KEY)

    async def auth(self, request: AuthRequest) -> AuthResponse | BaseError:
        employee = await self._multi_repository.find_one(
            Employe,
            Employe.email == request.email
        )

        if not employee:
            raise NotFoundError(entity='employee', request=request.dict())

        time_now = datetime.datetime.now()
        auth_token_valid_until = time_now + datetime.timedelta(hours=Settings.AUTH_TOKEN_HOURS_LIVING)
        refresh_token_valid_until = time_now + datetime.timedelta(days=Settings.REFRESH_TOKEN_DAYS_LIVING)

        user_agent_data = parse(request.user_agent_str)

        auth_token = AuthToken(
            employee_id=employee.id,
            token=self._jwt_tool.encode(
                {
                    "name": employee.name,
                    "email": employee.email,
                    "role": employee.role,
                    "valid_until": auth_token_valid_until.timestamp()
                }
            ),
            valid_until=auth_token_valid_until,
            browser=user_agent_data.browser.family,
            browser_version=user_agent_data.browser.version_string,
            os=user_agent_data.os.family,
            os_version=user_agent_data.os.version_string,
            device_family=user_agent_data.device.family,
            device_brand=user_agent_data.device.brand,
            device_model=user_agent_data.device.model
        )

        refresh_token = RefreshToken(
            refresh_token=hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest(),
            auth_token=auth_token.token,
            valid_until=refresh_token_valid_until
        )

        await self._multi_repository.add(auth_token)
        await self._multi_repository.add(refresh_token)

        return AuthResponse(
            auth_token=auth_token.token,
            refresh_token=refresh_token.refresh_token
        )

    async def refresh(self, request: RefreshTokenRequest) -> AuthResponse | BaseError:
        refresh_token = await self._multi_repository.find_one(
            RefreshToken,
            RefreshToken.refresh_token == request.refresh_token
        )

        if not refresh_token:
            raise NotFoundError(entity='refresh_token', request=request.dict())

        RefreshTokenExpirationValidate(refresh_token=refresh_token)

        auth_token = await self._multi_repository.find_one(
            AuthToken,
            AuthToken.token == request.auth_token
        )

        if not auth_token:
            raise NotFoundError(entity='auth_token', request=request.dict())

        employee = await self._multi_repository.find_one(
            Employe,
            Employe.id == auth_token.employee_id
        )

        time_now = datetime.datetime.now()
        auth_token_valid_until = time_now + datetime.timedelta(hours=Settings.AUTH_TOKEN_HOURS_LIVING)
        refresh_token_valid_until = time_now + datetime.timedelta(days=Settings.REFRESH_TOKEN_DAYS_LIVING)

        user_agent_data = parse(request.user_agent_str)

        new_auth_token = AuthToken(
            employee_id=employee.id,
            token=self._jwt_tool.encode(
                {
                    "name": employee.name,
                    "email": employee.email,
                    "role": employee.role,
                    "valid_until": auth_token_valid_until.timestamp()
                }
            ),
            valid_until=auth_token_valid_until,
            browser=user_agent_data.browser.family,
            browser_version=user_agent_data.browser.version_string,
            os=user_agent_data.os.family,
            os_version=user_agent_data.os.version_string,
            device_family=user_agent_data.device.family,
            device_brand=user_agent_data.device.brand,
            device_model=user_agent_data.device.model
        )

        new_refresh_token = RefreshToken(
            refresh_token=hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest(),
            auth_token=new_auth_token.token,
            valid_until=refresh_token_valid_until
        )

        await self._multi_repository.delete(auth_token)
        await self._multi_repository.delete(refresh_token)

        await self._multi_repository.add(new_auth_token)
        await self._multi_repository.add(new_refresh_token)

        return AuthResponse(
            auth_token=new_auth_token.token,
            refresh_token=new_refresh_token.refresh_token
        )

    async def revoke(self, request: RevokeToken) -> BaseError | None:
        auth_token = await self._multi_repository.find_one(
            AuthToken,
            AuthToken.token == request.token
        )

        if not auth_token:
            raise NotFoundError(entity='auth_token', request=request.dict())

        AuthTokenExpirationValidate(expiration_datetime=auth_token.valid_until)

        refresh_token = await self._multi_repository.find_one(
            RefreshToken,
            RefreshToken.auth_token == request.token
        )

        await self._multi_repository.delete(auth_token)
        await self._multi_repository.delete(refresh_token)
