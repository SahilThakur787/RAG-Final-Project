from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from .embeddings import get_embeddings
from .config import DB,COLLECTION
def ingest_pdf(path):
    docs=PyPDFLoader(path).load()
    chunks=RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=150).split_documents(docs)
    db=Chroma.from_documents(chunks,get_embeddings(),collection_name=COLLECTION,persist_directory=DB)
    db.persist()
    print('Indexed',len(chunks),'chunks')
