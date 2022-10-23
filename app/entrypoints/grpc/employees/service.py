import grpc

from grpc_metadata import company_to_employees_pb2, company_to_employees_pb2_grpc

from ..utils import get_company_from_context

from ....company import CompanyPool, NewEmployeeRequest


__all__ = [
    'company_to_employees_pb2_grpc',
    'Employees'
]


class Employees(company_to_employees_pb2_grpc.EmployeesServiceServicer):

    def __init__(self, company_pool: CompanyPool):
        self._company_pool = company_pool

    async def CreateSuperUser(
        self,
        request: company_to_employees_pb2.UserRequest,
        context: grpc.aio.ServicerContext
    ) -> company_to_employees_pb2.UserResponse:
        company = await get_company_from_context(self._company_pool, context)

        user = await company.employees.add(
            NewEmployeeRequest(
                name=request.name,
                email=request.email,
                password=request.password,
                repeated_password=request.repeat_password,
                role='super'
            )
        )

        return company_to_employees_pb2.UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role
        )
