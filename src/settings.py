from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import pathlib

DOTENV = pathlib.Path(os.path.dirname(__file__)).parent / '.env'


class Settings(BaseSettings):
    driver_name: str
    user_name: str
    password: str
    host: str
    port: int
    database: str

    model_config = SettingsConfigDict(
        env_file=DOTENV,
    )
