import uvicorn
import pathlib
import os

from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from authx.exceptions import MissingTokenError, TokenRequiredError

from src.articles import router as articles_router
from src.users import router as users_router
from src.pages import router as blogs_router
from src.pages.errors.exception_handlers import (
    unauthorized_handler,
    not_found_handler,
    forbidden_handler,
)
from src.auth.security import security
from src.middleware import register_middleware

# Creation of FastApi App
app = FastAPI()

# Exception Handlers
app.add_exception_handler(status.HTTP_401_UNAUTHORIZED, unauthorized_handler)
app.add_exception_handler(status.HTTP_403_FORBIDDEN, forbidden_handler)
app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)

# Exception Handlers for Errors which happened after problems with access and refresh tokens
security.handle_errors(app)
app.add_exception_handler(MissingTokenError, unauthorized_handler)
app.add_exception_handler(TokenRequiredError, unauthorized_handler)

# Register Middleware
register_middleware(app=app)

# Static Files
# static_path = pathlib.Path(__file__).parent
static_path = pathlib.Path(os.path.dirname(__file__)).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Routers
app.include_router(articles_router)
app.include_router(users_router)
app.include_router(blogs_router)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
