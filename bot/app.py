# -*- coding: utf-8 -*-
import asyncio
import logging

import settings
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.student import student_router
from handlers.headman import headman_router
from handlers.user_private import user_private_router

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(headman_router)
dp.include_router(student_router)

async def on_startup(bot):
    print("Bot started")


async def on_shutdown(bot):
    print("Bot stopped")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
