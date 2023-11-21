import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


def get_env_path():
    credentials_dir = pathlib.Path(__file__).parent.resolve()
    if pathlib.Path(credentials_dir / '.env').exists():
        return credentials_dir / '.env'
    else:
        assert False, f"Add .env file to {credentials_dir}"


class Settings(BaseSettings):
    # SecretStr for more security
    bot_token: SecretStr
    firebase_realtime_db: SecretStr
    firebase_storage: SecretStr
    db_max_workers: int

    # Make sure that .env has UTF-8 encoding
    model_config = SettingsConfigDict(env_prefix='wishpick_', env_file=get_env_path(), env_file_encoding='utf-8')


# Load
config = Settings()
