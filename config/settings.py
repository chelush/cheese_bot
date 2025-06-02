import datetime
from pathlib import Path
from yarl import URL
from . import dotenv

ROOT_DIR = Path(__file__).parents[1]
LOG_FILES_DIR = ROOT_DIR / 'logs'

ADMINS_LIST = []

CONFIG_CACHE_TIME = datetime.timedelta(seconds=30)
USER_CACHE_TIME = datetime.timedelta(days=3)
