import datetime
import typing as t
from piccolo.table import Table
from piccolo.columns import Varchar, Secret, Email, Boolean, Timestamptz
from piccolo.utils.sync import run_sync
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash
from uuid_utils import UUID
from utils.logging import get_logger
from utils.column_types import UUID as UUIDv7

logger = get_logger(__name__)


class User(Table, tablename="auth_user"):
    id = UUIDv7(primary_key=True, required=True)
    username = Varchar(length=36, unique=True)
    password = Secret(length=255)
    nickname = Varchar(null=True)
    email = Email(length=255, unique=True)
    active = Boolean(default=False)
    admin = Boolean(default=False)
    superuser = Boolean(default=False)
    last_login = Timestamptz(null=True, default=None, required=False)

    _min_password_length = 6
    _max_password_length = 128
    _ph = PasswordHasher()

    def __setattr__(self, name: str, value: t.Any):
        """
        确保密码被hash
        """
        if name == "password" and (
            value[:9]
            not in {
                "$argon2id",
                "$argon2i$",
                "$argon2d$",
            }
        ):
            value = self.__class__.hash_password(value)

        super().__setattr__(name, value)

    @classmethod
    def _validate_password(cls, password: str) -> bool:
        """
        验证密码是否符合要求
        """
        if len(password) < cls._min_password_length:
            raise ValueError("Password length must be at least 6 characters")

        if len(password) > cls._max_password_length:
            raise ValueError("Password length must be at most 128 characters")

        return True

    ###########################################################################

    @classmethod
    def hash_password(cls, password: str) -> str:
        """hash密码
        Args:
            password (str): 密码, 需要大于6位, 小于128位

        Returns:
            str: hash后的密码
        """
        if not cls._validate_password(password):
            raise ValueError("Invalid password.")
        return cls._ph.hash(password)

    @classmethod
    async def login(cls, username: str, password: str) -> t.Optional[UUID]:
        """
        如果用户存在且密码正确, 则更新数据库中的 ``last_login`` 字段
        否则返回 ``None``
        """
        if not cls._validate_password(password):
            return None

        response = await cls.objects().where(cls.username == username).first()
        if not response:
            # No match found
            return None

        stored_password = response.password
        try:
            if cls._ph.verify(stored_password, password):
                update_data: t.Dict = {
                    cls.last_login: datetime.datetime.now(tz=datetime.timezone.utc)
                }
                if cls._ph.check_needs_rehash(stored_password):
                    update_data = {
                        **update_data,
                        cls.password: cls.hash_password(password),
                    }
                await cls.update(update_data).where(cls.username == username)
                return response.id
            else:
                return None
        except InvalidHash as e:
            logger.warning(f"错误的用户密码存储, 无法验证: {e}")
            return None
        except Exception as e:
            logger.warning(f"发生了未知错误: {e}")
            return None

    ###########################################################################

    @classmethod
    def update_password_sync(
        cls,
        password: str,
        user_id: t.Optional[UUID] = None,
        username: t.Optional[str] = None,
    ) -> None:
        return run_sync(
            cls.update_password(user_id=user_id, username=username, password=password)
        )

    @classmethod
    async def update_password(
        cls,
        password: str,
        user_id: t.Optional[UUID] = None,
        username: t.Optional[str] = None,
    ) -> None:
        cls._validate_password(password)
        if not user_id and not username:
            raise ValueError("`user_id` or `username` must be provided")
        if user_id and username:
            raise ValueError(
                "`user_id` and `username` cannot be provided at the same time"
            )

        if user_id:
            clause = cls.id == user_id
        else:
            clause = cls.username == username

        password = cls.hash_password(password)

        await cls.update({cls.password: password}).where(clause).run()

    ###########################################################################

    @classmethod
    def create_user_sync(
        cls, username: str, password: str, email: str, nickname: t.Optional[str] = None
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
        cls, username: str, password: str, email: str, nickname: t.Optional[str] = None
    ) -> "User":
        if not username:
            raise ValueError("username cannot be empty")
        if not email:
            raise ValueError("email cannot be empty")
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
