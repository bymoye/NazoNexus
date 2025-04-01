from piccolo.table import Table
from piccolo.columns import Varchar, Text, Timestamp, ForeignKey
from utils.column_types import UUID as UUIDv7
from user.tables import User


class Posts(Table):
    id = UUIDv7(primary_key=True, required=True)
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
            title=title,
            content=content,
            author=author,
        )
