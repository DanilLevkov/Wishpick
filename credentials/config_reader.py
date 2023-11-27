import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


def get_cred_path(file_name: str):
    credentials_dir = pathlib.Path(__file__).parent.resolve()
    if pathlib.Path(credentials_dir / file_name).exists():
        return credentials_dir / file_name
    else:
        assert False, f"Add {file_name} file to {credentials_dir}"


class Settings(BaseSettings):
    # SecretStr for more security
    bot_token: SecretStr
    firebase_realtime_db: SecretStr
    firebase_storage: SecretStr
    db_max_workers: int
    web_parser_host: str
    web_parser_port: int
    inside_docker: bool = False

    # Make sure that .env has UTF-8 encoding
    model_config = SettingsConfigDict(env_prefix='wishpick_')


# Load
config = Settings()
