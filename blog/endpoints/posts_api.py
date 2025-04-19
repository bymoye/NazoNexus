from blacksheep import Response, FromQuery
from blacksheep.server.controllers import APIController, get

from blog.tables import Posts
from utils.responses import ApiResponse, StatusCode, jsonify


class PostsAPI(APIController):
    @classmethod
    def route(cls) -> str:
        return "posts"

    @get("/list")
    async def get_list(self, page: FromQuery[int] = FromQuery(1)):
        _page = page.value
        if _page < 1:
            return jsonify(
                ApiResponse(
                    code=StatusCode.INVALID_PARAMS,
                    message="Page must be greater than 0.",
                )
            )
        return jsonify(
            ApiResponse(
                code=StatusCode.SUCCESS,
                data=(
                    await Posts.select()
                    .limit(10)
                    .offset((_page - 1) * 10)
                    .order_by(Posts.created_at, ascending=False)
                ),
            )
        )
