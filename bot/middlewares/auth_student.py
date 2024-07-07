from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker

from database.orm_query import (
    orm_add_user,
    orm_delete_user,
    orm_get_user,
)

from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard

class AuthStudent(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            
            print(event)


            user = {
                "telegram_id": int(event.from_user.id),
                "username": event.from_user.username,
                "full_name": event.from_user.full_name,
                # "groupe": "test",
                # "codeName": "test",
            }
            
            
            # if event.callback_query != None:
            #     user = {
            #         "telegram_id": int(event.callback_query.from_user.id),
            #         "username": event.callback_query.from_user.username,
            #         "full_name": event.callback_query.from_user.full_name,
            #         # "groupe": "test",
            #         # "codeName": "test",
            #     }
            
            
            
            # print(await orm_get_user(session, user['telegram_id']))
            
            if await orm_get_user(session, user['telegram_id']) != None:
                
                return await handler(event, data)

            data['user'] = user
            
            await event.answer(
                text="Вы не зарегистрированы!",
                reply_markup=get_callback_btns(
                    btns={
                        "Зарегистрироваться": "registration",
                    }
                ),
            )
            # await event.answer("Вы не зарегистрированы")
            
            

            
