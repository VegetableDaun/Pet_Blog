from fastapi import FastAPI
from src.articles import router as articles_router
import uvicorn

app = FastAPI()
app.include_router(articles_router)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
