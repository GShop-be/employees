from .grpc import GrpcServer


__all__ = [
    'Entrypoints'
]


class Entrypoints:
    def __init__(self):
        self._grpc_server = GrpcServer()

    async def start(self) -> None:
        await self._grpc_server.start()
