from __future__ import annotations
import typing as t
from enum import Enum
import uuid_utils as uuid
from uuid import UUID as DefaultUUID
from typing import overload
from piccolo.table import Table
from piccolo.columns.defaults import Default
from piccolo.columns.base import Column


class UUID7(Default):
    @property
    def postgres(self):
        return "uuid_generate_v7()"

    @property
    def cockroach(self):
        return self.postgres

    @property
    def sqlite(self):
        return "''"

    def python(self):
        return uuid.uuid7()


UUIDv7Arg = t.Union[
    UUID7,
    uuid.UUID,
    DefaultUUID,
    str,
    Enum,
    None,
    t.Callable[[], uuid.UUID],
    t.Callable[[], DefaultUUID],
]


class UUID(Column):
    value_type = DefaultUUID

    def __init__(self, default: UUIDv7Arg = UUID7(), **kwargs) -> None:
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
    def column_type(self):
        return "UUID"

    @overload
    def __get__(self, obj: Table, objtype=None) -> t.Union[uuid.UUID, DefaultUUID]: ...

    @overload
    def __get__(self, obj: None, objtype=None) -> UUID: ...

    def __get__(self, obj, objtype=None):
        return obj.__dict__[self._meta.name] if obj else self

    def __set__(self, obj, value: t.Union[uuid.UUID, DefaultUUID, None]):
        obj.__dict__[self._meta.name] = value

    @property
    def python_type(self):
        return uuid.UUID

    @property
    def column_Type(self) -> str:
        return "UUID"
