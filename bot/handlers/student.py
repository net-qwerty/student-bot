import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from filters.chat_types import ChatTypeFilter, IsStudent
from jinja2 import Environment, FileSystemLoader

from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard

student_router = Router()
student_router.message.filter(ChatTypeFilter(["private"]))


env = Environment(loader=FileSystemLoader("bot/templates/"), lstrip_blocks=True)

STUDENTS_KB = get_keyboard(
    "Выбрать Записи",
    "Предметы",
    placeholder="Выберите",
    sizes=(2,),
)

@student_router.message(or_f((CommandStart()), Command("menu"), (F.text.lower().contains("menu"))))
async def start_main(message: types.Message):
    """
    Main menu
    """
    await message.answer("Главное меню", reply_markup=STUDENTS_KB)


