import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

CACHE_TYPE = os.getenv("CACHE_TYPE", "diskcache")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_SEARCH_LOOPS = int(os.getenv("MAX_SEARCH_LOOPS", "3"))
TOTAL_TOKEN_BUDGET = int(os.getenv("TOTAL_TOKEN_BUDGET", "50000"))

REPORTS_DIR = BASE_DIR / "outputs" / "reports"
AUDIT_LOGS_DIR = BASE_DIR / "outputs" / "audit_logs"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOGS_DIR.mkdir(parents=True, exist_ok=True)
