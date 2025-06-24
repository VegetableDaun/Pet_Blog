import uvicorn

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.articles import router as articles_router
from src.users import router as users_router
from src.pages import router as blogs_router
from src.pages.errors.exception_handlers import (
    unauthorized_handler,
    not_found_handler,
    forbidden_handler,
)
from src.auth.security import security

# Creation of FastApi App
app = FastAPI()

# Exception Handlers
app.add_exception_handler(status.HTTP_401_UNAUTHORIZED, unauthorized_handler)
app.add_exception_handler(status.HTTP_403_FORBIDDEN, forbidden_handler)
app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)

# Exception Handlers for Errors which happened after problems with access and refresh tokens
security.handle_errors(app)

# CORS Middleware
origins = ["http://localhost:8000/", "https://localhost:8000/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(articles_router)
app.include_router(users_router)
app.include_router(blogs_router)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
