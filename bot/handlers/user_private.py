from aiogram import F, Router, types, Bot
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter

from kbds.reply import get_keyboard, AUTH_KB


from database.orm_query import (
    orm_add_user,
    orm_get_user,
    orm_get_group_atr,
    orm_add_group,
    orm_add_semestr,
    orm_add_subject,
    orm_get_semestr_name,
    orm_get_group_all
)


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

CANCEL_KB=get_keyboard(["Отмена",], placeholder="Выберите", sizes=(2,),)


@user_private_router.message(Command("chat_id"))
async def menu_cmd(message: types.Message):
    """
    Get Chat ID user
    """
    await message.answer(f"Ваш ChatID: <code>{message.chat.id}</code>")


@user_private_router.message(or_f((CommandStart()), Command("start"), (F.text.lower().contains("start"))))
async def start_main(message: types.Message, bot: Bot, session: AsyncSession):
    """
    Auth menu
    """
    groups = await orm_get_group_all(session)

    headmans_list = [
        group.headmanID
        for group in groups
    ]

    bot.headmans_list = headmans_list
    await message.answer("Привет!\nЭтот бот предназначен для помощи в учебе.\nВыберите роль, под которой хотите авторизоваться", reply_markup=AUTH_KB)

class RegistrationStudent(StatesGroup):
    code_name_group = State()
    callback = State()

@user_private_router.callback_query(StateFilter(None), F.data.startswith("registration_student"))
async def registration_student(callback: types.CallbackQuery, state: FSMContext):
    """
    Регистрация студента
    
    """
    await callback.message.answer(
        "Введите кодовое слово", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationStudent.code_name_group)

#Хендлер отмены и сброса состояния должен быть всегда именно здесь,
#после того как только встали в состояние номер 1 (элементарная очередность фильтров)
@user_private_router.message(StateFilter('*'), Command("отмена"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=AUTH_KB)

@user_private_router.message(RegistrationStudent.code_name_group, F.text)
async def add_name(message: types.Message, state: FSMContext, session):
    await state.update_data(code_name_group=message.text)
    data = await state.get_data()
    
    if await orm_get_group_atr(session, "codeName", data['code_name_group']) == None:
        await message.answer("Кодовое слово не верно. Введите другое кодовое слово")
        return
    
    
    group = await orm_get_group_atr(session, "codeName", data['code_name_group'])

    user = {
                "telegram_id": int(message.from_user.id),
                "username": message.from_user.username,
                "full_name": message.from_user.full_name,
                "group_id": group.id,
            }

    await orm_add_user(session, user)

    await message.answer(str(data))    
    await message.answer("Вы зарегистрированы!", reply_markup=AUTH_KB)
    await state.clear()


# Создание группы

class CreateGroup(StatesGroup):
    name_group = State()
    code_group = State()
    semestr_group = State()
    notification_interval = State()
    subjects_group = State()
    
    callback = State()

@user_private_router.message(StateFilter(None), Command("create_group"))
async def registration_student(message: types.Message, state: FSMContext, session: AsyncSession):
    """
    Регистрация студента и создание группы
    """
    await message.answer(
        "Введите номер группы", reply_markup=types.ReplyKeyboardRemove()
    )

    await state.set_state(CreateGroup.name_group)

#Хендлер отмены и сброса состояния должен быть всегда именно здесь,
#после того как только встали в состояние номер 1 (элементарная очередность фильтров)
@user_private_router.message(StateFilter('*'), Command("отмен"))
@user_private_router.message(StateFilter('*'), F.text.casefold() == "отмен")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=AUTH_KB)


@user_private_router.message(CreateGroup.name_group, F.text)
async def add_name(message: types.Message, state: FSMContext, session: AsyncSession):
    """
    Создание группы. Задаём номер, запрашиваем имя группы.
    """
    
    if await orm_get_group_atr(session, "name", message.text) != None:
        await message.answer("Группа с таким именем существует. Введите другое имя группы")
        return

    await state.update_data(name_group=message.text)

    await message.answer("Введите код для вашей группы",reply_markup=CANCEL_KB)

    await state.set_state(CreateGroup.code_group)


