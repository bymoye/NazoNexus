import typing as t
from blacksheep import Application, Request

from app.settings import Settings
from guardpost import AuthenticationHandler, AuthorizationStrategy, Policy
from guardpost.common import AuthenticatedRequirement

from utils.identity import UserIdentity
from utils.logging import get_logger


def configure_authentication(app: Application, settings: Settings):
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
    ):
        self.logger = get_logger("jwt_auth")
        self.auth_mode = auth_mode

    async def decode_token(self, token: str) -> t.Optional[UserIdentity]:
        """
        Decode the JWT token and return the user identity.
        """
        # Implement your JWT decoding logic here
        # For example, using PyJWT:
        # decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        # return UserIdentity(decoded)
        pass

    async def authenticate(self, context: Request) -> t.Optional[UserIdentity]:  # type: ignore
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

        # try:
        #     decoded = await self._validator.validate_jwt(token)
        # except (InvalidAccessToken, InvalidTokenError) as ex:
        #     # pass, because the application might support more than one
        #     # authentication method and several JWT Bearer configurations
        #     self.logger.debug(
        #         "JWT Bearer - access token not valid for this configuration: %s",
        #         str(ex),
        #     )
        #     pass
        # else:
        #     context.user = Identity(decoded, self.auth_mode)
        #     return context.user

        # context.user = Identity({})
        # return None
