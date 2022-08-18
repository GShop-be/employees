from db_entities.session_maker import SessionMaker

from .services import EmployeesService


__all__ = [
    'Company'
]


class Company:
    def __init__(self, session_maker: SessionMaker):
        self._employees_service = EmployeesService(session_maker)
