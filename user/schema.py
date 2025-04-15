from msgspec import Struct


class LoginInput(Struct):
    username: str
    password: str
