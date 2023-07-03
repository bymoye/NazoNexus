import orjson
import typing as t
from blacksheep import Application, Content, Request, Response
from essentials.exceptions import (
    AcceptedException,
    ForbiddenException,
    NotImplementedException,
    ObjectNotFound,
    UnauthorizedException,
)

from utils.responses import JSON_CONTENT_TYPE


def configure_error_handlers(app: Application) -> None:
    async def not_found_handler(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return Response(
            404,
            content=Content(
                JSON_CONTENT_TYPE,
                orjson.dumps({"status": 404, "message": str(exception) or "Not found"}),
            ),
        )

    async def not_implemented(*args: t.Any) -> Response:
        return Response(
            500,
            content=Content(
                JSON_CONTENT_TYPE,
                orjson.dumps({"status": 500, "message": "Not implemented"}),
            ),
        )

    async def unauthorized(*args: t.Any) -> Response:
        return Response(
            401,
            content=Content(
                JSON_CONTENT_TYPE,
                orjson.dumps({"status": 401, "message": "Unauthorized"}),
            ),
        )

    async def forbidden(*args: t.Any) -> Response:
        return Response(
            403,
            content=Content(
                JSON_CONTENT_TYPE, orjson.dumps({"status": 403, "message": "Forbidden"})
            ),
        )

    async def accepted(*args: t.Any) -> Response:
        return Response(
            202,
            content=Content(
                JSON_CONTENT_TYPE, orjson.dumps({"status": 202, "message": "Accepted"})
            ),
        )

    app.exceptions_handlers.update(
        {
            ObjectNotFound: not_found_handler,
            NotImplementedException: not_implemented,
            UnauthorizedException: unauthorized,
            ForbiddenException: forbidden,
            AcceptedException: accepted,
        }
    )
