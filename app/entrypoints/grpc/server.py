import logging

import grpc

from .employees import Employees, company_to_employees_pb2_grpc


__all__ = [
    'GrpcServer'
]


class GrpcServer:
    async def start(self):
        server = grpc.aio.server()

        listen_on = '[::]:50051'

        self._register_servicers(server)

        server.add_insecure_port(listen_on)

        logging.info(f'Starting Grpc server on {listen_on}.')

        await server.start()
        await server.wait_for_termination()

        logging.info('Grpc server was started')

    def _register_servicers(self, server: grpc.aio.Server) -> None:
        company_to_employees_pb2_grpc.add_EmployeesServiceServicer_to_server(Employees(), server)
