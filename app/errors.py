import typing as t
from blacksheep import Application, Request, Response
from essentials.exceptions import (
    AcceptedException,
    ForbiddenException,
    NotImplementedException,
    ObjectNotFound,
    UnauthorizedException,
    EmptyArgumentException,
    ConflictException,
)

from utils.responses import jsonify, StatusCode, ApiResponse


def configure_error_handlers(app: Application) -> None:

    async def not_found_handler(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.PAGE_NOT_FOUND,
                data=None,
                message=str(exception) or "Not found",
            ),
            status=404,
        )

    async def empty_argument_exception(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.INVALID_PARAMS,
                data=None,
                message=str(exception) or "Empty Argument",
            ),
            status=400,
        )

    async def conflict_exception(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.DATA_CONFLICT,
                data=None,
                message=str(exception) or "Conflict",
            ),
            status=409,
        )

    async def not_implemented(*args: t.Any) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.SERVER_EXCEPTION,
                data=None,
                message="Not implemented",
            ),
            status=500,
        )

    async def unauthorized(*args: t.Any) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.AUTH_FAILED,
                data=None,
                message="Unauthorized",
            ),
            status=401,
        )

    async def forbidden(*args: t.Any) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.PERMISSION_DENIED,
                data=None,
                message="Forbidden",
            ),
            status=403,
        )

    async def accepted(*args: t.Any) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.SUCCESS,
                data=None,
                message="Accepted",
            ),
            status=202,
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
