from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.articles import router as articles_router
from src.users import router as users_router
from src.pages import router as blogs_router
import uvicorn

app = FastAPI()

# origins = ["http://localhost:8000/", "https://localhost:8000/"]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(articles_router)
app.include_router(users_router)
app.include_router(blogs_router)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
