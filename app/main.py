"""
This module configures the BlackSheep application before it starts.
"""

from blacksheep import Application
from rodi import Container
from app.auth import configure_authentication
from app.cors import configure_cors
from app.docs import configure_docs
from app.errors import configure_error_handlers
from app.json import configure_json
from app.router import configure_router
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
    configure_authentication(app=app, settings=settings)
    configure_json(app=app)
    configure_cors(app=app, settings=settings)
    configure_error_handlers(app=app)
    configure_db(app=app)
    configure_docs(app=app, settings=settings)
    configure_router(app=app)
    return app


app = configure_application(*configure_services(load_settings()))
