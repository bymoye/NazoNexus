from datetime import datetime
from piccolo.table import Table
from piccolo.columns import Varchar, Text, Timestamptz, ForeignKey
from utils.column_types import UUID as UUIDv7
from user.tables import User


class Posts(Table):
    id = UUIDv7(primary_key=True, required=True)
    title = Varchar(length=100)
    content = Text()
    author = ForeignKey(references=User)
    created_at = Timestamptz()
    updated_at = Timestamptz(required=False, null=True, auto_update=datetime.now)

    def __str__(self) -> str:
        return self.title

    @classmethod
    async def create_posts(cls, title: str, content: str, author: User) -> "Posts":
        """创建文章

        Args:
            title (str): 最大长度为100
            content (str): 文章主体
            author (User): 作者

        Returns:
            Posts: Posts实例
        """
        return await cls.objects().create(
            title=title,
            content=content,
            author=author,
        )
