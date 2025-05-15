from fastapi import APIRouter
from typing import List, Dict
from src.articles.schemas import ArticleSchema

router = APIRouter()

@router.get('/blog')
def get_articles():
    return {'A': 'A'}

@router.post('/blog')
def add_article(article: ArticleSchema) -> ArticleSchema:
    return article
