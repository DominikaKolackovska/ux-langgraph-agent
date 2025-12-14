from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    openai_model: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    supabase_db_host: str | None = os.environ.get("SUPABASE_DB_HOST")
    supabase_db_port: int = int(os.environ.get("SUPABASE_DB_PORT", "5432"))
    supabase_db_name: str | None = os.environ.get("SUPABASE_DB_NAME")
    supabase_db_user: str | None = os.environ.get("SUPABASE_DB_USER")
    supabase_db_password: str | None = os.environ.get("SUPABASE_DB_PASSWORD")

    def has_db(self) -> bool:
        return all([
            self.supabase_db_host,
            self.supabase_db_name,
            self.supabase_db_user,
            self.supabase_db_password,
        ])

settings = Settings()
