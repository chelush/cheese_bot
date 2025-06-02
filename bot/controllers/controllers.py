import asyncio
from asyncio import sleep as asleep
import datetime
from typing import Tuple

import telethon
import time
import aiogram
from decimal import Decimal, ROUND_HALF_EVEN

from pyasn1_modules.rfc7906 import aa_userCertificate

import config
from logger import logger
from aiogram.types import (
    InputFile,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    Message,
)
from config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_PASSWORD,
)
from pymongo import ASCENDING, DESCENDING
from aiogram.types.base import UNSET_DISABLE_WEB_PAGE_PREVIEW, UNSET_PARSE_MODE
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest, AddChatUserRequest, \
    EditChatAdminRequest, MigrateChatRequest
from telethon.tl.functions.channels import InviteToChannelRequest, TogglePreHistoryHiddenRequest, EditAdminRequest
from telethon.tl.types import ChatAdminRights, Updates
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.types import InputPeerChat, InputUser, InputChannel
from beanie.operators import Set
from config import (
    CONFIG_CACHE_TIME,
)
from telethon.tl.functions.folders import EditPeerFoldersRequest
from telethon.tl.types import InputFolderPeer
from config import USER_CACHE_TIME
from redis.asyncio import Redis
from ..bot import redis, bot, loop
from bot.database import async_engine, async_session_maker
from bot import funcs
from models import User
from sqlalchemy import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
)


async def send_message(
        chat_id: int,
        text: str,
        photo: InputFile | str = None,
        document: InputFile | str = None,
        parse_mode: str = UNSET_PARSE_MODE,
        reply_markup: (
                InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | list
        ) = None,
        disable_web_page_preview: bool = UNSET_DISABLE_WEB_PAGE_PREVIEW,
        reply_to_message_id: int = None
) -> Message:
    base_args = dict(
        chat_id=chat_id,
        parse_mode=parse_mode,
        reply_markup=reply_markup,
        reply_to_message_id=reply_to_message_id
    )
    if type(reply_markup) is list:
        reply_markup = InlineKeyboardMarkup(inline_keyboard=reply_markup)
    if photo:
        return await bot.send_photo(
            **base_args,
            photo=photo,
            caption=text,
        )
    elif document:
        return await bot.send_document(
            **base_args,
            document=document,
            caption=text,
        )
    else:
        return await bot.send_message(
            **base_args,
            text=text,
            disable_web_page_preview=disable_web_page_preview,
        )


async def create_user(user_telegram: aiogram.types.User, session: AsyncSession = None) -> User:
    user = User(
        telegram_id=user_telegram.id,
        lang=user_telegram.language_code,
        telegram=user_telegram.model_dump_json(),
        is_admin=False
    )
    async with session or async_session_maker() as session:
        merged_user = await session.merge(user)
        await session.commit()
        return merged_user


async def fetch_user(user_telegram: aiogram.types.User, session: AsyncSession = None) -> User:
    async with session or async_session_maker() as session:
        query = select(User).where(User.telegram_id == user_telegram.id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        user.updated_at = datetime.datetime.now()
        await session.flush()
        logger.info(f"Updated user {user.telegram_id=} at {user.updated_at}")
        if user is None:
            user = await create_user(user_telegram, session=session)
        return user


async def update_user_updated_at(user_id: int, new_time: datetime.datetime, session: AsyncSession = None):
    async with session or async_session_maker() as session:
        stmt = (
            update(User)
            .where(User.telegram_id == user_id)
            .values(updated_at=new_time)
        )
        await session.exec(stmt)
        await session.commit()


async def get_active_users(hours: int, session: AsyncSession = None) -> list[User]:
    threshold_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
    async with session or async_session_maker() as session:
        stmt = select(User).where(User.updated_at >= threshold_time)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users
