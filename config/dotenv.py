from envparse import env

env.read_envfile()

TELEGRAM_BOT_TOKEN: str = env.str('TELEGRAM_BOT_TOKEN')

POSTGRES_USER: str = env.str('POSTGRES_USER')
POSTGRES_PASSWORD: str = env.str('POSTGRES_PASSWORD')
POSTGRES_HOST: str = env.str('POSTGRES_HOST')
POSTGRES_PORT: int = env.int('POSTGRES_PORT')
POSTGRES_DB: str = env.str('POSTGRES_DB')

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

TELEGRAM_API_ID: int = env.int('TELEGRAM_API_ID', default=2040)
TELEGRAM_API_HASH: str = env.str('TELEGRAM_API_HASH', default='b18441a1ff607e10a989891a5462e627')
TELEGRAM_DEVICE_MODEL: str = env.str('TELEGRAM_DEVICE_MODEL', default='MacBook Air M1')
TELEGRAM_SYSTEM_VERSION: str = env.str('TELEGRAM_SYSTEM_VERSION', default='macOS 14.4.1')
TELEGRAM_APP_VERSION: str = env.str('TELEGRAM_APP_VERSION', default='4.16.8 arm64')

REDIS_HOST: str = env.str('REDIS_HOST', default='redis')
REDIS_PORT: int = env.int('REDIS_PORT', default=6379)
REDIS_DB: int = env.int('REDIS_DB', default=0)
REDIS_PASSWORD: str | None = env.str('REDIS_PASSWORD', default=None)
