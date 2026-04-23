# Final RAG Customer Support Assistant
Uses Groq LLM + local embeddings.

## Setup
Run: `pip install -r requirements.txt`
Set `GROQ_API_KEY` in `.env`

## Usage

### Command Line Interface
- Ingest PDF: `python main.py --ingest docs/manual.pdf`
- Chat mode: `python main.py --chat`

### Web Interface (Streamlit)
Run: `streamlit run streamlit_app.py`

Features:
- Upload and ingest PDFs directly from browser
- Chat with AI assistant that has access to ingested documents
- View database statistics and available documents
- Persistent chat history

The web app will be available at http://localhost:8501
