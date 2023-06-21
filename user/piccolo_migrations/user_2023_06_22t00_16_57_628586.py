from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Boolean
from piccolo.columns.column_types import Email
from piccolo.columns.column_types import Secret
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Varchar
from piccolo.columns.indexes import IndexMethod


ID = "2023-06-22T00:16:57:628586"
VERSION = "0.115.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="user", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="active",
        db_column_name="active",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="admin",
        db_column_name="admin",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="email",
        db_column_name="email",
        column_class_name="Email",
        column_class=Email,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": True,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="last_login",
        db_column_name="last_login",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": None,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="nickname",
        db_column_name="nickname",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="superuser",
        db_column_name="superuser",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "default": False,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.alter_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="username",
        db_column_name="username",
        params={"length": 36, "unique": True},
        old_params={"length": 30, "unique": False},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="password",
        db_column_name="password",
        params={"length": 255, "secret": True},
        old_params={"length": 30, "secret": False},
        column_class=Secret,
        old_column_class=Varchar,
    )

    return manager
