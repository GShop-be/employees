from db_entities.session_maker import SessionMaker

from .services import EmployeesService, AuthService


__all__ = [
    'Company'
]


class Company:
    def __init__(self, session_maker: SessionMaker):
        self._employees_service = EmployeesService(session_maker)
        self._auth_service = AuthService(session_maker)

    @property
    def employees(self) -> EmployeesService:
        return self._employees_service

    @property
    def auth(self) -> AuthService:
        return self._auth_service
