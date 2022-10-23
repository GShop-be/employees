from communications.rest import FastApiApp

from .auth import auth_router
from .common import CommonApp

from ..shared import CompanyExtractorMiddleware


__all__ = [
    'ApiV1App'
]


class ApiV1App(FastApiApp):
    as_sub_app = True
    path = '/api/v1'

    sub_apps = [
        CommonApp
    ]

    routers = [
        auth_router
    ]

    middlewares = [
        CompanyExtractorMiddleware
    ]
