import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from filters.chat_types import ChatTypeFilter
from jinja2 import Environment, FileSystemLoader

from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard

headman_router = Router()
headman_router.message.filter(ChatTypeFilter(["private"]))

env = Environment(loader=FileSystemLoader("bot/templates/"), lstrip_blocks=True)

HEADMAN_KB = get_keyboard(
    ["Информация",
    "Материалы",
    "Требования",
    "Настройки",
    "Переключить семестр"],
    sizes=(2,),
)

# список будет собираться динамически
subjects  = ["АБД",
    "ИКСС",
    "МПиС",
    "Питон"]
    
    
SUBJECTS_KB = get_keyboard(
    ["Общее"] + subjects + ["Назад"],
    sizes=(2,),
)

# HEADMAN_KB = get_keyboard(
#     "Запись",
#     "Семестры",
#     "Предметы",
#     placeholder="Выберите",
#     sizes=(2,),
# )

# RECORD_KB = get_keyboard(
#     "Создать",
#     "Добавить",
#     "Удалить",
#     "Меню админа⏫",
#     placeholder="Выберите действие с записями",
#     sizes=(2,),
# )

# SEMESTER_KB = get_keyboard(
#     "Создать",
#     "Выбрать текущий",
#     "Добавить",
#     "Удалить",
#     "Меню админа⏫",
#     placeholder="Выберите действие с семестром",
#     sizes=(2,),
# )

# LESSON_KB = get_keyboard(
#     "Создать",
#     "Добавить",
#     "Удалить предметы",
#     "Меню админа⏫",
#     placeholder="Выберите действие с предметом",
#     sizes=(2,),
# )

# @headman_router.message(or_f(Command("admin"), (F.text.lower().contains("админ"))))
# async def start_main(message: types.Message):
#     """
#     Main admin
#     """
#     await message.answer("Главное меню", reply_markup=HEADMAN_KB)


# @headman_router.message(or_f(Command("record"),(F.text.lower().contains("запись"))))
# async def admin_features(message: types.Message):
#     """
#     Main record
#     """
#     await message.answer("Меню управления записями", reply_markup=RECORD_KB)


# @headman_router.message(or_f(Command("semestr"),(F.text.lower().contains("семестры"))))
# async def admin_features(message: types.Message):
#     """
#     Main semestr
#     """
#     await message.answer("Меню управления семестрами", reply_markup=SEMESTER_KB)


# @headman_router.message(or_f(Command("lesson"),(F.text.lower().contains("предметы"))))
# async def admin_features(message: types.Message):
#     """
#     Main lesson
#     """
#     await message.answer("Меню управления предметами", reply_markup=LESSON_KB)
class AddOrChangePost(StatesGroup):
    # Шаги состояний
    text = State()
    deadline = State()
    subject_id = State()
    subject = State()
    material = State()

    post_for_change = None

    # texts = {
    #     "AddProduct:name": "Введите название заново:",
    #     "AddProduct:description": "Введите описание заново:",
    #     "AddProduct:category": "Выберите категорию  заново ⬆️",
    #     "AddProduct:price": "Введите стоимость заново:",
    #     "AddProduct:image": "Этот стейт последний, поэтому...",
    # }

    texts = {
        "AddOrChangePost:text": "Введите текст поста:",
        "AddOrChangePost:deadline": "Введите дедлайн:",
        "AddOrChangePost:material": "Приложиите материал",
    }

@headman_router.message(or_f(Command("headman"), (F.text.lower().contains("староста"))))
async def headman_main(message: types.Message):
    """
    Main admin
    """
    await message.answer("Меню", reply_markup=HEADMAN_KB)


# Становимся в состояние ожидания ввода text
# @headman_router.message(StateFilter(None), F.text == "Добавить товар")
# async def add_post(message: types.Message, state: FSMContext):
#     await message.answer(
#         "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
#     )
#     await state.set_state(AddOrChangePost.name)



@headman_router.message(StateFilter(None), F.text == "Информация")
async def headman_subject(message: types.Message, state: FSMContext):

    await message.answer("Предметы", reply_markup=SUBJECTS_KB)


@headman_router.message()
async def echo(message: types.Message):
    if message.text in subjects:
        await message.answer("Текст сообщения соответствует категории")
    else:
        pass