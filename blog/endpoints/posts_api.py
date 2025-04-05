from blacksheep.server.controllers import APIController, get


class PostsAPI(APIController):
    @classmethod
    def route(cls):
        return "posts"

    @get("/test")
    async def test_endpoint(self):
        return {"message": "Test endpoint is working!"}
