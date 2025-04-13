import typing as t
from blacksheep import Application, Request, Response
from utils.responses import jsonify, StatusCode, ApiResponse
from blacksheep.exceptions import (
    BadRequest,
    Unauthorized,
    Forbidden,
    RangeNotSatisfiable,
    NotFound,
    InternalServerError,
    NotImplementedByServer,
)


def configure_error_handlers(app: Application) -> None:

    async def not_found_handler(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.PAGE_NOT_FOUND,
                data=None,
                message=str(exception) if exception else "Not found",
            ),
            status=404,
        )

    async def bad_request_exception(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.INVALID_PARAMS,
                data=None,
                message=str(exception) if exception else "Empty Argument",
            ),
            status=400,
        )

    async def not_implemented(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.SERVER_EXCEPTION,
                data=None,
                message=str(exception) if exception else "Not implemented",
            ),
            status=501,
        )

    async def unauthorized(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.AUTH_FAILED,
                data=None,
                message=str(exception) if exception else "Unauthorized",
            ),
            status=401,
        )

    async def forbidden(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.FORBIDDEN,
                data=None,
                message=str(exception) if exception else "Forbidden",
            ),
            status=403,
        )

    async def range_not_satisfiable(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.RANGE_NOT_SATISFIABLE,
                data=None,
                message=str(exception) if exception else "Range Not Satisfiable",
            ),
            status=416,
        )

    async def internal_server_error(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return jsonify(
            data=ApiResponse(
                code=StatusCode.SERVER_ERROR,
                data=None,
                message=str(exception) if exception else "Internal Server Error",
            ),
            status=500,
        )

    app.exceptions_handlers.update(
        {
            NotFound: not_found_handler,
            Unauthorized: unauthorized,
            Forbidden: forbidden,
            BadRequest: bad_request_exception,
            RangeNotSatisfiable: range_not_satisfiable,
            InternalServerError: internal_server_error,
            NotImplementedByServer: not_implemented,
            404: not_found_handler,
            400: bad_request_exception,
            500: internal_server_error,
        }
    )
