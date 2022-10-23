from typing import Any
from uuid import uuid4
import hashlib

from db_entities.session_maker import SessionMaker
from repositories.local import LocalRepository
from communications.errors import NotFoundError, EntityAlreadyExists, BadRequest

from .requests import NewEmployeeRequest, GetEmployeeRequest
from .responses import EmployeeResponse

from ...models import Employe


__all__ = [
    'EmployeesService'
]


class EmployeesService:
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker
        self._multi_repository = LocalRepository(self._session_maker)

    async def get(self, request: GetEmployeeRequest) -> EmployeeResponse:
        employee = await self._multi_repository.find_one(Employe, Employe.id == request.id)

        if not employee:
            raise NotFoundError(
                entity='employee',
                request=request.dict()
            )

        return self._make_response_model(employee)

    async def list(self) -> list[EmployeeResponse]:
        employees = await self._multi_repository.find(Employe)

        return [self._make_response_model(employee) for employee in employees]

    async def add(self, request: NewEmployeeRequest) -> EmployeeResponse:

        if not self._ensure_passwords_match(request.password, request.repeated_password):
            raise BadRequest(
                request=request.dict(),
                details='Password must match.'
            )

        employee = await self._multi_repository.find_one(Employe, Employe.email == request.email)

        if employee:
            raise EntityAlreadyExists(
                entity='employee',
                request=request.dict()
            )

        new_employee = Employe(
            id=uuid4().hex,
            name=request.name,
            email=request.email,
            role=request.role,
            password=hashlib.sha256(request.password.encode()).hexdigest()
        )

        await self._multi_repository.add(new_employee)

        return self._make_response_model(employee)

    async def update(self, id_: str, fields_to_update: dict[str, Any]) -> None:
        employe = await self._multi_repository.find_one(Employe, Employe.id == id_)

        if not employe:
            raise NotFoundError(
                entity='employee',
                request={'id': id_}
            )

        for key, value in fields_to_update.items():
            setattr(employe, key, value)

        await self._multi_repository.update(employe)

    async def delete(self, id_: str) -> None:
        employe = await self._multi_repository.find_one(Employe, Employe.id == id_)

        if not employe:
            raise NotFoundError(
                entity='employee',
                request={'id': id_}
            )

        await self._multi_repository.delete(employe)

    @staticmethod
    def _ensure_passwords_match(password: str, password2: str) -> bool:
        return password == password2

    @staticmethod
    def _make_response_model(entity: Employe) -> EmployeeResponse:
        return EmployeeResponse(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            role=entity.role
        )