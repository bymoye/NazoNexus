from blacksheep.server.controllers import APIController, get


class UsersAPI(APIController):
    @classmethod
    def route(cls):
        return "users"

    @get("/test")
    async def test_endpoint(self):
        return {"message": "Test endpoint is working!"}
