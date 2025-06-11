from pydantic import BaseModel, Field


class ArticleCreate(BaseModel):
    title: str
    content: str
    secret_info: str | None = Field(default=None)


class ArticlePublic(BaseModel):
    title: str
    content: str


class ArticleUpdate(BaseModel):
    title: str | None = Field(default=None)
    content: str | None = Field(default=None)
