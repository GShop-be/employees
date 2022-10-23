from communications.grpc import GrpcServer

from .employees import Employees, company_to_employees_pb2_grpc

from ...company import CompanyPool


__all__ = [
    'SideServiceServer'
]


class SideServiceServer:
    def __init__(self, company_pool: CompanyPool):
        self._company_pool = company_pool

        self._grpc_server = GrpcServer()

    async def start(self):
        await self._grpc_server.start(
            (
                (company_to_employees_pb2_grpc.add_EmployeesServiceServicer_to_server, Employees(self._company_pool)),
            )
        )
