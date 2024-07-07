import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from filters.chat_types import ChatTypeFilter
from jinja2 import Environment, FileSystemLoader

from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard, AUTH_KB

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

SKIP_KB = get_keyboard(
    ["Отменить","Пропустить"],
    sizes=(2,),
)

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


@headman_router.message(StateFilter(None), F.text == "Информация")
async def headman_information(message: types.Message, state: FSMContext):

    await message.answer("Предметы", reply_markup=SUBJECTS_KB)


@headman_router.message(StateFilter(None), F.text.in_(set(subjects)))
async def headman_subjects(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(AddOrChangePost.subject)
    data = await state.get_data()
    print(data)
    await message.answer("Введите текст поста", reply_markup=types.ReplyKeyboardRemove())


# Ловим данные для состояния subject и потом меняем состояние на text
@headman_router.message(AddOrChangePost.subject, F.text)
async def add_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(AddOrChangePost.text)
    data = await state.get_data()
    print(data)
    await message.answer("Введите дедлайн в формате: 01.01.2001")

# Ловим данные для состояние text и потом меняем состояние на deadline
@headman_router.message(AddOrChangePost.text, F.text)
async def add_deadline(message: types.Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await state.set_state(AddOrChangePost.deadline)
    data = await state.get_data() 
    await message.answer(f"Вы ввели:\n{data["subject"]}\n{data["text"]}\n{data["deadline"]}", reply_markup=HEADMAN_KB)

    await state.clear()