from pydantic import BaseModel, Field


class ArticleCreate(BaseModel):
    title: str = Field(max_length=80)
    content: str = Field(max_length=280)
    secret_info: str | None = Field(default=None, max_length=80)


class ArticlePublic(BaseModel):
    title: str = Field(max_length=80)
    content: str = Field(max_length=280)


class ArticleUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=80)
    content: str | None = Field(default=None, max_length=280)
