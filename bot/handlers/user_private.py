from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, or_f
from filters.chat_types import ChatTypeFilter
from kbds.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

AUTH_KB = get_keyboard(
    ["Староста",
    "Студент"],
    placeholder="Выберите роль",
    sizes=(2,),
)

@user_private_router.message(or_f((CommandStart()), Command("start"), (F.text.lower().contains("start"))))
async def start_main(message: types.Message):
    """
    Auth menu
    """
    await message.answer("Привет!\nЭтот бот предназначен для помощи в учебе.\nВыберите роль, под которой хотите авторизоваться", reply_markup=AUTH_KB)

# @user_private_router.message(Command("id"))
# async def menu_cmd(message: types.Message):
#     """
#     Get ID user
#     """
#     await message.answer(f"Ваш ID: <code>{message.from_user.id}</code>")
