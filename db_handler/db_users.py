# from sqlalchemy.orm import relationship
from decouple import config
from sqlalchemy import TIMESTAMP, Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем асинхронный движок для подключения к базе данных
engine = create_async_engine(config('ASYNC_PG_LINK'), echo=True)
# Создаем асинхронную сессию
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
# Определяем базовый класс для моделей
Base = declarative_base()


async def create(model_name, data):
    async with AsyncSessionLocal() as session:
        new_element = model_name(**data)
        session.add(new_element)
        await session.commit()
        return new_element


async def update(model_name, id, data):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.query(model_name).filter(
                model_name.telegram_id == id).update(
                    **data)
        await session.commit()


async def get_element(model_name, id):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(model_name).filter_by(user_telegram_id=id))
        return result.scalar()


async def delete(model_name, id, url):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(model_name).filter_by(user_telegram_id=id, url=url))
            obj = result.scalar()
            if obj:
                await session.delete(obj)
                await session.commit()  # Сохраняем изменения в базе данных
                return True  # Успешно удалено
            return False


async def get_all_elements(model_name):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(model_name))
            return result.scalars()


async def get_all_elements_for_user(model_name, id):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            results = await session.execute(
                select(model_name).filter_by(
                    user_telegram_id=id))
            return results.scalars().all()


# Таблица пользователя
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer)
    user_login = Column(String, nullable=False)
    full_name = Column(String)
    date_reg = Column(TIMESTAMP)


# Таблица расписания
class Schedule_url(Base):
    __tablename__ = 'schedule_url'

    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(Integer)
    url = Column(String)
    time_zone = Column(String)
    schedule_time = Column(String)
    city = Column(String)


# async def init_db():
#     async with engine.begin() as conn:
#         # Создаем все таблицы
#         await conn.run_sync(Base.metadata.create_all)

# async def drop_user_table():
#     async with engine.begin() as conn:
#         # Удаляем только таблицу 'users'
#         await conn.run_sync(Schedule_url.__table__.create)

# asyncio.run(drop_user_table())
