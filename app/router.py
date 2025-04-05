from blacksheep import Application


def configure_router(app: Application) -> None:
    """
    Configure the router for the application.
    """
    from blog import endpoints
    from user import endpoints
