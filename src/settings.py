from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Literal, Sequence
import os
import pathlib

DOTENV = pathlib.Path(os.path.dirname(__file__)).parent / ".env"


class Settings(BaseSettings):
    driver_name: str
    user_name: str
    password: str
    host: str
    port: int
    database: str

    model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")


class AuthEnvConfig(BaseSettings):
    jwt_algorithm: Literal[
        "HS256",
        "HS384",
        "HS512",
        "ES256",
        "ES256K",
        "ES384",
        "ES512",
        "RS256",
        "RS384",
        "RS512",
        "PS256",
        "PS384",
        "PS512",
    ]
    jwt_secret_key: str
    jwt_token_location: Sequence[Literal["headers", "cookies", "json", "query"]]

    model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")
