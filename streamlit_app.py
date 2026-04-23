import streamlit as st
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

from app.chat import answer
from app.ingest import ingest_pdf
from app.vectorstore import get_db
from app.config import DB, COLLECTION

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .stChatInput {
        border-radius: 20px;
    }
    .sidebar .stButton button {
        width: 100%;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 RAG Chatbot")
st.markdown("A Retrieval-Augmented Generation chatbot powered by Groq and ChromaDB")

# Sidebar for document management
with st.sidebar:
    st.header("📚 Document Management")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload PDF to ingest", type="pdf")
    if uploaded_file is not None:
        if st.button("Ingest Document"):
            with st.spinner("Ingesting document..."):
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                try:
                    ingest_pdf(temp_path)
                    st.success(f"Successfully ingested {uploaded_file.name}")
                    # Clean up temp file
                    os.remove(temp_path)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error ingesting document: {str(e)}")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
    
    st.divider()
    
    # Display current documents info
    st.subheader("📊 Database Info")
    try:
        db = get_db()
        # Try to get count - different versions of Chroma may have different APIs
        try:
            count = len(db.get())
        except:
            try:
                count = db._collection.count()
            except:
                count = "Unknown"
        st.metric("Documents in DB", count)
    except Exception as e:
        st.error("Could not connect to database")
        st.write(f"Error: {str(e)}")
    
    # List existing PDFs in Docs folder
    st.subheader("📁 Available PDFs")
    docs_path = Path("Docs")
    if docs_path.exists():
        pdfs = list(docs_path.glob("*.pdf"))
        if pdfs:
            for pdf in pdfs:
                if st.button(f"Ingest {pdf.name}", key=f"ingest_{pdf.name}"):
                    with st.spinner(f"Ingesting {pdf.name}..."):
                        try:
                            ingest_pdf(str(pdf))
                            st.success(f"Successfully ingested {pdf.name}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error ingesting {pdf.name}: {str(e)}")
        else:
            st.info("No PDFs found in Docs folder")
    else:
        st.info("Docs folder not found")

# Main chat interface
st.header("💬 Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything about your documents..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        response = answer(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.divider()
st.markdown("*Built with Streamlit, LangChain, ChromaDB, and Groq*")