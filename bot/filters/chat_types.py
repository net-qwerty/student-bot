# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.filters import Filter


class ChatTypeFilter(Filter):
    """
    Filter to determine chat type
    """

    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsStudent(Filter):
    """
    Filter for authorization of a user from the list telegram ID
    """

    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
    
        return message.from_user.id not in bot.headmans_list

class IsHeadman(Filter):
    """
    Filter for authorization of a user from the list telegram ID
    """

    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
    
        return message.from_user.id in bot.headmans_list
