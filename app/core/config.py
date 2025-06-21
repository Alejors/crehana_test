from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DB: str

    @property
    def db_url(self):
        return (
            f"mysql+asyncmy://{self.MYSQL_USER}:"
            f"{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:"
            f"{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
