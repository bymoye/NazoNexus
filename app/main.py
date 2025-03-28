"""
This module configures the BlackSheep application before it starts.
"""

from blacksheep import Application
from rodi import Container

from app.auth import configure_authentication
from app.errors import configure_error_handlers
from app.services import configure_services
from app.db import configure_db
from app.settings import load_settings, Settings


def configure_application(
    services: Container,
    settings: Settings,
) -> Application:
    app = Application(
        services=services, show_error_details=settings.app.show_error_details
    )

    configure_error_handlers(app)
    configure_authentication(app, settings)
    configure_db(app=app)
    return app


app = configure_application(*configure_services(load_settings()))