@user_private_router.message(CreateGroup.code_group, F.text)
async def add_name(message: types.Message, state: FSMContext, session: AsyncSession):
    """
    Создание группы. Задаём код группы, запрашиваем текущий семестр.
    """
    if await orm_get_group_atr(session, "codeName", message.text) != None:
        await message.answer("Группа с таким кодом существует. Введите другой код группы")
        return
    
    await state.update_data(code_name_group=message.text)

    await message.answer("Номер текущего семестра", reply_markup=CANCEL_KB)

    await state.set_state(CreateGroup.semestr_group)


@user_private_router.message(CreateGroup.semestr_group, F.text)
async def add_name(message: types.Message, state: FSMContext):
    """
    Создание группы. Задаём текущий семестр, запрашиваем интервал уведомлений.
    """
    await state.update_data(semestr_group=message.text)

    await message.answer("Введите интервал уведомлений (в днях)", reply_markup=CANCEL_KB)

    await state.set_state(CreateGroup.notification_interval)


@user_private_router.message(CreateGroup.notification_interval, F.text)
async def add_name(message: types.Message, state: FSMContext):
    """
    Создание группы. Задаём интервал уведомлений, запрашиваем предметы.
    """
    await state.update_data(notification_interval=message.text)
    await state.update_data(subjects_group=[])

    await message.answer("Введите название предметов по одному или выберите <strong>Пропустить</strong>",
                         reply_markup=get_keyboard(["Пропустить", "Отмена"], placeholder="Выберите", sizes=(2,),))

    await state.set_state(CreateGroup.subjects_group)


@user_private_router.message(CreateGroup.subjects_group, F.text)
async def add_name(message: types.Message, bot: Bot,state: FSMContext, session: AsyncSession):
    """
    Создание группы. Задаём предметы, завершаем FSM.
    """
    data = await state.get_data()

    if not "завершить" in message.text.lower() and not "пропустить" in message.text.lower():
        await message.answer("Введите ещё предмет или нажмите <strong>завершить</strong>", 
                             reply_markup=get_keyboard(["Завершить", "Отмена"], placeholder="Выберите", sizes=(2,),))
        data["subjects_group"].append(message.text)
        return

    # add group
    data_group = {
        "name": data["name_group"],
        "codeName": data["code_name_group"],
        "headmanID": int(message.from_user.id),
        "currentSemester": int(data["semestr_group"]),
        "notificationInterval": int(data["notification_interval"]),
    }

    await orm_add_group(session, data_group)
    
    group = await orm_get_group_atr(session, "codeName", data['code_name_group'])
    
    # add user if not
    if not await orm_get_user(session, int(message.from_user.id)):
        
        user = {
            "telegram_id": int(message.from_user.id),
            "username": message.from_user.username,
            "full_name": message.from_user.full_name,
            "group_id": group.id,
        }
        
        await orm_add_user(session, user)
    
    
    # add semestr
    semestr = {
        "number": int(data["semestr_group"]),
        "group_id": group.id,
        
    }
    
    await orm_add_semestr(session, semestr)

    semestr = await orm_get_semestr_name(session, int(data["semestr_group"]), group.id)

    # add subject

    await orm_add_subject(session, {"name": "Общее", "semestr_id": semestr.id,})

    for subject in data["subjects_group"]:
        subject = {
            "name": subject,
            "semestr_id": semestr.id,
        }
        
        await orm_add_subject(session, subject)
    
    groups = await orm_get_group_all(session)

    headmans_list = [
        group.headmanID
        for group in groups
    ]

    bot.headmans_list = headmans_list
    
    await message.answer("Группа создана!", reply_markup=AUTH_KB)
    await state.clear()
