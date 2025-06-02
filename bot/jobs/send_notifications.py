import datetime
import traceback

import logger
from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram.enums import ParseMode

import config
from bot.keyboards.buttons import buttons
from asyncio import sleep as asleep
from bot import controllers

from bot.sourcefile import pictures, texts
from bot import bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

texts = texts()
buttons = buttons()


async def send_notification_sale():
    users = await controllers.get_active_users(60)

    keyboard = [
        [buttons().Stars],
        [buttons().Card, buttons().Stripe],
        [buttons().Lava, buttons().Support],
    ]

    for user in users:
        try:
            await controllers.send_message(
                chat_id=user.telegram_id,
                photo=pictures.NOTIFICATION_SALE,
                text=texts().NOTIFICATION_SALE,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
            )
        except:
            continue

    logger.logger.info(users)


async def send_notification_group():
    users = await controllers.get_active_users(30)

    for user in users:
        try:
            await controllers.send_message(
                chat_id=user.telegram_id,
                text=texts().POST_PROMO,
            )
        except:
            continue

    logger.logger.info(users)
