import os
from dotenv import load_dotenv

load_dotenv()

# ======================================
# LLM Provider
# ======================================

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "openai"
)

# ======================================
# OpenAI
# ======================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4.1-mini"
)


# ======================================
# Ollama (Local Only)
# ======================================

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:latest"
)

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)


# ======================================
# Database
# ======================================

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "database/minillm.db"
)


# ======================================
# Vector Database
# ======================================

VECTOR_DB = os.getenv(
    "VECTOR_DB",
    "vectorstore"
)


# ======================================
# Uploads
# ======================================

UPLOAD_FOLDER = os.getenv(
    "UPLOAD_FOLDER",
    "uploads"
)


# ======================================
# Create folders
# ======================================

for folder in [
    "database",
    "uploads",
    "vectorstore",
    "static",
    "templates",
]:
    os.makedirs(folder, exist_ok=True)