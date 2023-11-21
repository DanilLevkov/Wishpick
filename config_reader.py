from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # SecretStr for more security
    bot_token: SecretStr

    # Make sure that .env has UTF-8 encoding
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


# Load
config = Settings()
