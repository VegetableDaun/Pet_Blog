from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from src.database import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.users.schemas import UserSchema


class ArticleSchema(BaseModel):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()

    release_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    secret_info: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserSchema"] = Relationship(
        back_populates="articles",
        lazy="selectin",
    )
