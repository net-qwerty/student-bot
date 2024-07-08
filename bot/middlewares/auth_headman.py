from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker

from database.orm_query import (
    orm_get_user,
    orm_get_group_atr,
)

from kbds.inline import get_callback_btns

class AuthHeadman(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            
            if await orm_get_group_atr(session, "headmanID", int(event.from_user.id)) != None:
                
                user = await orm_get_user(session, int(event.from_user.id))
                group = await orm_get_group_atr(session, "id", user.group_id)
                
                data['user'] = user
                data['group'] = group
                
                return await handler(event, data)

            
            await event.answer(
                text="Вы не являетесь старостой!",
                reply_markup=get_callback_btns(
                    btns={
                        "Создать группу": "create_group",
                    }
                ),
            )
