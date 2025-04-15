import typing as t
from blacksheep import Response, auth
from blacksheep.server.controllers import APIController, get, post

from user.schema import LoginInput
from user.tables import User
from utils.bindings import FromSchema
from utils.identity import UserIdentity
from utils.responses import ApiResponse, StatusCode, jsonify
from utils.token import JWTService, TokenPayload


class UsersAPI(APIController):
    @classmethod
    def route(cls) -> str:
        return "users"

    @get("/test")
    async def test_endpoint(self) -> Response:
        return self.json({"message": "Test endpoint is working!"})

    @post("/login")
    async def login(
        self, user_input: FromSchema[LoginInput], jwt_service: JWTService
    ) -> Response:
        """
        Login endpoint.
        """
        data = user_input.value
        user_id = await User.login(
            username=data.username,
            password=data.password,
        )

        if not user_id:
            return jsonify(
                data=ApiResponse(
                    code=StatusCode.USER_OR_PASSWORD_ERROR,
                    message="Invalid username or password.",
                )
            )
        token = jwt_service.generate_jwt(payload=TokenPayload(sub=user_id))
        return jsonify(
            data=ApiResponse(
                code=StatusCode.SUCCESS,
                message="Login successful.",
                data={"token": token},
            )
        )

    # 验证登录状态
    @auth()
    @get("/status")
    async def status(self, user: UserIdentity) -> Response:
        """
        Check login status endpoint.
        """
        if not user:
            return jsonify(
                data=ApiResponse(
                    code=StatusCode.USER_NOT_FOUND,
                    message="User not found.",
                )
            )
        return jsonify(
            data=ApiResponse(
                code=StatusCode.SUCCESS,
                message="User is logged in.",
                data={"user": user.id, "username": user.username},
            )
        )
