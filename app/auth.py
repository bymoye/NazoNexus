import typing as t
from blacksheep import Application, Request
from blacksheep.exceptions import Forbidden
from app.settings import Settings
from guardpost import AuthenticationHandler, AuthorizationStrategy, Policy
from guardpost.common import AuthenticatedRequirement

from user.tables import User
from utils.identity import UserIdentity
from utils.logging import get_logger
from utils.token import JWTService
from time import time

from cacheout import Cache


def configure_authentication(app: Application, settings: Settings) -> None:
    """
    Configure authentication as desired. For reference:
    https://www.neoteroi.dev/blacksheep/authentication/
    """
    app.use_authentication().add(JWTAuthHandler(settings=settings))
    app.use_authorization(
        strategy=AuthorizationStrategy(
            container=app.services,
            default_policy=Policy("default"),
        ).add(
            Policy(
                "authenticated",
                AuthenticatedRequirement(),
            )
        ),
    )


class JWTAuthHandler(AuthenticationHandler):
    def __init__(
        self,
        settings: Settings,
        auth_mode: str = "JWT Bearer",
    ) -> None:
        self.logger = get_logger("jwt_auth")
        self.auth_mode = auth_mode
        self.jwt_service = JWTService()
        self.ttl_cache = Cache(maxsize=256, ttl=3600)  # 1 hour

    async def decode_token(self, token: str) -> t.Optional[UserIdentity]:
        """
        Decode the JWT token and return the user identity.
        """
        if not self.ttl_cache.get(token):
            payload = self.jwt_service.verify_jwt(token=token)
            user = await User.objects().get(User.id == payload.sub)
            if not user:
                raise Forbidden("User not found.")
            self.ttl_cache.set(
                key=token,
                value=UserIdentity(
                    claims={"account": user}, authentication_mode=self.auth_mode
                ),
                ttl=(ttl if (ttl := payload.exp - time()) < 3600 else 3600),
            )

        return self.ttl_cache.get(token)

    async def authenticate(  # type: ignore
        self,
        context: Request,
    ) -> t.Optional[UserIdentity]:
        authorization_value = context.get_first_header(b"Authorization")
        if not authorization_value:
            context.user = UserIdentity({})
            return None
        if not authorization_value.startswith(b"Bearer "):
            self.logger.debug(
                "Invalid Authorization header, not starting with `Bearer `, "
                "the header is ignored."
            )
            context.user = UserIdentity({})
            return None
        token = authorization_value[7:].decode()
        try:
            return await self.decode_token(token=token)
        except Exception as e:
            self.logger.error(f"Token decoding failed: {e}")
            context.user = UserIdentity({})
            return None
