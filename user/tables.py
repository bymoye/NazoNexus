import secrets
import logging
import datetime
import typing as t
from piccolo.table import Table
from piccolo.columns import Varchar, Serial, Secret, Email, Boolean, Timestamp
from piccolo.utils.sync import run_sync
from pyargon2 import hash

logger = logging.getLogger(__name__)


class User(Table, tablename="auth_user"):
    id: Serial
    username = Varchar(length=36, unique=True)
    password = Secret(length=255)
    nickname = Varchar(null=True)
    email = Email(length=255, unique=True)
    active = Boolean(default=False)
    admin = Boolean(default=False)
    superuser = Boolean(default=False)
    last_login = Timestamp(null=True, default=None, required=False)

    _min_password_length = 6
    _max_password_length = 128

    def __setattr__(self, name: str, value: t.Any):
        """
        Make sure that if the password is set, it's stored in a hashed form.
        """
        if name == "password" and not value.startswith("argon2"):
            value = self.__class__.hash_password(value)

        super().__setattr__(name, value)

    @classmethod
    def get_salt(cls):
        return secrets.token_hex(16)

    @classmethod
    def hash_password(
        cls, password: str, salt: t.Optional[str] = None, iterations: int = 600
    ) -> str:
        """
        Hashes the password, ready for storage, and for comparing during
        login.

        :raises ValueError:
            If an excessively long password is provided.

        """
        if len(password) > cls._max_password_length:
            logger.warning("Excessively long password provided.")
            raise ValueError("The password is too long.")

        if not salt:
            salt = cls.get_salt()
        hashed = hash(password, salt=salt, time_cost=iterations)
        return f"argon2${iterations}${salt}${hashed}"

    @classmethod
    def _validate_password(cls, password: str):
        """
        Validate the raw password. Used by :meth:`update_password` and
        :meth:`create_user`.

        :param password:
            The raw password e.g. ``'hello123'``.
        :raises ValueError:
            If the password fails any of the criteria.

        """
        if not password:
            raise ValueError("A password must be provided.")

        if len(password) < cls._min_password_length:
            raise ValueError("The password is too short.")

        if len(password) > cls._max_password_length:
            raise ValueError("The password is too long.")

        if password.startswith("pbkdf2_sha256"):
            logger.warning("Tried to create a user with an already hashed password.")
            raise ValueError("Do not pass a hashed password.")

    @classmethod
    def split_stored_password(cls, password: str) -> t.List[str]:
        elements = password.split("$")
        if len(elements) != 4:
            raise ValueError("Unable to split hashed password")
        return elements

    @classmethod
    async def login(cls, username: str, password: str) -> t.Optional[int]:
        """
        Make sure the user exists and the password is valid. If so, the
        ``last_login`` value is updated in the database.

        :returns:
            The id of the user if a match is found, otherwise ``None``.

        """
        if len(username) > cls.username.length:
            logger.warning("Excessively long username provided.")
            return None

        if len(password) > cls._max_password_length:
            logger.warning("Excessively long password provided.")
            return None

        response = (
            await cls.select(cls._meta.primary_key, cls.password)
            .where(cls.username == username)
            .first()
            .run()
        )
        if not response:
            # No match found
            return None

        stored_password = response["password"]

        algorithm, iterations, salt, hashed = cls.split_stored_password(stored_password)

        if cls.hash_password(password, salt, int(iterations)) == stored_password:
            await cls.update({cls.last_login: datetime.datetime.now()}).where(
                cls.username == username
            )
            return response["id"]
        else:
            return None

    @classmethod
    def create_user_sync(
        cls, username: str, password: str, email: str, nickname: t.Union[str, None]
    ) -> "User":
        return run_sync(
            cls.create_user(
                username=username,
                password=password,
                email=email,
                nickname=nickname,
            )
        )

    @classmethod
    async def create_user(
        cls, username: str, password: str, email: str, nickname: t.Union[str, None]
    ) -> "User":
        if not username:
            raise ValueError("A username must be provided.")
        if not nickname:
            nickname = username

        cls._validate_password(password=password)
        user = cls(
            username=username,
            password=password,
            email=email,
            nickname=nickname,
            active=True,
        )
        await user.save()
        return user
