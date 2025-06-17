from authx import RequestToken, AuthX
from fastapi import HTTPException


def check_token(token: RequestToken, auth: AuthX) -> None:
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
