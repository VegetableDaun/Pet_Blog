from pydantic import BaseModel, Field


class ArticleCreate(BaseModel):
    author: str
    title: str
    content: str
    secret_info: str | None = Field(default=None)


class ArticlePublic(BaseModel):
    author: str
    title: str
    content: str


class ArticleUpdate(BaseModel):
    author: str | None = Field(default=None)
    title: str | None = Field(default=None)
    content: str | None = Field(default=None)
