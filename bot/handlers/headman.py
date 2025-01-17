import datetime
import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter, IsHeadman
from jinja2 import Environment, FileSystemLoader

from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard, AUTH_KB

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_add_post,
    # orm_get_subject_all
    orm_get_subjects_by_group,
    orm_get_users_by_group
)

headman_router = Router()
# headman_router.message.filter(ChatTypeFilter(["private"]), IsHeadman())
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

SKIP_KB = get_keyboard(
    ["Отменить","Пропустить"],
    sizes=(2,),
)

CANCEL_KB = get_keyboard(
    ["Отменить"],
    sizes=(2,),
)

class AddOrChangePost(StatesGroup):
    # Шаги состояний
    text = State()
    deadline = State()
    subject_id = State()
    material = State()
    type = State()

    post_for_change = None

    texts = {
        "AddOrChangePost:text": "Введите текст поста:",
        "AddOrChangePost:deadline": "Введите дедлайн:",
        "AddOrChangePost:material": "Приложиите материал",
    }

@headman_router.message(or_f(Command("headman"), F.text.contains("Староста")))
async def headman_main(message: types.Message):
    await message.answer("Выберите следующий шаг", reply_markup=HEADMAN_KB)

# сборка массива предметов
async def find_subjects(session: AsyncSession, group):
    subjects = []
    # for s in await orm_get_subject_all(session):
    for s in await orm_get_subjects_by_group(session, group.id):
        subjects.append(s.name)
    return subjects  

# ------------------------------------------------------------- FSM 

@headman_router.message(StateFilter(None), or_f(F.text.contains("Информация"), F.text.contains("Материалы"), F.text.contains("Требования")))
async def headman_information(message: types.Message, state: FSMContext, session: AsyncSession, group):
    
    subs = await find_subjects(session, group)
    if (message.text == "Требования"):
        subs.remove("Общее")
   
    SUBJECT_KB = get_keyboard(
        subs + ["Назад"],
        sizes=(2,),
        )
    await state.update_data(type=message.text)
    await state.set_state(AddOrChangePost.type)
    await message.answer("Выберите предмет", reply_markup=SUBJECT_KB)



@headman_router.message(or_f(F.text.contains("Назад"), F.text.contains("Отменить")))
async def back_information(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите следующий шаг", reply_markup=HEADMAN_KB)


@headman_router.message(AddOrChangePost.type, F.text)
async def headman_subjects(message: types.Message, state: FSMContext, session: AsyncSession, group):
    subs = await find_subjects(session, group)
    if (message.text in subs):
        # for s in await orm_get_subject_all(session):
        for s in await orm_get_subjects_by_group(session, group.id):
            if(s.name == message.text):
                await state.update_data(subject_id=s.id)
                await state.set_state(AddOrChangePost.subject_id)
        
        await message.answer("Введите описание", reply_markup=CANCEL_KB)
    else:
        pass



# Ловим данные для состояния subject и потом меняем состояние на text
@headman_router.message(AddOrChangePost.subject_id, F.text)
async def add_text(message: types.Message, state: FSMContext, session: AsyncSession, group):
    await state.update_data(text=message.text)
    data = await state.get_data() 
    print(data["type"])
    if (data["type"] == "Требования"):
        await save_post(message, state, session, group)
    else:
        await state.set_state(AddOrChangePost.text)
        await message.answer("Приложите фото или файл", reply_markup=SKIP_KB)

# Ловим данные для состояния text и потом меняем состояние на material
@headman_router.message(AddOrChangePost.text, or_f(F.photo, F.document, F.text))
async def add_material(message: types.Message, state: FSMContext, session: AsyncSession, group):

    if message.document:
        await state.update_data(material=message.document.file_id)
    elif message.photo:
        await state.update_data(material=message.photo[-1].file_id)
    elif message.text == "Пропустить":
        pass
    else:
        await state.clear()
        await message.answer("Выберите следующий шаг", reply_markup=HEADMAN_KB)
        return
    
    data = await state.get_data() 
    print(data["type"])
    if (data["type"] == "Материалы"):
        await save_post(message, state, session, group)
    else:
        await state.set_state(AddOrChangePost.material)
        await message.answer("Введите дедлайн в формате: 01.01.2001", reply_markup=SKIP_KB)

# Ловим данные для состояния material и потом меняем состояние на deadline
@headman_router.message(AddOrChangePost.material, F.text)
async def add_deadline(message: types.Message, state: FSMContext, session: AsyncSession, group):

    if message.text != "Пропустить":
        await state.update_data(deadline=datetime.datetime.strptime(message.text, '%d.%m.%Y'))
        await state.set_state(AddOrChangePost.deadline)
        await save_post(message, state, session, group)
    elif message.text == "Пропустить":
        await save_post(message, state, session, group)
    else:
        await state.clear()
        await message.answer("Выберите следующий шаг", reply_markup=HEADMAN_KB)
        return


async def save_post(message: types.Message, state: FSMContext, session: AsyncSession, group):
    
    data = await state.get_data() 
    print(data)
    # await message.answer(f"Вы ввели:\n{data["subject"]}\n{data["text"]}\n{data["deadline"]}\n{data["material"]}", reply_markup=HEADMAN_KB)

    try:
        await orm_add_post(session, data)
        await publish_post(message, session, group.id, data)
        
        
        await message.answer(
            f"<strong> Запись добавлена!</strong>",
            reply_markup=HEADMAN_KB
        )
    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к разработчикам",
            reply_markup=HEADMAN_KB,
        )
    await state.clear()

async def publish_post(message: types.Message, session: AsyncSession, group_id: int, post: dict):
    s = f"<i>Новый пост</i>\n\n" + post["text"]
    if('deadline' in post):
        s = s + f"<i>\n\nДедлайн: </i>" + datetime.datetime.strftime(post["deadline"], '%d.%m.%Y')
    group_users = await orm_get_users_by_group(session, group_id)
    for group_user in group_users:
        if('material' in post):
            try:
                await message.bot.send_document(chat_id = group_user.telegram_id, document=post["material"], caption=s)
            except Exception as e:
                await message.bot.send_photo(chat_id = group_user.telegram_id, photo=post["material"], caption=s)
        else:
            await message.bot.send_message(chat_id = group_user.telegram_id, text=s)