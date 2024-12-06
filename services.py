
from aiohttp import ClientSession
from sqlalchemy import delete
from sqlalchemy.future import select

from database.connection import async_session
from database.models import Favorite, User


class UserService:
    async def create_user(name: str):
        async with async_session() as session:
            session.add(User(name=name))
            await session.commit()

    async def delete_user(user_id: int):
        async with async_session() as session:
            await session.execute(
                delete(User).where(User.id == user_id)
            )
            await session.commit()

    async def list_user():
        async with async_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    async def get_by_id(user_id: int):
        async with async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar()


class FavoriteService:
    async def add_favorite(user_id: int, symbol: str):
        async with async_session() as session:
            session.add(Favorite(user_id=user_id, symbol=symbol))
            await session.commit()

    async def remove_favorite(user_id: int, symbol: str):
        async with async_session() as session:
            await session.execute(delete(Favorite).where(Favorite.user_id == user_id, Favorite.symbol == symbol))
            await session.commit()


class AssetService:
    async def day_summary(symbol: str):
        print("estou aqui")
        url = f'https://api.mercadobitcoin.net/api/v4/tickers?symbols={symbol}'
        async with ClientSession() as session:
            response = await session.get(url)
            data = await response.json()
            retorno = data[0]

        return {
                'high': retorno['high'],
                'low': retorno['low'],
                'pair': retorno['pair']
        }
