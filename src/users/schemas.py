from sqlalchemy.orm import Mapped, mapped_column, Relationship
from src.database import BaseModel

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.articles.schemas import ArticleSchema


class UserSchema(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    articles: Mapped[List["ArticleSchema"] | None] = Relationship(
        back_populates="user", lazy="selectin"
    )
