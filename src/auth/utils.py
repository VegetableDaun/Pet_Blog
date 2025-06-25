from passlib.context import CryptContext

from authx import RequestToken, AuthX
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_token(token: RequestToken, auth: AuthX) -> None:
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
