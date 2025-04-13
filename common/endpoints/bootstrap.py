from blacksheep import Request
from blacksheep.server.controllers import APIController, get
from user.tables import User
from blacksheep.exceptions import Forbidden


class BoostrapAPI(APIController):
    @classmethod
    def route(cls):
        return "bootstrap"

    async def on_request(self, request: Request):
        if not await User.exists():
            raise Forbidden("Bootstrap API can only be accessed when no users exist.")

    @get("/test")
    async def test_endpoint(self):
        return {"message": "Test endpoint is working!"}
