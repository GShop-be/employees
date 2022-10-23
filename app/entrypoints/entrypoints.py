from .grpc import SideServiceServer
from .rest import RestServer

from ..company import CompanyPool


__all__ = [
    'Entrypoints'
]


class Entrypoints:
    def __init__(self, company_pool: CompanyPool):
        self._company_pool = company_pool

        self._side_service_server = SideServiceServer(self._company_pool)
        self._rest_server = RestServer(
            host='localhost',
            port=8000,
            company_pool=self._company_pool
        )

    async def start(self) -> None:
        self._rest_server.start()
        await self._side_service_server.start()

    async def stop(self) -> None:
        self._rest_server.stop()
