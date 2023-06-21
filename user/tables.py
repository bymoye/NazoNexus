import secrets
import logging
import datetime
import typing as t
from piccolo.table import Table
from piccolo.columns import Varchar, Serial, Secret, Email, Boolean, Timestamp
from piccolo.utils.sync import run_sync
from argon2 import PasswordHasher

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
    ph = PasswordHasher()

    def __setattr__(self, name: str, value: t.Any):
        """
        Make sure that if the password is set, it's stored in a hashed form.
        """
        if name == "password" and not value.startswith("$argon2id"):
            value = self.__class__.hash_password(value)

        super().__setattr__(name, value)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hashes the password, ready for storage, and for comparing during
        login.

        :raises ValueError:
            If an excessively long password is provided.

        """
        if len(password) > cls._max_password_length:
            logger.warning("Excessively long password provided.")
            raise ValueError("The password is too long.")
        hash = cls.ph.hash(password)
        return hash

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

        if password.startswith("$argon2id"):
            logger.warning("Tried to create a user with an already hashed password.")
            raise ValueError("Do not pass a hashed password.")

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
        try:
            print(f"开始验证密码,时间:: {datetime.datetime.now()}")
            if cls.ph.verify(stored_password, password):
                update_data: t.Dict = {cls.last_login: datetime.datetime.now()}
                if cls.ph.check_needs_rehash(stored_password):
                    update_data = {
                        **update_data,
                        cls.password: cls.hash_password(password),
                    }
                print(f"验证密码结束,时间:: {datetime.datetime.now()}")
                await cls.update(update_data).where(cls.username == username)
                return response["id"]
            else:
                return None
        except Exception as e:
            logger.warning(f"Error verifying password: {e}")
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
