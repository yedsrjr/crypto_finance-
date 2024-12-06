from typing import List

from pydantic import BaseModel, ConfigDict

# from sqlalchemy import Ser


class User(BaseModel):
    name: str


class UserFavoriteAdd(BaseModel):
    user_id: int
    symbol: str


class Favorite(BaseModel):
    id: int
    symbol: str
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    id: int
    name: str
    favorites: List[Favorite]
    model_config = ConfigDict(from_attributes=True)


class DaySummaryList(BaseModel):
    high: float
    low: float
    pair: str


class Message(BaseModel):
    message: str


class ErrorMessage(BaseModel):
    detail: str
