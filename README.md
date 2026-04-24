# 🛡️ RAG SOC Triage Assistant (L1)

Proyek ini adalah asisten **Chatbot/RAG** yang dirancang untuk **Tier 1 Security Operations Center (SOC)**. 
Aplikasi ini menerima *alert* dari sistem SIEM (dalam format JSON) dan melakukan triase secara otomatis: apakah alert tersebut merupakan **False Positive**, perlu di-**Escalate ke L2**, atau dapat di-**Close**.

## 🚀 Fitur Utama

1. **RAG Pipeline**: Menggunakan **ChromaDB** untuk menyimpan dan mencari konteks dari *SOC Playbooks* lokal.
2. **LLM Inference**: Menggunakan **Groq API (Llama3-70B)** yang cepat untuk penalaran dan pengambilan keputusan triase.
3. **Agentic Workflow**: Orkestrasi alur kerja analisis menggunakan **LangGraph**.
4. **Synthetic Data**: Generator data bawaan (`faker`) untuk menghasilkan simulasi alert SIEM.
5. **Interactive UI**: Antarmuka berbasis web interaktif menggunakan **Streamlit**.
6. **Tracing**: Terintegrasi penuh dengan **LangSmith** untuk memantau performa, latensi, dan token LLM.

## 🏗️ Arsitektur Proyek (Feature-Based)

Proyek ini dibangun menggunakan arsitektur *feature-based* standar *Enterprise*, sehingga sangat modular:
```
rag-soc-triage-assistant/
├── data/                    # Penyimpanan lokal (ChromaDB)
├── src/
│   ├── features/
│   │   ├── data_generation/ # Generator alert SIEM sintetis
│   │   └── triage/          # Inti logika RAG, Prompt, LangGraph & Evaluasi
│   ├── shared/
│   │   ├── llm/             # Wrapper Groq LLM
│   │   ├── vector_store/    # Wrapper ChromaDB
│   │   └── config.py        # Pengaturan Pydantic
│   └── ui/
│       └── app.py           # Streamlit Frontend
├── .env                     # Variabel Environment (API Keys)
└── requirements.txt         # Dependensi Python
```

## 🛠️ Cara Menjalankan (Instalasi)

1. **Buat dan aktifkan Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instal Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfigurasi Environment**:
   * Salin file `.env.example` menjadi `.env`.
   * Masukkan `GROQ_API_KEY` milik Anda.
   * (Opsional) Masukkan kredensial `LANGCHAIN_API_KEY` jika Anda ingin mengaktifkan *tracing* di LangSmith.

## 💻 Menjalankan Aplikasi Streamlit

Setelah instalasi selesai, jalankan perintah berikut dari *root directory*:
```bash
streamlit run src/ui/app.py
```
Browser akan otomatis membuka `http://localhost:8501`.

## 🧪 Pengujian Evaluasi RAG

Untuk melihat seberapa cepat dan akurat sistem, Anda dapat menjalankan *script* evaluasi yang akan menjalankan triase pada 5 alert secara berurutan dan memberikan statistik akhir:
```bash
python src/features/triage/evaluation.py
```