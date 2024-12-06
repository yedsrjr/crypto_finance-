from asyncio import gather
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException

from schemas import (
    DaySummaryList,
    ErrorMessage,
    Message,
    User,
    UserFavoriteAdd,
    UserList,
)
from services import AssetService, FavoriteService, UserService

user_router = APIRouter(prefix='/user')
assets_router = APIRouter(prefix='/assets')


@user_router.post('/create', response_model=Message, responses={HTTPStatus.BAD_REQUEST: {'model': ErrorMessage}})
async def create_user(user: User):
    try:
        await UserService.create_user(name=user.name)
        return {
            'message': 'OK'
        }
    except:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='something went wrong when creating the user'
        )


@user_router.delete('/delete/{user_id}', response_model=Message, responses={HTTPStatus.BAD_REQUEST: {'model': ErrorMessage}})
async def delete_user(user_id: int):
    try:
        await UserService.delete_user(user_id)
        return {
            'message': 'OK'
        }
    except:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='user does not exist'
        )


@user_router.post('/favorite/add', response_model=Message, responses={HTTPStatus.BAD_REQUEST: {'model': ErrorMessage}})
async def user_favorite_add(favorite_add: UserFavoriteAdd):
    try:
        await FavoriteService.add_favorite(
            user_id=favorite_add.user_id,
            symbol=favorite_add.symbol
        )

        return {'message': 'OK'}
    except:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='something went wrong when creating the favorite'
        )


@user_router.delete('/favorite/remove/{user_id}', response_model=Message, responses={HTTPStatus.BAD_REQUEST: {'model': ErrorMessage}})
async def user_favorite_remove(user_id: int, symbol: str):
    try:
        await FavoriteService.remove_favorite(user_id=user_id, symbol=symbol)
        return {'message': 'OK'}
    except:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail='favorite does not exist')


@user_router.get('/list', response_model=List[UserList], responses={400: {'model': ErrorMessage}})
async def user_list():
    try:
        resposta = await UserService.list_user()
        return resposta
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@assets_router.get('/day_summary/{user_id}', response_model=List[DaySummaryList], responses={400: {'model': ErrorMessage}})
async def day_summary(user_id: int):
    try:
        user = await UserService.get_by_id(user_id)
        favorites_symbols = [favorite.symbol for favorite in user.favorites]
        print("FAV", favorites_symbols)
        tasks = [AssetService.day_summary(symbol=symbol) for symbol in favorites_symbols]
        return await gather(*tasks)
    except Exception as error:
        raise HTTPException(400, detail=str(error))
