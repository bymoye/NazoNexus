import re
import typing as t
from msgspec import Struct, Meta

EmailType = t.Annotated[
    str,
    Meta(
        pattern=r"^(?![._%+-])[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,63}$",
        examples=["a@example.com"],
        description="Email address",
    ),
]

UsernameType = t.Annotated[
    str,
    Meta(
        min_length=1,
        max_length=20,
        pattern=r"^[a-zA-Z][a-zA-Z0-9]*(_[a-zA-Z0-9]+)*(?<![_])$",
    ),
]


class RegisterInput(Struct):
    username: UsernameType
    password: t.Annotated[str, Meta(min_length=6, max_length=128)]
    nickname: str
    email: EmailType
