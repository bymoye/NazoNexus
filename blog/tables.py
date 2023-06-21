from piccolo.table import Table
from piccolo.columns import Varchar, Text, Timestamp, ForeignKey
from fast_ulid import ulid

from user.tables import User


class Posts(Table):
    id = Varchar(length=26, primary_key=True, index=True, unique=True)
    title = Varchar(length=100)
    content = Text()
    author = ForeignKey(references=User)
    created_at = Timestamp()
    updated_at = Timestamp(required=False, null=True)

    def __str__(self):
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
            id=ulid(),
            title=title,
            content=content,
            author=author,
        )
