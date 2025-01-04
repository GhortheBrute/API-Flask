from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import db


class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})'
