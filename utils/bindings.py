from typing import Any, TypeVar

from msgspec import Struct, ValidationError
from msgspec.json import decode as msgspec_decode
from utils.responses import DECODER

from blacksheep import Application, FromJSON
from blacksheep.messages import Request
from blacksheep.server.bindings import Binder, BoundValue
from blacksheep.exceptions import BadRequest

StructType = TypeVar("StructType", bound=Struct)


class FromStruct(BoundValue[StructType]): ...


class StructBinder(Binder):
    handle = FromStruct

    def struct_loads(self, text: str):
        return msgspec_decode(text, type=self.expected_type)

    async def get_value(self, request: Request) -> Any:
        try:
            data = await request.json(loads=self.struct_loads)
            if not isinstance(data, self.expected_type):
                raise BadRequest(f"Invalid payload")
            return data
        except ValidationError as e:
            raise BadRequest(f"Invalid payload: {e}") from e

    # except Exception as e:
    #     raise ValueError(f"Invalid data: {e}") from e
    # return self.expected_type(many=True).load(data)
    # except Exception as e:
    #     raise ValueError(f"Invalid data: {e}") from e
