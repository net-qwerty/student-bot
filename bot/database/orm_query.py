from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Post, Users, Subject, Semestr, Group

async def orm_add_user(session: AsyncSession, data: dict):
    obj = Users(
        telegram_id=data["telegram_id"],
        username=data["username"],
        full_name=data["full_name"],
        groupe=data["groupe"],
        codeName=data["codeName"]
    )
    session.add(obj)
    await session.commit()

async def orm_delete_user(session: AsyncSession, user_id: int):
    query = delete(Users).where(Users.telegram_id == user_id)
    await session.execute(query)
    await session.commit()

async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(Users).where(Users.telegram_id == user_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_code_name(session: AsyncSession, code_name: int):
    query = select(Users).where(Users.codeName == code_name)
    result = await session.execute(query)
    return result.scalar()

# ADD
async def orm_add_post(session: AsyncSession, data: dict):
    obj = Post(
        text=data["text"],
        deadline=data["deadline"],
        subject_id=data["subject_id"],
        subject=data["subject"],
        material=data["material"],
    )
    session.add(obj)
    await session.commit()

async def orm_add_subject(session: AsyncSession, data: dict):
    obj = Subject(
        name=data["name"],
        semestr_id=data["semestr_id"],
        semestr=data["semestr"],
    )
    session.add(obj)
    await session.commit()

async def orm_add_semestr(session: AsyncSession, data: dict):
    obj = Semestr(
        number=data["number"],
        subjects=data["subjects"],
        group_id=data["group_id"],
        group=data["group"],
    )
    session.add(obj)
    await session.commit()

async def orm_add_group(session: AsyncSession, data: dict):
    obj = Group(
        name=data["name"],
        codeName=data["codeName"],
        headmanID=data["headmanID"],
        notificationInterval=data["notificationInterval"],
    )
    session.add(obj)
    await session.commit()



# ADD ALL
async def orm_get_post(session: AsyncSession):
    query = select(Post)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_subject(session: AsyncSession):
    query = select(Subject)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_semestr(session: AsyncSession):
    query = select(Semestr)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_group(session: AsyncSession):
    query = select(Group)
    result = await session.execute(query)
    return result.scalars().all()



# ADD BY ID
async def orm_get_post(session: AsyncSession, post_id: int):
    query = select(Post).where(Post.id == post_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_subject(session: AsyncSession, subject_id: int):
    query = select(Subject).where(Subject.id == subject_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_semestr(session: AsyncSession, semestr_id: int):
    query = select(Semestr).where(Semestr.id == semestr_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_group(session: AsyncSession, group_id: int):
    query = select(Group).where(Group.id == group_id)
    result = await session.execute(query)
    return result.scalar()



# UPDATE
async def orm_update_post(session: AsyncSession, post_id: int, data):
    query = update(Post).where(Post.id == post_id).values(
        text=data["text"],
        deadline=data["deadline"],
        subject_id=data["subject_id"],
        subject=data["subject"],
        material=data["material"],
        )
    await session.execute(query)
    await session.commit()

async def orm_update_subject(session: AsyncSession, subject_id: int, data):
    query = update(Subject).where(Subject.id == subject_id).values(
        name=data["name"],
        semestr_id=data["semestr_id"],
        semestr=data["semestr"],
        )
    await session.execute(query)
    await session.commit()

async def orm_update_semestr(session: AsyncSession, semestr_id: int, data):
    query = update(Semestr).where(Semestr.id == semestr_id).values(
        number=data["number"],
        subjects=data["subjects"],
        group_id=data["group_id"],
        group=data["group"],
        )
    await session.execute(query)
    await session.commit()

async def orm_update_group(session: AsyncSession, group_id: int, data):
    query = update(Group).where(Group.id == group_id).values(
        name=data["name"],
        codeName=data["codeName"],
        headmanID=data["headmanID"],
        notificationInterval=data["notificationInterval"],
        )
    await session.execute(query)
    await session.commit()



# DELETE BY ID
async def orm_delete_post(session: AsyncSession, post_id: int):
    query = delete(Post).where(Post.id == post_id)
    await session.execute(query)
    await session.commit()

async def orm_delete_subject(session: AsyncSession, subject_id: int):
    query = delete(Subject).where(Subject.id == subject_id)
    await session.execute(query)
    await session.commit()

async def orm_delete_semestr(session: AsyncSession, semestr_id: int):
    query = delete(Semestr).where(Semestr.id == semestr_id)
    await session.execute(query)
    await session.commit()

async def orm_delete_group(session: AsyncSession, group_id: int):
    query = delete(Group).where(Group.id == group_id)
    await session.execute(query)
    await session.commit()