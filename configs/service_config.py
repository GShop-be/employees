from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent
ALEMBIC_CONFIG_PATH = ROOT_DIR / 'alembic.ini'

PRIVATE_KEY_PATH = ROOT_DIR / 'configs' / 'private_key.pem'
PUBLIC_KEY_PATH = ROOT_DIR / 'configs' / 'public_key.pem'

PRIVATE_KEY = None
PUBLIC_KEY = None

AUTH_TOKEN_HOURS_LIVING = 2
REFRESH_TOKEN_DAYS_LIVING = 30

AUTH_TOKEN_STORE_NAME = 'gshop-auth-token'
REFRESH_TOKEN_STORE_NAME = 'gshop-refresh-token'
COMPANY_NAME_STORE_NAME = 'gshop-company-id'
