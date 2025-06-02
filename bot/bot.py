import asyncio
from redis.asyncio import Redis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from config import (
    REDIS_DB,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
    TELEGRAM_BOT_TOKEN,
    DATABASE_URL
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

loop = asyncio.get_event_loop()
redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD
)
storage = RedisStorage(redis)
dp = Dispatcher(storage=storage)
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True
)
scheduler = AsyncIOScheduler()
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
