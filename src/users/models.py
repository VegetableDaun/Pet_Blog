from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Self


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str


class UserLogin(BaseModel):
    username: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    password: str

    @model_validator(mode="after")
    def check_name_filled(self) -> Self:
        if not self.username and not self.email:
            raise ValueError("At least one of Username or Email must be filled.")

        return self


class UserUpdate(BaseModel):
    username: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None)
