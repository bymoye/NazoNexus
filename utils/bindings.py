from typing import Any, TypeVar

from msgspec import Struct, ValidationError, DecodeError
from msgspec.json import decode as msgspec_decode

from blacksheep.messages import Request
from blacksheep.server.bindings import Binder, BoundValue
from blacksheep.exceptions import BadRequest

SchemaType = TypeVar("SchemaType", bound=Struct)


class FromSchema(BoundValue[SchemaType]): ...


class SchemaBinder(Binder):
    handle = FromSchema

    async def get_value(self, request: Request) -> Any:
        try:
            body = await request.read()
            if not body:
                raise BadRequest("Empty body")
            return msgspec_decode(body, type=self.expected_type)
        except (ValidationError, DecodeError) as e:
            raise BadRequest(f"Invalid payload: {e}") from e
