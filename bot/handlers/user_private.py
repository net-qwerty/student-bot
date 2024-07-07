from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter

from kbds.reply import get_keyboard, AUTH_KB


from database.orm_query import (
    orm_add_user,
    orm_delete_user,
    orm_get_user,
    orm_get_code_name,
)


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

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


class RegistrationStudent(StatesGroup):
    code_name = State()
    callback = State()

STUDENT_KB = get_keyboard(
    ["Информация",
    "Материалы",
    "Требования",
    "Переключить семестр"],
    placeholder="Выберите",
    sizes=(2,),
)

@user_private_router.callback_query(StateFilter(None), F.data.startswith("registration"))
async def registration_student(callback: types.CallbackQuery, state: FSMContext):
    """
    Регистрация студента
    
    """
    await callback.message.answer(
        "Введите кодовое слово", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationStudent.code_name)

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

@user_private_router.message(RegistrationStudent.code_name, F.text)
async def add_name(message: types.Message, state: FSMContext, session):
    await state.update_data(code_name=message.text)
    data = await state.get_data()
    
    print(data)

    if await orm_get_code_name(session, data['code_name']) == None:
        await message.answer("Кодовое слово не верно. Введите другое кодовое слово")
        return

    user = {
                "telegram_id": int(message.from_user.id),
                "username": message.from_user.username,
                "full_name": message.from_user.full_name,
                "groupe": "test",
                "codeName": data["code_name"],
            }
    
    # user["codeName"] = data["code_name"]
    
    # user["groupe"] = "test"

    await orm_add_user(session, user)

    await message.answer(str(data))    
    await message.answer("Вы зарегистрированы!", reply_markup=AUTH_KB)
    await state.clear()
