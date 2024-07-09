import asyncio
import aioschedule
from aiogram import Bot, types

from sqlalchemy import func, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.engine import engine

from database.orm_query import (
    orm_get_posts_by_group,
    orm_get_post_all,
    orm_get_users_by_group,
    orm_get_group_all
)
# ! garbage collection
async def notif(bot: Bot):
    # session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    # session = session_maker()

    # Получить интервал оповещения группы NI
    for group in await orm_get_group_all(await get_session()):
        notification_interval = group.notificationInterval
        # Получить список пользователей этой группы из БД
        print("==========------group ", group.name)
        print("================notification_interval ", notification_interval)
        group_users = await orm_get_users_by_group(await get_session(), group.id)
        print("=================group_users sucsessful")
        # Пробежаться по дедлайнам в БД
        # for post in await orm_get_posts_by_group(await get_session(), group.id):
            # Сравнить дату дедлайна минус NI c текущей датой
        for post in await orm_get_post_all(await get_session()):
            print(post.deadline)
            # print(post.deadline-notification_interval)
            print(func.now())

            # # Если даты совпадают, то выслать оповещение о дедлайне группе
            # if(post.deadline-notification_interval == func.now()):
            #     for group_user in group_users:
            #         await bot.send_message(chat_id = group_user.telegram_id, text=post.text)
            for group_user in group_users:
                await bot.send_message(chat_id = 635260494, text=post.text)
    
# async def notif(bot: Bot, session: session, group, user):
#     # Получить интервал оповещения группы NI
#     notification_interval = group.notificationInterval
#     # Пробежаться по дедлайнам в БД
#     for post in await orm_get_posts_by_group(session, group.id):
#         # Сравнить дату дедлайна минус NI c текущей датой
#         print(post.deadline)
#         print(post.deadline-notification_interval)
#         print(func.now())

#         # Если даты совпадают, то выслать оповещение о дедлайне группе
#         if(post.deadline-notification_interval == func.now()):
#             await bot.send_message(chat_id = user.telegram_id, text=post.text)

async def scheduler(bot: Bot):
    aioschedule.every().day.at("22:33").do(notif, bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def get_session():
    session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    session = session_maker()
    return session