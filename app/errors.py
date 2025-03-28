from msgspec import json, Struct
import typing as t
from blacksheep import Application, Content, Request, Response
from essentials.exceptions import (
    AcceptedException,
    ForbiddenException,
    NotImplementedException,
    ObjectNotFound,
    UnauthorizedException,
    EmptyArgumentException,
    ConflictException,
)

from utils.responses import JSON_CONTENT_TYPE


def configure_error_handlers(app: Application) -> None:
    class Res(Struct):
        status: int
        message: str

    async def not_found_handler(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return Response(
            status=404,
            content=Content(
                content_type=JSON_CONTENT_TYPE,
                data=json.encode(
                    Res(status=404, message=str(exception) or "Not found")
                ),
            ),
        )

    async def empty_argument_exception(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return Response(
            status=400,
            content=Content(
                content_type=JSON_CONTENT_TYPE,
                data=json.encode(
                    Res(status=400, message=str(exception) or "Empty Argument")
                ),
            ),
        )

    async def conflict_exception(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return Response(
            status=409,
            content=Content(
                content_type=JSON_CONTENT_TYPE,
                data=json.encode(Res(status=409, message=str(exception) or "Conflict")),
            ),
        )

    async def not_implemented(*args: t.Any) -> Response:
        return Response(
            status=500,
            content=Content(
                content_type=JSON_CONTENT_TYPE,
                data=json.encode(Res(status=500, message="Not implemented")),
            ),
        )

    async def unauthorized(*args: t.Any) -> Response:
        return Response(
            status=401,
            content=Content(
                content_type=JSON_CONTENT_TYPE,
                data=json.encode(Res(status=401, message="Unauthorized")),
            ),
        )

    async def forbidden(*args: t.Any) -> Response:
        return Response(
            status=403,
            content=Content(
                content_type=JSON_CONTENT_TYPE,
                data=json.encode(Res(status=403, message="Forbidden")),
            ),
        )

    async def accepted(*args: t.Any) -> Response:
        return Response(
            status=202,
            content=Content(
                content_type=JSON_CONTENT_TYPE,
                data=json.encode(
                    Res(
                        status=202,
                        message="The operation is accepted, "
                        "but its completion is not guaranteed.",
                    )
                ),
            ),
        )

    app.exceptions_handlers.update(
        {
            ObjectNotFound: not_found_handler,
            NotImplementedException: not_implemented,
            UnauthorizedException: unauthorized,
            ForbiddenException: forbidden,
            AcceptedException: accepted,
            EmptyArgumentException: empty_argument_exception,
            ConflictException: conflict_exception,
        }
    )
