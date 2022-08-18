from .company import CompanyPool
from .core import Core
from .entrypoints import Entrypoints


__all__ = [
    'Application'
]


class Application:
    def __init__(self):
        self.core = Core()

        self.company_pool = CompanyPool(
            self.core.async_session_maker_factory,
            self.core.initializer_factory
        )

        self.entrypoints = Entrypoints()

    async def start(self):
        company = await self.company_pool.get('dev')

        await self.entrypoints.start()
