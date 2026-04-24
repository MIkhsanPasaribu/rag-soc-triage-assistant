import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.shared.config import settings

def get_embeddings_model() -> HuggingFaceEmbeddings:
    """
    Mengembalikan model embedding HuggingFace lokal (gratis dan tanpa API key).
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store() -> Chroma:
    """
    Mengembalikan instance Vector Store ChromaDB.
    Membuat direktori persist_directory jika belum ada.
    """
    persist_dir = settings.CHROMA_PERSIST_DIRECTORY
    
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir, exist_ok=True)
        
    embeddings = get_embeddings_model()
    
    vector_store = Chroma(
        collection_name="soc_playbooks",
        embedding_function=embeddings,
        persist_directory=persist_dir
    )
    
    return vector_store

def add_playbook_to_store(texts: list[str], metadatas: list[dict] = None) -> None:
    """
    Menambahkan dokumen playbook SOC ke dalam Vector Store.
    """
    vector_store = get_vector_store()
    vector_store.add_texts(texts=texts, metadatas=metadatas)
