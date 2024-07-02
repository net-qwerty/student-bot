import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from filters.chat_types import ChatTypeFilter
from jinja2 import Environment, FileSystemLoader

from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard

headman_router = Router()
headman_router.message.filter(ChatTypeFilter(["private"]))

env = Environment(loader=FileSystemLoader("bot/templates/"), lstrip_blocks=True)

HEADMAN_KB = get_keyboard(
    "Запись",
    "Семестры",
    "Предметы",
    placeholder="Выберите",
    sizes=(2,),
)

RECORD_KB = get_keyboard(
    "Создать",
    "Добавить",
    "Удалить",
    "Меню админа⏫",
    placeholder="Выберите действие с записями",
    sizes=(2,),
)

SEMESTER_KB = get_keyboard(
    "Создать",
    "Выбрать текущий",
    "Добавить",
    "Удалить",
    "Меню админа⏫",
    placeholder="Выберите действие с семестром",
    sizes=(2,),
)

LESSON_KB = get_keyboard(
    "Создать",
    "Добавить",
    "Удалить предметы",
    "Меню админа⏫",
    placeholder="Выберите действие с предметом",
    sizes=(2,),
)

@headman_router.message(or_f(Command("admin"), (F.text.lower().contains("админ"))))
async def start_main(message: types.Message):
    """
    Main admin
    """
    await message.answer("Главное меню", reply_markup=HEADMAN_KB)


@headman_router.message(or_f(Command("record"),(F.text.lower().contains("запись"))))
async def admin_features(message: types.Message):
    """
    Main record
    """
    await message.answer("Меню управления записями", reply_markup=RECORD_KB)


@headman_router.message(or_f(Command("semestr"),(F.text.lower().contains("семестры"))))
async def admin_features(message: types.Message):
    """
    Main semestr
    """
    await message.answer("Меню управления семестрами", reply_markup=SEMESTER_KB)


@headman_router.message(or_f(Command("lesson"),(F.text.lower().contains("предметы"))))
async def admin_features(message: types.Message):
    """
    Main lesson
    """
    await message.answer("Меню управления предметами", reply_markup=LESSON_KB)
