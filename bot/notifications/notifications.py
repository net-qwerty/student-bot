import datetime

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from database.engine import engine

from database.orm_query import (
    orm_get_posts_by_group,
    orm_get_users_by_group,
    orm_get_group_all
)

async def notif(bot: Bot):

    # Получить интервал оповещения группы NI
    for group in await orm_get_group_all(await get_session()):
        notification_interval = group.notificationInterval

        # Получить список пользователей этой группы из БД
        group_users = await orm_get_users_by_group(await get_session(), group.id)

        # Пробежаться по дедлайнам в БД
        for post in await orm_get_posts_by_group(await get_session(), group.id):

            # Сравнить дату дедлайна c текущей датой плюс NI
            if(post.deadline is not None):
                deadline = datetime.datetime.strftime(post.deadline, '%d.%m.%Y')
                now_plus_ni = (datetime.datetime.now() + datetime.timedelta(days=notification_interval)).strftime('%d.%m.%Y')

                # Если даты совпадают, то выслать оповещение о дедлайне группе
                if(deadline == now_plus_ni):
                    for group_user in group_users:
                        await bot.send_message(chat_id = group_user.telegram_id, text=("Напоминание!\n\n" + post.text))
            # for group_user in group_users:
            #     await bot.send_message(chat_id = group_user.telegram_id635260494, text=post.text)
    

async def schedule_bot(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.start()

    trigger = CronTrigger(
        year="*", month="*", day="*", hour="11", minute="0", second="0"
        # year="*", month="*", day="*", hour="*", minute="*", second="5"
    )
    scheduler.add_job(
        notif,
        trigger=trigger,
        args=[bot],
        name="daily reminder",
    )

async def get_session():
    session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    session = session_maker()
    return session