from blacksheep import Response
from blacksheep.server.controllers import APIController, get


class PostsAPI(APIController):
    @classmethod
    def route(cls) -> str:
        return "posts"

    @get("/test")
    async def test_endpoint(self) -> Response:
        return self.json({"message": "Test endpoint is working!"})
