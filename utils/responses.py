import typing as t
from msgspec import json
from blacksheep import Content, Response

JSON_CONTENT_TYPE = b"application/json"


def json_res(data: t.Any, status: int = 200) -> Response:
    """
    Returns a response with application/json content,
    and given status (default HTTP 200 OK).
    """
    return Response(
        status=status,
        headers=None,
        content=Content(content_type=JSON_CONTENT_TYPE, data=json.encode(data)),
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
        status=status,
        headers=None,
        content=Content(
            content_type=JSON_CONTENT_TYPE,
            data=(json.format(json.encode(data))),
        ),
    )
