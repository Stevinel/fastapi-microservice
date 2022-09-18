from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class LoginMessage(BaseModel):
    access_token: str


class UserMessage(BaseModel):
    user: str


class StatusMessage(BaseModel):
    status: str
    id: Optional[int] = None
    success: Optional[bool] = None


class ErrorMessage(BaseModel):
    status: str
    message: str


class PlayerItem(BaseModel):
    name: str
    email: str


class GameItem(BaseModel):
    name: str


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"