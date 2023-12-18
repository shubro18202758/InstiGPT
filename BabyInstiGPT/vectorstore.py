import chromadb
from langchain.vectorstores import Chroma
from documentloader import DocumentLoader
from embedding_model import embedder

DATA_PATH = "data/rulebook.jsonl"

def save_db(path, embeddings = embedder):
    dl = DocumentLoader(DATA_PATH)
    documents = dl.load_documents('.doc')
    db = Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory= path)
    db.persist()

def load_retriever(embeddings = embedder):
    db = Chroma(persist_directory="data/embeddings", embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 10})
    return retriever
