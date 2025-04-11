from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info
from app.settings import Settings
from utils.scalar.scalar_docs import ScalarUIProvider


def configure_docs(app: Application, settings: Settings) -> None:
    """
    Configure the OpenAPI documentation for the application.
    """
    if settings.app.enable_docs:
        docs = OpenAPIHandler(
            info=Info(title="NazoNexus API", version="0.0.1"), anonymous_access=True
        )
        docs.ui_providers[0] = ScalarUIProvider()
        docs.bind_app(app)
