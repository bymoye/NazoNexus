import orjson
import typing as t
from blacksheep import Content, Response

JSON_CONTENT_TYPE = b"application/json"


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
