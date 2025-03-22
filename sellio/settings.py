import os
from pathlib import Path

from pydantic import BaseModel
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import EnvSettingsSource
from pydantic_settings import PydanticBaseSettingsSource
from pydantic_settings import SettingsConfigDict
from pydantic_settings import TomlConfigSettingsSource

CONFIG_PATH = Path(__file__).parent.parent / "config/{}.toml".format(
    os.environ["SELLIO__ENV"]
)


class DbConfig(BaseModel):
    db: str
    host: str
    port: str
    user: SecretStr
    password: str


class Config(BaseSettings):
    env: str
    main_db: DbConfig

    model_config = SettingsConfigDict(frozen=True)

    @classmethod
    def load(cls) -> "Config":
        return cls()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        **_,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            EnvSettingsSource(
                settings_cls,
                env_prefix="SELLIO__",
                case_sensitive=False,
            ),
            TomlConfigSettingsSource(
                settings_cls=settings_cls,
                toml_file=CONFIG_PATH,
            ),
        )
