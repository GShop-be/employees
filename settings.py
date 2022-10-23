from pathlib import Path

from config import config_from_yaml, ConfigurationSet, config_from_python

from configs import service_config


__all__ = [
    'Settings'
]


Settings = ConfigurationSet(
    config_from_yaml(
        str(Path('configs', 'db-config.yaml')),
        read_from_file=True
    ),
    config_from_python(service_config, separator='__')
)
