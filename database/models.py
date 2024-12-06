from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    favorites = relationship('Favorite', backref='user', lazy='subquery')
    # favorites= 'teste1'


class Favorite(Base):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
