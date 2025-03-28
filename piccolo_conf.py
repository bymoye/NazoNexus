import os
from piccolo.engine.postgres import PostgresEngine

from piccolo.conf.apps import AppRegistry

from app.settings import load_settings

settings = load_settings().database
DB = PostgresEngine(
    config={
        "database": settings.database,
        "user": settings.user,
        "password": settings.password,
        "host": settings.host,
        "port": settings.port,
    }
)

APP_REGISTRY = AppRegistry(apps=["user.piccolo_app", "blog.piccolo_app"])
