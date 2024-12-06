import asyncio
from asyncio import run

from models import Base

from database.connection import engine

# Configura um Event Loop compatível com o Windows
if __name__ == "__main__" and hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def create_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    run(create_database())
