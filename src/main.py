from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.articles import router as articles_router
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(articles_router)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
