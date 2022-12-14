from functools import partial

from db_entities.initilaizer import Initializer
from db_entities.session_maker import SessionMaker

from settings import Settings

from .secret_keys import SecretKeys

from ..company import Base


__all__ = [
    'Core'
]


class Core:
    def __init__(self):
        self.async_session_maker_factory = partial(
            SessionMaker,
            driver='postgresql+asyncpg',
            user=Settings.db.company.user,
            password=Settings.db.company.password,
            host=Settings.db.company.host,
            port=Settings.db.company.port,
            is_async=True,
            echo=False,
        )

        self.initializer_factory = partial(
            Initializer,
            metadata=Base.metadata,
            alembic_config_path=Settings.ALEMBIC_CONFIG_PATH,
        )

        self.secret_keys = SecretKeys()

    def initialize(self):
        self.secret_keys.load_keys()