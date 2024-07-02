from aiogram import Router, types
from aiogram.filters import Command
from filters.chat_types import ChatTypeFilter

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(Command("id"))
async def menu_cmd(message: types.Message):
    """
    Get ID user
    """
    await message.answer(f"Ваш ID: <code>{message.from_user.id}</code>")
