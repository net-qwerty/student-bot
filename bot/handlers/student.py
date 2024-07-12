import asyncio
import settings
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter, IsStudent
from jinja2 import Environment, FileSystemLoader


from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard, AUTH_KB

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_get_subjects_by_group,
    orm_get_posts_by_group
)


student_router = Router()
# student_router.message.filter(ChatTypeFilter(["private"]), IsStudent())
student_router.message.filter(ChatTypeFilter(["private"]))


env = Environment(loader=FileSystemLoader("bot/templates/"), lstrip_blocks=True)

STUDENT_KB = get_keyboard(
    ["информация",
    "материалы",
    "требования",
    "переключить семестр"],
    placeholder="Выберите",
    sizes=(2,),
)

class ViewPost(StatesGroup):
    # Шаги состояний
    subject_id = State()
    type = State()

# STUDENTS_KB = get_keyboard(
#     "Выбрать Записи",
#     "Предметы",
#     placeholder="Выберите",
#     sizes=(2,),
# )


# @student_router.message(or_f((CommandStart()), Command("menu"), (F.text.contains("menu"))))
# async def start_main(message: types.Message):
#     """
#     Main menu
#     """
#     await message.answer("Главное меню", reply_markup=STUDENTS_KB)


@student_router.message(or_f(Command("student"), (F.text.contains("Студент"))))
async def student_main(message: types.Message, user, group):
    """
    Main student
    """
    await message.answer(f"Пользователь @{user.username} - {user.full_name}\nТекущий семестр: {group.currentSemester}")
    await message.answer("Меню", reply_markup=STUDENT_KB)


# сборка массива предметов
async def find_subjects(session: AsyncSession, group):
    subjects = []
    for s in await orm_get_subjects_by_group(session, group.id):
        subjects.append(s.name)
    return subjects

# ------------------------------------------------------------- FSM 

@student_router.message(StateFilter(None), or_f(F.text.contains("информация"), F.text.contains("материалы"), F.text.contains("требования")))
async def student_information(message: types.Message, state: FSMContext, session: AsyncSession, group):
    
    subs = await find_subjects(session, group)
    if (message.text == "требования"):
        subs.remove("Общее")
   
    SUBJECT_KB = get_keyboard(
        subs + ["назад"],
        sizes=(2,),
        )
    await state.update_data(type=message.text)
    await state.set_state(ViewPost.type)
    await message.answer("Выберите предмет", reply_markup=SUBJECT_KB)


@student_router.message(or_f(F.text.contains("назад"), F.text.contains("отменить")))
async def back_information(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите следующий шаг", reply_markup=STUDENT_KB)


@student_router.message(ViewPost.type, F.text)
async def student_subjects(message: types.Message, state: FSMContext, session: AsyncSession, group):
    subs = await find_subjects(session, group)
    if (message.text in subs):
        for s in await orm_get_subjects_by_group(session, group.id):
            if(s.name == message.text):
                await state.update_data(subject_id=s.id)
                await state.set_state(ViewPost.subject_id)
        
        await get_posts(message, state, session, group.id)
        
    else:
        pass

async def get_posts(message: types.Message, state: FSMContext, session: AsyncSession, group_id: int):
    
    data = await state.get_data() 
    try:
        i=0
        for post in await orm_get_posts_by_group(session, group_id):
            if ((data["type"] == "требования") & (post.type == "Требования") & (post.subject_id == data["subject_id"])):
                i=+1
                await message.answer(f"{post.text}", reply_markup=STUDENT_KB)
            elif ((data["type"] == "материалы") & (post.type == "Материалы") & (post.subject_id == data["subject_id"])):
                if (post.material is not None):

                    try:
                        await message.answer_photo(post.material, caption=f"{post.text}\n", reply_markup=STUDENT_KB)
                        i=+1
                    except Exception as e:
                        await message.answer_document(post.material, caption=f"{post.text}\n", reply_markup=STUDENT_KB)
                        i=+1
                else:
                    i=+1
                    await message.answer(f"{post.text}", reply_markup=STUDENT_KB)
            elif ((data["type"] == "информация") & (post.type == "Информация") & (post.subject_id == data["subject_id"])):
                if (post.material is not None):
                        if (post.deadline is not None):
                            try:
                                await message.answer_photo(post.material, caption=f"{post.text}\n{post.deadline}", reply_markup=STUDENT_KB)
                                i=+1
                            except Exception as e:
                                await message.answer_document(post.material, caption=f"{post.text}\n{post.deadline}", reply_markup=STUDENT_KB)
                                i=+1
                        else:
                            try:
                                await message.answer_photo(post.material, caption=f"{post.text}\n", reply_markup=STUDENT_KB)
                                i=+1
                            except Exception as e:
                                await message.answer_document(post.material, caption=f"{post.text}\n", reply_markup=STUDENT_KB)
                                i=+1
                else:
                    if (post.deadline is not None):
                        i=+1
                        await message.answer(f"{post.text}\n{post.deadline}", reply_markup=STUDENT_KB)
                    else:
                        i=+1
                        await message.answer(f"{post.text}", reply_markup=STUDENT_KB)   
            else:
                pass
        if (i==0):
            await message.answer("Записи не найдены", reply_markup=STUDENT_KB)

    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к разработчикам",
            reply_markup=STUDENT_KB,
        )
    await state.clear()


