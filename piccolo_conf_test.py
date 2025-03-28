import os
from piccolo_conf import PostgresEngine

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
