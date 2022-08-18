import grpc

# from ..metadata import company_to_employees_pb2, company_to_employees_pb2_grpc

from grpc_metadata import company_to_employees_pb2, company_to_employees_pb2_grpc


__all__ = [
    'company_to_employees_pb2_grpc',
    'Employees'
]


class Employees(company_to_employees_pb2_grpc.EmployeesServiceServicer):

    async def CreateUser(
        self,
        request: company_to_employees_pb2.UserRequest,
        context: grpc.aio.ServicerContext
    ) -> company_to_employees_pb2.UserResponse:
        return company_to_employees_pb2.UserResponse(
            name='test',
            email='test@test.ru',
            role='admin'
        )
