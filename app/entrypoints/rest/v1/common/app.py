from communications.rest import FastApiApp

from .employees import employee_router

from ...shared import AuthenticationMiddleware


__all__ = [
    'CommonApp'
]


class CommonApp(FastApiApp):
    as_sub_app = True
    path = ''

    routers = [
        employee_router
    ]

    middlewares = [
        AuthenticationMiddleware
    ]
