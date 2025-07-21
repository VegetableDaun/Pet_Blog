from sqlalchemy.orm import Mapped, mapped_column, Relationship
from src.database import BaseModel
from sqlalchemy import String, CheckConstraint

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.articles.schemas import ArticleSchema


class UserSchema(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(16), unique=True)
    email: Mapped[str] = mapped_column(
        String(32),
        CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'"),
        unique=True,
    )
    password: Mapped[str] = mapped_column(String(72))

    articles: Mapped[List["ArticleSchema"] | None] = Relationship(
        back_populates="user", lazy="selectin"
    )
