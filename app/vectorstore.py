from langchain_community.vectorstores import Chroma
from .embeddings import get_embeddings
from .config import DB,COLLECTION
def get_db():
    return Chroma(collection_name=COLLECTION,persist_directory=DB,embedding_function=get_embeddings())
