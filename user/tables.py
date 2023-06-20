from piccolo.table import Table
from piccolo.columns import Varchar


class User(Table, tablename="auth_user"):
    username = Varchar(length=30)
    password = Varchar(length=30)
