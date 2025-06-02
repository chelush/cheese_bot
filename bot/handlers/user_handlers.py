import inspect
import time
import datetime

import config
from bot.controllers import controllers
from logger import logger
from typing import Callable, Coroutine
from aiogram import Router, F
from aiogram.fsm.context import FSMContext, StorageKey
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, Message, LabeledPrice
from aiogram.enums import ChatAction
from bot.filters import CallbackDataFilter
from asyncio import sleep as asleep
from ..bot import loop, bot, dp
from bot.keyboards import buttons
from bot import funcs, pictures, states, callbacks
from bot.sourcefile import pictures, texts
from bot.types import NavigationHistory
from models import User

texts = texts()
buttons = buttons.buttons()


def register_handlers(router: Router):
    # message handlers
    router.message.register(
        handler_wrapper(menu_event),
        F.text.regexp("^/start$"),
    )
    # callback_query handlers
    router.callback_query.register(
        handler_wrapper(examples_event),
        CallbackDataFilter(callbacks.NEXT),
    )
    router.callback_query.register(
        handler_wrapper(price_event),
        CallbackDataFilter(callbacks.EXAMPLES),
    )
    router.callback_query.register(
        handler_wrapper(catalog_event),
        CallbackDataFilter(f"{callbacks.PRICE}|{callbacks.PAY}")
    )
    router.callback_query.register(
        handler_wrapper(payment_russia_event),
        CallbackDataFilter(callbacks.CARD)
    )
    router.callback_query.register(
        handler_wrapper(payment_usa_event),
        CallbackDataFilter(f"{callbacks.STRIPE}|{callbacks.LAVA}")
    )
    router.callback_query.register(
        handler_wrapper(payment_starts_event),
        CallbackDataFilter(callbacks.STARS)
    )


def handler_wrapper(
        callback: Callable[..., Coroutine],
        delete_query_message: bool = False,
):
    annotations = inspect.get_annotations(callback)

    async def wrapper(call: CallbackQuery | Message, state: FSMContext):
        user_id = call.from_user.id
        args = {}
        query = call if type(call) is CallbackQuery else None

        if User in annotations.values():
            user = await controllers.fetch_user(user_telegram=call.from_user)

        for arg_name, arg_type in annotations.items():
            if arg_type is User:
                args[arg_name] = user
            if arg_type is FSMContext:
                args[arg_name] = state
            elif arg_type is Message:
                args[arg_name] = call if type(call) is Message else None
            elif arg_type is CallbackQuery:
                args[arg_name] = query
            elif arg_name == "user_id" and arg_type is int:
                args[arg_name] = user_id

        await bot.send_chat_action(chat_id=user.telegram_id, action=ChatAction.TYPING)
        await asleep(1)

        await callback(**args)
        if delete_query_message and query:
            try:
                await query.message.delete()
            except:
                pass

    return wrapper


async def menu_event(query: CallbackQuery, user: User):
    keyboard = [
        [buttons().NextMenu, buttons().Payment],
    ]
    await controllers.update_user_updated_at(user_id=user.telegram_id, new_time=datetime.datetime.utcnow())
    await controllers.send_message(
        chat_id=user.telegram_id,
        text=texts().WELCOME,
        photo=pictures.MENU,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


async def examples_event(query: CallbackQuery, user: User):
    keyboard = [
        [buttons().NextExamples],
    ]
    await controllers.send_message(
        chat_id=user.telegram_id,
        text=texts().EXAMPLES,
        photo=pictures.EXAMPLES,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


async def price_event(query: CallbackQuery, user: User):
    keyboard = [
        [buttons().Price],
    ]
    await controllers.send_message(
        chat_id=user.telegram_id,
        text=texts().PRICE,
        photo=pictures.PRICE,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


async def catalog_event(query: CallbackQuery, user: User):
    keyboard = [
        [buttons().Stars],
        [buttons().Card, buttons().Stripe],
        [buttons().Lava, buttons().Support],
    ]
    await controllers.send_message(
        chat_id=user.telegram_id,
        text=texts().CATALOG,
        photo=pictures.CATALOG,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


async def payment_russia_event(query: CallbackQuery, user: User):
    keyboard = [
        [buttons().Pay],
    ]
    await controllers.send_message(
        chat_id=user.telegram_id,
        text=texts().PAYMENT_RUSSIA,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


async def payment_usa_event(query: CallbackQuery, user: User):
    keyboard = [
        [buttons().Pay],
    ]
    await controllers.send_message(
        chat_id=user.telegram_id,
        text=texts().PAYMENT_USA,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


async def payment_starts_event(query: CallbackQuery, user: User):
    prices = [LabeledPrice(label="1 ⭐", amount=1)]
    await bot.send_invoice(
        chat_id=user.telegram_id,
        title="Оплата",
        description="Купить подписку",
        payload="buy_1_star",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter="stars_payment",
        is_flexible=False
    )
