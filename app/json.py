from typing import Any
from blacksheep import Application
from blacksheep.settings.json import json_settings
from utils.responses import ENCODER, DECODER
from msgspec.json import format


def configure_json(app: Application) -> None:
    """
    Configure JSON serialization settings for the application.
    """

    def serialize(obj: Any) -> str:
        return ENCODER.encode(obj).decode("utf-8")

    def pretty_serialize(obj: Any) -> str:
        return format(ENCODER.encode(obj), indent=4).decode("utf-8")

    json_settings.use(
        loads=DECODER.decode, dumps=serialize, pretty_dumps=pretty_serialize
    )
