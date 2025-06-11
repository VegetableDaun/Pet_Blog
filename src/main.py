from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.articles import router as articles_router
from src.users import router as users_router
from src.blog import router as blogs_router
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(articles_router)
app.include_router(users_router)
app.include_router(blogs_router)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
