from . import handlers, jobs
from logger import logger
from .bot import dp, loop, bot, scheduler
from .database import init_db


@dp.startup()
async def startup():
    jobs.setup_jobs()
    scheduler.start()
    await init_db()
    handlers.register_handlers(router=dp)
    logger.info("Starting pooling...")


@dp.shutdown()
async def shutdown():
    logger.info("Goodbye!")


def start_bot():
    loop.run_until_complete(dp.start_polling(bot))
