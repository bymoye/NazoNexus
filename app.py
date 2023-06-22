import os
from dotenv import load_dotenv

from piccolo.engine import engine_finder
from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from utils.reference import handler_error


load_dotenv()

app = Application(show_error_details=bool(os.environ.get("SHOW_ERROR_DETAILS", None)))


docs = OpenAPIHandler(info=Info(title="New API", version="0.0.1"))
docs.bind_app(app)

app.handle_internal_server_error = handler_error


async def open_database_connection_pool(application):
    try:
        engine = engine_finder()
        if engine is None:
            raise Exception("No engine found")
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


async def close_database_connection_pool(application):
    try:
        engine = engine_finder()
        if engine is None:
            raise Exception("No engine found")
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")


app.on_start += open_database_connection_pool
app.on_stop += close_database_connection_pool
