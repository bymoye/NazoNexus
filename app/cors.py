from blacksheep import Application

from app.settings import Settings


def configure_cors(app: Application, settings: Settings) -> None:
    """
    Configure CORS settings for the application.
    """
    app.use_cors(
        allow_headers=["*"],
        allow_methods=["*"],
        allow_origins=settings.app.allow_origin,
        max_age=30,
    )
