import asyncio
from typing import Callable

from settings import Settings

from .company import Company


__all__ = [
    'CompanyPool'
]


class CompanyPool:

    def __init__(
        self,
        async_session_maker_factory: Callable,
        initializer_factory: Callable
    ):
        self._cached: dict[str, Company] = {}

        self._async_session_maker_factory = async_session_maker_factory
        self._initializer_factory = initializer_factory

    async def get(self, id_: str) -> Company:
        if self._cached.get(id_) is not None:
            return self._cached[id_]

        return await self._new(id_)

    async def _new(
        self,
        id_: str,
    ):
        async_session_maker = self._async_session_maker_factory(db_name=f'{Settings.db.company.db_prefix}_{id_}')

        initializer = self._initializer_factory(async_session_maker)

        init_coro = asyncio.create_task(initializer.initialize())

        done, _ = await asyncio.wait({init_coro})

        if init_coro in done:
            company = Company(async_session_maker)

            self._cached[id_] = company

            return company
