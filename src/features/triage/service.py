import json
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import StrOutputParser
from src.shared.llm.client import get_llm_client
from src.shared.vector_store.client import get_vector_store
from src.features.triage.prompts import triage_prompt

# Define state schema for LangGraph
class TriageState(TypedDict):
    alert: dict
    context: str
    result: dict

def retrieve_context(state: TriageState) -> TriageState:
    """Node: Mengambil dokumen dari Vector Store berdasarkan alert_type atau deskripsi."""
    vector_store = get_vector_store()
    query = state["alert"].get("description", "")
    
    # Ambil 2 dokumen paling relevan
    docs = vector_store.similarity_search(query, k=2)
    context_text = "\n\n".join([d.page_content for d in docs])
    
    if not context_text:
        context_text = "Tidak ada playbook yang relevan ditemukan untuk alert ini."
        
    return {"context": context_text}

def analyze_alert(state: TriageState) -> TriageState:
    """Node: Menganalisis alert menggunakan LLM Groq."""
    llm = get_llm_client(temperature=0.1) # Deterministic
    
    chain = triage_prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "context": state["context"],
        "alert": json.dumps(state["alert"], indent=2)
    })
    
    try:
        # Bersihkan output jika LLM memberikan format markdown (```json ... ```)
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:-3]
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:-3]
            
        result_dict = json.loads(cleaned_response)
    except Exception as e:
        # Fallback jika gagal parsing JSON
        result_dict = {
            "analysis": f"Gagal memparsing respons LLM: {str(e)}. Respons asli: {response}",
            "decision": "Escalate to L2", # Fail safe: selalu eskalasi jika sistem bingung
            "confidence_score": 0.0
        }
        
    return {"result": result_dict}

# Membangun LangGraph Workflow
workflow = StateGraph(TriageState)

workflow.add_node("retrieve", retrieve_context)
workflow.add_node("analyze", analyze_alert)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "analyze")
workflow.add_edge("analyze", END)

triage_app = workflow.compile()

def process_triage(alert: dict) -> dict:
    """
    Fungsi utama untuk memproses satu alert SIEM melalui pipeline RAG.
    """
    inputs = {"alert": alert, "context": "", "result": {}}
    output = triage_app.invoke(inputs)
    return output["result"]
