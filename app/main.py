"""
This module configures the BlackSheep application before it starts.
"""
from blacksheep import Application
from rodi import Container

from app.auth import configure_authentication
from app.errors import configure_error_handlers
from app.services import configure_services
from app.settings import load_settings, Settings
from piccolo.engine import engine_finder


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(
        services=services, show_error_details=settings.app.show_error_details
    )

    configure_error_handlers(app)
    configure_authentication(app, settings)
    return app


app = configure_application(*configure_services(load_settings()))


@app.on_start
async def open_database_connection_pool(application: Application):
    try:
        engine = engine_finder()
        if engine is None:
            raise Exception("No engine found")
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@app.on_stop
async def close_database_connection_pool(application: Application):
    try:
        engine = engine_finder()
        if engine is None:
            raise Exception("No engine found")
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")
