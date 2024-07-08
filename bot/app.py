# -*- coding: utf-8 -*-
import asyncio
import logging

import settings

from middlewares.db import DataBaseSession
from middlewares.auth_student import AuthStudent
from middlewares.auth_headman import AuthHeadman

from database.engine import create_db, drop_db, session_maker


from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
# from handlers.admin_private import admin_router
from handlers.student import student_router
from handlers.headman import headman_router
from handlers.user_private import user_private_router

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

student_router.message.middleware(AuthStudent(session_pool=session_maker))
headman_router.message.middleware(AuthHeadman(session_pool=session_maker))

# dp.include_router(admin_router)
dp.include_router(user_private_router)
dp.include_router(student_router)
dp.include_router(headman_router)

async def on_startup(bot):
    print("Bot started")
    # run_param = False
    # if run_param:
    #    await drop_db()
    # # Пока всегда дропаем бд при перезапуске (для отладки)
    await drop_db()

    await create_db()


async def on_shutdown(bot):
    print("Bot stopped")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
