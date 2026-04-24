from langchain_groq import ChatGroq
from src.shared.config import settings

def get_llm_client(temperature: float = 0.0) -> ChatGroq:
    """
    Membuat dan mengembalikan instance client LLM Groq.
    
    Args:
        temperature (float): Tingkat kreativitas model (0.0 untuk deterministik).
        
    Returns:
        ChatGroq: Instance LangChain Groq model.
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY tidak ditemukan di environment variables.")
        
    return ChatGroq(
        temperature=temperature,
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.LLM_MODEL
    )
