from .company import CompanyPool
from .core import Core
from .entrypoints import Entrypoints


__all__ = [
    'Application'
]


class Application:
    def __init__(self):
        self.core = Core()

        self._company_pool = CompanyPool(
            self.core.async_session_maker_factory,
            self.core.initializer_factory
        )

        self.entrypoints = Entrypoints(self._company_pool)

    async def start(self):
        self.core.initialize()

        await self.entrypoints.start()

    async def stop(self):
        await self.entrypoints.stop()

