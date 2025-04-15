from blacksheep import Request, Response
from blacksheep.server.controllers import APIController, get, post
from schemas.account_schemas import RegisterInput
from user.tables import User
from blacksheep.exceptions import Forbidden

from utils.bindings import FromSchema


class BoostrapAPI(APIController):
    """
    本程序为 引导程序, 用于用户首次使用.
    如果返回 403 Forbidden, 表示数据库中已经存在用户数据
    """

    @classmethod
    def route(cls) -> str:
        return "bootstrap"

    async def on_request(self, request: Request) -> None:
        if await User.exists():
            raise Forbidden("Bootstrap API can only be accessed when no users exist.")

    @get("/")
    async def get_status(self) -> Response:
        return self.no_content()

    # 超级管理员账号密码
    @post("/register")
    async def register(self, user_input: FromSchema[RegisterInput]) -> Response:
        """
        注册超级管理员账号
        """
        data = user_input.value
        await User.create_user(
            username=data.username,
            password=data.password,
            email=data.email,
            nickname=data.nickname,
        )
        # TODO: 重定向到登录页面
        return self.created(location="l")
