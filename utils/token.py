import os
import jwt
import typing as t
from datetime import datetime, timezone
from app.settings import Settings
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


class JWTService:
    _instance: t.Self

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, settings: Settings):
        self.settings = settings
        project_root = Path(__file__).parent.parent
        self.secret_dir = os.path.join(project_root, "secret")
        if not os.path.exists(self.secret_dir):
            os.makedirs(self.secret_dir)
        self.private_key_path = os.path.join(self.secret_dir, "private.key")
        if not os.path.exists(self.private_key_path):
            self._generate_key_pair()

        with open(self.private_key_path, "rb") as f:
            self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(f.read())
            self.public_key = self.private_key.public_key()

    def _generate_key_pair(self):
        private_key = ed25519.Ed25519PrivateKey.generate()

        # 将密钥对保存到文件中
        with open(self.private_key_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PrivateFormat.Raw,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

    # 生成JWT
    def generate_jwt(self, payload: dict) -> str:
        """
        生成JWT
        :param payload: JWT的有效负载, 需要包含 "sub" 字段
        :return: 生成的JWT字符串
        """

        token = jwt.encode(
            {
                **payload,
                "iss": self.settings.info.title,
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc)
                + self.settings.jwt.expire_timedelta,
            },
            key=self.private_key,
            algorithm="EdDSA",
            headers={"alg": "EdDSA", "typ": "JWT"},
        )
        return token

    # 验证JWT
    def verify_jwt(self, token: str) -> dict:
        """
        验证JWT
        :param token: JWT字符串
        :return: 解码后的JWT有效负载
        """
        try:
            payload = jwt.decode(
                token,
                key=self.public_key,
                algorithms=["EdDSA"],
                issuer=self.settings.info.title,
                options={
                    "verify_signature": True,
                    "require": ["exp", "iss", "sub", "iss"],
                },
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidIssuerError:
            raise ValueError("Invalid issuer.")
        except jwt.MissingRequiredClaimError:
            raise ValueError("Missing required claim.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")
