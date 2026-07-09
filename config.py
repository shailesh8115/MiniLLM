import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_secret(name, default=None):
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name, default)


# ==============================
# LLM
# ==============================

LLM_PROVIDER = get_secret("LLM_PROVIDER", "openai")

OPENAI_API_KEY = get_secret("OPENAI_API_KEY")

OPENAI_MODEL = get_secret(
    "OPENAI_MODEL",
    "gpt-4.1-mini"
)

# Optional (for local development only)

OLLAMA_MODEL = get_secret(
    "OLLAMA_MODEL",
    "llama3.2:latest"
)

OLLAMA_HOST = get_secret(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

# ==============================
# Database
# ==============================

DATABASE_NAME = "database/minillm.db"

VECTOR_DB = "vectorstore"

UPLOAD_FOLDER = "uploads"

for folder in [
    "database",
    "uploads",
    "vectorstore",
    "static",
    "templates",
]:
    os.makedirs(folder, exist_ok=True)