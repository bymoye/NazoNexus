from __future__ import annotations
import typing as t
import uuid_utils.compat as uuid
from enum import Enum
from piccolo.columns.defaults import Default
from piccolo.columns import UUID as PiccoloUUID


class UUID7(Default):
    @property
    def postgres(self) -> str:
        return "uuid_generate_v7()"

    @property
    def cockroach(self) -> str:
        return self.postgres

    @property
    def sqlite(self) -> str:
        return "''"

    def python(self) -> uuid.UUID:
        return uuid.uuid7()


UUIDv7Arg = t.Union[
    UUID7,
    uuid.UUID,
    str,
    Enum,
    None,
    t.Callable[[], uuid.UUID],
]


class UUID(PiccoloUUID):
    value_type = uuid.UUID

    def __init__(self, default: UUIDv7Arg = UUID7(), **kwargs: t.Any) -> None:
        if default is UUID7:
            default = UUID7()

        self._validate_default(default, UUIDv7Arg.__args__)  # type: ignore

        if default == uuid.uuid7:
            default = UUID7()

        if isinstance(default, str):
            try:
                default = uuid.UUID(default)
            except ValueError as e:
                raise ValueError(
                    "The default is a string, but not a valid uuid."
                ) from e

        self.default = default
        kwargs.update({"default": default})
        super().__init__(**kwargs)

    @property
    def column_type(self) -> str:
        return "UUID"
