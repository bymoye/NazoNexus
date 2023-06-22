import os
from piccolo.engine.postgres import PostgresEngine

from piccolo.conf.apps import AppRegistry


DB = PostgresEngine(
    config={
        "database": os.environ.get("PG_DATABASE", "test"),
        "user": os.environ.get("PG_USER", "postgres"),
        "password": os.environ.get("PG_PASSWORD", "postgres"),
        "host": os.environ.get("PG_HOST", "localhost"),
        "port": int(os.environ.get("PG_PORT", "5432")),
    }
)

APP_REGISTRY = AppRegistry(apps=["user.piccolo_app", "blog.piccolo_app"])
