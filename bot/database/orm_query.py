from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users

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

# async def orm_add_product(session: AsyncSession, data: dict):
#     obj = Product(
#         name=data["name"],
#         description=data["description"],
#         price=float(data["price"]),
#         image=data["image"],
#     )
#     session.add(obj)
#     await session.commit()


# async def orm_get_products(session: AsyncSession):
#     query = select(Product)
#     result = await session.execute(query)
#     return result.scalars().all()


# async def orm_get_product(session: AsyncSession, product_id: int):
#     query = select(Product).where(Product.id == product_id)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_update_product(session: AsyncSession, product_id: int, data):
#     query = update(Product).where(Product.id == product_id).values(
#         name=data["name"],
#         description=data["description"],
#         price=float(data["price"]),
#         image=data["image"],)
#     await session.execute(query)
#     await session.commit()


# async def orm_delete_product(session: AsyncSession, product_id: int):
#     query = delete(Product).where(Product.id == product_id)
#     await session.execute(query)
#     await session.commit()