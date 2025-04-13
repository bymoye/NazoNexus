from datetime import timedelta
from pathlib import Path
from msgspec import Struct
from msgspec import toml

BASE_DIR = Path(__file__).parent.parent


class App(Struct):
    show_error_details: bool
    enable_docs: bool
    allow_origin: list[str]


class JWT(Struct):
    expire_time: int
    issuer: str

    @property
    def expire_timedelta(self) -> timedelta:
        return timedelta(hours=self.expire_time)


class Site(Struct):
    copyright: str
    title: str
    description: str


class Database(Struct):
    database: str
    user: str
    password: str
    host: str
    port: int


class Settings(Struct):
    app: App
    jwt: JWT
    site: Site
    database: Database


_setting = None


def load_settings() -> Settings:
    global _setting
    if _setting:
        return _setting

    config_path = BASE_DIR.joinpath("config.toml")
    if config_path.exists():
        _setting = toml.decode(config_path.read_bytes(), type=Settings)
    else:
        raise FileNotFoundError("config.toml 未找到, 请正确配置")
    return _setting
