from aiogram import Router
from . import (
    user_handlers,
)


def register_handlers(router: Router):
    user_handlers.register_handlers(router=router)
