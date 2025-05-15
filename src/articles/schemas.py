from pydantic import BaseModel


class ArticleSchema(BaseModel):
    author: str
    title: str
    content: str
