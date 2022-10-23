from asymetric_jwt import AsymmetricJwt
from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import ValidationError as PydValidationError

from settings import Settings
from communications.errors import AuthenticationError, BadRequest, ValidationError
from communications.rest import application_error_exception_handler, validation_error_exception_handler

from .validators import AuthTokenValidator


__all__ = [
    'AuthenticationMiddleware',
    'CompanyExtractorMiddleware'
]


class AuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        auth_token = request.headers.get(Settings.AUTH_TOKEN_STORE_NAME)

        if not auth_token:
            auth_token = request.cookies.get(Settings.AUTH_TOKEN_STORE_NAME)

        if not auth_token:
            return application_error_exception_handler(
                request,
                AuthenticationError()
            )

        try:
            AuthTokenValidator(token=auth_token)
        except PydValidationError as exc:
            return validation_error_exception_handler(
                request,
                ValidationError(info=exc.errors())
            )

        jwt_util = AsymmetricJwt(public_key=Settings.PUBLIC_KEY)
        payload = jwt_util.decode(auth_token)

        request.state.requestor = payload

        return await call_next(request)


class CompanyExtractorMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        company_id = request.headers.get(Settings.COMPANY_NAME_STORE_NAME)

        if not company_id:
            return application_error_exception_handler(
                request,
                BadRequest(details=f'You must provide company id in {Settings.COMPANY_NAME_STORE_NAME} header.')
            )

        company_pool = request.app.company_pool

        request.state.company_id = company_id
        company = await company_pool.get(company_id)
        request.state.company = company

        return await call_next(request)
