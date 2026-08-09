from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):

    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


class SecurityConfig(BaseSettings):

    ALGORITHM: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


db_config = DatabaseConfig()
security_config = SecurityConfig()
