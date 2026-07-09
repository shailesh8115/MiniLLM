import os
import streamlit as st
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

import os

LLM_PROVIDER = "gemini"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"
def get_secret(name, default=None):
    """
    Read configuration in this order:
    1. Streamlit Cloud Secrets
    2. Environment Variables
    3. Default value
    """
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name, default)


# =====================================
# LLM Configuration
# =====================================


GEMINI_MODEL = get_secret(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

# Optional (used only for local Ollama)
OLLAMA_MODEL = get_secret(
    "OLLAMA_MODEL",
    "llama3.2:latest"
)

OLLAMA_HOST = get_secret(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

# =====================================
# Database
# =====================================

DATABASE_NAME = get_secret(
    "DATABASE_NAME",
    "database/minillm.db"
)

# =====================================
# Vector Database
# =====================================

VECTOR_DB = get_secret(
    "VECTOR_DB",
    "vectorstore"
)

# =====================================
# Upload Folder
# =====================================

UPLOAD_FOLDER = get_secret(
    "UPLOAD_FOLDER",
    "uploads"
)

# =====================================
# Create folders
# =====================================

for folder in [
    "database",
    "uploads",
    "vectorstore",
    "static",
    "templates",
]:
    os.makedirs(folder, exist_ok=True)