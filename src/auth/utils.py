from passlib.context import CryptContext

from authx import RequestToken, AuthX
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_token(token: RequestToken, auth: AuthX) -> None:
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
