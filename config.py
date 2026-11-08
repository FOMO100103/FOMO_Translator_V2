from __future__ import annotations
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def app_root() -> Path:
    # In a PyInstaller build, keep .env beside the executable.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]

ROOT_DIR = app_root()
load_dotenv(ROOT_DIR / ".env")

def get_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "").strip()

def get_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"

def get_max_chunk_chars() -> int:
    try:
        return max(1000, int(os.getenv("MAX_CHUNK_CHARS", "6000")))
    except ValueError:
        return 6000
