import orjson
import typing as t
from blacksheep import Content, Request, Response, json

JSON_CONTENT_TYPE = b"application/json"


async def handler_error(request: Request, exc: Exception) -> Response:
    return Response(
        status=500,
        content=Content(
            JSON_CONTENT_TYPE, orjson.dumps({"status": 500, "error": f"{exc}"})
        ),
    )


def json_res(data: t.Any, status: int = 200) -> Response:
    """
    Returns a response with application/json content,
    and given status (default HTTP 200 OK).
    """
    return Response(
        status,
        None,
        Content(JSON_CONTENT_TYPE, orjson.dumps(data)),
    )


def pretty_json_res(
    data: t.Any,
    status: int = 200,
) -> Response:
    """
    Returns a response with indented application/json content,
    and given status (default HTTP 200 OK).
    """
    return Response(
        status,
        None,
        Content(JSON_CONTENT_TYPE, orjson.dumps(data, option=orjson.OPT_INDENT_2)),
    )
