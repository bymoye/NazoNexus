from blacksheep import Request
from blacksheep.server.controllers import APIController, get
from user.tables import User
from blacksheep.exceptions import Forbidden


class BoostrapAPI(APIController):
    @classmethod
    def route(cls):
        return "bootstrap"

    async def on_request(self, request: Request):
        # 在本路由中, 所有的请求都是基于 用户表 中不存在任何一条数据的情况下, 才能执行
        if await User.exists():
            raise Forbidden("Bootstrap API can only be accessed when no users exist.")

    @get("/test")
    async def test_endpoint(self):
        return {"message": "Test endpoint is working!"}
