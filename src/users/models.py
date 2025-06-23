from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Self


class UserCreate(BaseModel):
    username: str = Field(max_length=16)
    email: EmailStr = Field(max_length=32)
    password: str = Field(max_length=32)


class UserPublic(BaseModel):
    username: str = Field(max_length=16)


class UserLogin(BaseModel):
    username: str | None = Field(default=None, max_length=16)
    email: EmailStr | None = Field(default=None, max_length=32)
    password: str = Field(max_length=32)

    @model_validator(mode="after")
    def check_name_filled(self) -> Self:
        if not self.username and not self.email:
            raise ValueError("At least one of Username or Email must be filled.")

        return self


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, max_length=16)
    email: EmailStr | None = Field(default=None, max_length=32)
    password: str | None = Field(default=None, max_length=32)
