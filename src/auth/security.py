from src.settings import AuthEnvConfig
from authx import AuthX, AuthXConfig

settings = AuthEnvConfig()

config = AuthXConfig(
    JWT_ALGORITHM=settings.jwt_algorithm,
    JWT_SECRET_KEY=settings.jwt_secret_key,
    JWT_TOKEN_LOCATION=settings.jwt_token_location,
)

security = AuthX(config=config)
