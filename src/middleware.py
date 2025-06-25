from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.settings import CorsEnvConfig

cors_config = CorsEnvConfig()


def register_middleware(app: FastAPI):

    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=cors_config.origins,
        allow_credentials=cors_config.allow_credentials,
        allow_methods=cors_config.allow_methods,
        allow_headers=cors_config.allow_headers,
    )
