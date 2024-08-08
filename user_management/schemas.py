from pydantic import BaseModel


class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access: str
    refresh: str
