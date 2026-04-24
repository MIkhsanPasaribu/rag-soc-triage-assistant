import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Konfigurasi aplikasi yang dimuat dari file .env.
    """
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "llama3-70b-8192"
    
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "rag-soc-triage-assistant"
    
    CHROMA_PERSIST_DIRECTORY: str = "./data/vector_store"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
