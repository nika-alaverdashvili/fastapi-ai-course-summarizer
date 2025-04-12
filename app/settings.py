import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 2))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 15))


settings = Settings()
