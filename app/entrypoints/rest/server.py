from communications.rest import FastApiApp

from .v1 import ApiV1App


class RestServer(FastApiApp):
    sub_apps = [
        ApiV1App
    ]
