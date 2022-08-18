from typing import Any

from db_entities.session_maker import SessionMaker
from repositories.local import LocalRepository

from ..models import Employe


__all__ = [
    'EmployeesService'
]


class EmployeesService:
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker
        self._multi_repository = LocalRepository(self._session_maker)

    async def get(self, id_: str) -> Employe:
        return await self._multi_repository.find_one(Employe, Employe.id == id_)

    async def list(self) -> Employe:
        return await self._multi_repository.find(Employe)

    async def add(self, employe_data: dict[str, Any]) -> Employe:
        employe = Employe(
            **employe_data
        )

        await self._multi_repository.add(employe)

        return employe

    async def update(self, id_: str, fields_to_update: dict[str, Any]) -> None:
        employe = await self._multi_repository.find_one(Employe, Employe.id == id_)

        for key, value in fields_to_update.items():
            setattr(employe, key, value)

        await self._multi_repository.update(employe)

    async def delete(self, id_: str) -> None:
        employe = await self._multi_repository.find_one(Employe, Employe.id == id_)

        await self._multi_repository.delete(employe)
