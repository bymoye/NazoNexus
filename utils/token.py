import jwt
import typing as t
from datetime import datetime, timezone
from app.settings import Settings, BASE_DIR, load_settings
from pathlib import Path
from app.settings import BASE_DIR
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from msgspec import Struct, field, to_builtins, convert
from uuid_utils.compat import UUID, uuid7
from utils.logging import get_logger
from time import time

logger = get_logger("jwt_service")

SETTINGS: Settings = load_settings()


class TokenPayload(Struct):
    """
    Token payload structure.
    """

    sub: UUID  # Subject (用户ID)
    iss: str = SETTINGS.jwt.issuer  # Issuer (颁发者)
    exp: int = field(
        default_factory=lambda: int(
            (time() + SETTINGS.jwt.expire_timedelta),
        )
    )  # Expiration time (过期时间)
    iat: int = field(default_factory=lambda: int(time()))  # Issued at time (签发时间)
    jti: UUID = field(default_factory=lambda: uuid7())  # JWT ID (唯一标识符)


class JWTService:
    _instance: t.Self
    _initialized: bool = False

    def __new__(cls) -> t.Self:
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return t.cast(t.Self, cls._instance)

    def __init__(self) -> None:
        if JWTService._initialized:
            return
        JWTService._initialized = True
        secret_dir = BASE_DIR.joinpath("secret")
        self.private_key_path = secret_dir.joinpath("private.key")

        if not secret_dir.exists():
            secret_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created secret directory at {secret_dir}")

        if not self.private_key_path.exists():
            logger.info("Generating new Ed25519 key pair")
            self._generate_key_pair()
        else:
            logger.debug("Loading existing Ed25519 key pair")

        try:
            self.private_key: ed25519.Ed25519PrivateKey = t.cast(
                ed25519.Ed25519PrivateKey,
                serialization.load_pem_private_key(
                    data=self.private_key_path.read_bytes(),
                    password=None,
                ),
            )
            self.public_key = self.private_key.public_key()
        except Exception as e:
            logger.error(f"Failed to load private key: {e}")
            raise

    def _generate_key_pair(self) -> None:
        private_key = ed25519.Ed25519PrivateKey.generate()
        try:
            self.private_key_path.write_bytes(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                ),
            )
            logger.info(f"Private key saved to {self.private_key_path}")
        except Exception as e:
            logger.error(f"Failed to save private key: {e}")
            raise

    # 生成JWT
    def generate_jwt(self, payload: TokenPayload) -> str:
        """
        生成JWT
        :param payload: JWT的有效负载
        :return: 生成的JWT字符串
        """
        try:
            token = jwt.encode(
                payload=to_builtins(payload),
                key=self.private_key,
                algorithm="EdDSA",
                headers={"alg": "EdDSA", "typ": "JWT"},
            )
            logger.debug(f"Generated JWT for subject: {payload.sub}")
            return token

        except Exception as e:
            logger.error(f"Failed to generate JWT: {e}")
            raise

    # 验证JWT
    def verify_jwt(self, token: str) -> TokenPayload:
        """
        验证JWT
        :param token: JWT字符串
        :return: 解码后的JWT有效负载
        """
        try:
            payload: t.Dict[str, t.Any] = jwt.decode(
                token,
                key=self.public_key,
                algorithms=["EdDSA"],
                issuer=SETTINGS.jwt.issuer,
                options={
                    "verify_signature": True,
                    "require": ["exp", "iss", "sub", "iss"],
                },
            )
            return convert(payload, type=TokenPayload)
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidIssuerError:
            raise ValueError("Invalid issuer.")
        except jwt.MissingRequiredClaimError:
            raise ValueError("Missing required claim.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")
