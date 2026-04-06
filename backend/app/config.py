from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))   # 15 - default
        self.REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30))
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        db = os.getenv("POSTGRES_DB")
        self.DATABASE_URL = os.getenv("DATABASE_URL")

        # ✅ SAFETY CHECKS
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY not set in environment")
        if not self.ALGORITHM:
            raise ValueError("ALGORITHM not set in environment")

settings = Settings()