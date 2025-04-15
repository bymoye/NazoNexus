import typing as t
from guardpost import Identity

from user.tables import User

from uuid import UUID


class UserIdentity(Identity):
    @property
    def account(self) -> t.Optional[User]:
        return self.get("account")

    @property
    def id(self) -> t.Optional[UUID]:
        return self.account.id if self.account else None

    @property
    def username(self) -> t.Optional[str]:
        return self.account.username if self.account else None

    @property
    def email(self) -> t.Optional[str]:
        return self.account.email if self.account else None
