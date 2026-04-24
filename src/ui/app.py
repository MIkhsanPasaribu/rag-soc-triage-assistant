import json
import streamlit as st
import sys
import os

# Menambahkan parent directory ke PYTHONPATH agar src dapat diimport
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.features.triage.service import process_triage
from src.features.data_generation.generator import generate_synthetic_alerts
from src.shared.vector_store.client import add_playbook_to_store, get_vector_store

st.set_page_config(page_title="RAG SOC Triage Assistant", page_icon="🛡️", layout="wide")

st.title("🛡️ RAG SOC Triage Assistant (L1)")
st.markdown("Asisten AI untuk triase alert SIEM secara otomatis menggunakan pipeline RAG dan LangGraph.")

# Setup Vector Store (Membaca playbook dummy jika masih kosong)
@st.cache_resource
def setup_playbooks():
    store = get_vector_store()
    # Dummy playbook data
    playbooks = [
        "Playbook 1: Multiple Failed Login Attempts. Jika alert Multiple Failed Login Attempts muncul dengan severity Low, kemungkinan besar itu adalah user yang lupa password. Langkah: Cek apakah user segera berhasil login setelahnya. Jika iya, False Positive.",
        "Playbook 2: Suspicious PowerShell Execution. Jika PowerShell dijalankan dengan argumen encoded (-enc) atau bypass execution policy, eskalasi segera ke L2.",
        "Playbook 3: Malware Detected by EDR. Jika file dikarantina sukses, close alert. Jika gagal dikarantina dan network connect ke IP mencurigakan, eskalasi ke L2."
    ]
    
    # Hanya tambahkan jika store kosong
    # (Di Chroma versi baru, .get() mengembalikan list, bisa dihitung panjangnya)
    try:
        if len(store.get()["ids"]) == 0:
            add_playbook_to_store(texts=playbooks)
            return "✅ Playbook default berhasil dimuat ke Vector Store."
        return "✅ Playbook sudah ada di Vector Store."
    except Exception as e:
        return f"⚠️ Error memeriksa Vector Store: {e}"

status = setup_playbooks()
st.sidebar.success(status)

# Tombol untuk generate data
if "alerts" not in st.session_state:
    st.session_state.alerts = []

st.sidebar.header("Data SIEM Sintetis")
if st.sidebar.button("Generate Alerts"):
    with st.spinner("Membuat alert..."):
        st.session_state.alerts = generate_synthetic_alerts(3)
        st.sidebar.success(f"Berhasil membuat 3 alert!")

if st.session_state.alerts:
    alert_names = [f"{a['alert_type']} ({a['severity']})" for a in st.session_state.alerts]
    selected_alert_idx = st.sidebar.selectbox("Pilih Alert untuk dianalisis:", range(len(alert_names)), format_func=lambda x: alert_names[x])
    
    selected_alert = st.session_state.alerts[selected_alert_idx]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Detail Alert SIEM")
        st.json(selected_alert)
        
    with col2:
        st.subheader("Hasil Triase RAG")
        if st.button("Jalankan Triase 🚀"):
            with st.spinner("Menganalisis dengan LLM Groq & RAG..."):
                try:
                    result = process_triage(selected_alert)
                    
                    decision = result.get("decision", "Unknown")
                    if decision == "False Positive":
                        st.success(f"**Keputusan:** {decision}")
                    elif decision == "Escalate to L2":
                        st.error(f"**Keputusan:** {decision}")
                    else:
                        st.info(f"**Keputusan:** {decision}")
                        
                    st.progress(result.get("confidence_score", 0.0), text=f"Confidence Score: {result.get('confidence_score', 0.0)}")
                    
                    st.markdown("### Analisis:")
                    st.write(result.get("analysis", "Tidak ada penjelasan."))
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
else:
    st.info("👈 Silakan klik 'Generate Alerts' di sidebar untuk memulai.")
