from sqlalchemy.orm import Mapped, mapped_column
from src.database import BaseModel


class ArticleSchema(BaseModel):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    author: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()


class UserSchema(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
