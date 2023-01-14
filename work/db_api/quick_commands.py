from asyncpg import UniqueViolationError
from work.db_api.db_bot_user import *
from work.db_api.schemas.user import *


async def add_user(id_bd: int, name: str, status_name: str):
    try:
        user = User(id_bd=id_bd, name=name, status_name=status_name)
        await user.create()
    except UniqueViolationError:
        print('База данных не изменена')


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(User.id_bd).gino.scalar()
    return count


async def select_user(id_bd):
    user = await User.query.where(User.id_bd == id_bd).gino.first()
    return user


async def update_user_name(id_bd, new_name):
    user = await select_user(id_bd)
    await user.update(name=new_name).apply()
