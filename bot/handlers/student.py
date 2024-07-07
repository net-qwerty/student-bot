import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter, IsStudent
from jinja2 import Environment, FileSystemLoader


from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard, AUTH_KB


from middlewares.auth_student import AuthStudent

student_router = Router()
student_router.message.filter(ChatTypeFilter(["private"]))


env = Environment(loader=FileSystemLoader("bot/templates/"), lstrip_blocks=True)

STUDENT_KB = get_keyboard(
    ["Информация",
    "Материалы",
    "Требования",
    "Переключить семестр"],
    placeholder="Выберите",
    sizes=(2,),
)

# STUDENTS_KB = get_keyboard(
#     "Выбрать Записи",
#     "Предметы",
#     placeholder="Выберите",
#     sizes=(2,),
# )


# @student_router.message(or_f((CommandStart()), Command("menu"), (F.text.lower().contains("menu"))))
# async def start_main(message: types.Message):
#     """
#     Main menu
#     """
#     await message.answer("Главное меню", reply_markup=STUDENTS_KB)


@student_router.message(or_f(Command("student"), (F.text.lower().contains("студент"))))
async def student_main(message: types.Message, user):
    """
    Main student
    """
    await message.answer("Меню", reply_markup=STUDENT_KB)
