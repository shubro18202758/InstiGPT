import json

from langchain_core.embeddings import Embeddings
from langchain.vectorstores.chroma import Chroma
import chromadb
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings
import os

EMBEDDING_MODEL = "thenlper/gte-large"

#Change these two according to data:
#Use "../data/ugrulebook.json" for ugrulebook or "../data/resobin_courses.json" for resobin data
DATA_PATH = "../data/resobin_courses.json"
#Use "ugrulebook" for ugrulebook or "resobin_courses" for resobin data
COLLECTION_NAME = "resobin_courses"

#set metadata = True for ugrulebook and False for resobin_data

def get_embeddings() -> Embeddings:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings

def get_db_client():
    return chromadb.HttpClient(
        host=os.environ["VECTOR_DB_HOST"],
        port=os.environ["VECTOR_DB_PORT"],
        settings=Settings(allow_reset=True),
    )
    
def preprocess_json_data(data_path: str, metadata: bool = True):
    with open(data_path) as f:
        docs = json.load(f)
    
    formatted_metadatas = []
    formatted_documents = []
    for doc in docs:
        formatted_documents.append(json.dumps(doc))
        if metadata:
            metadata_dict = {"url": doc["metadata"]}
            formatted_metadatas.append(metadata_dict)
        else:
            formatted_metadatas.append(None)
    
    return formatted_documents, formatted_metadatas

def load_data_in_db(docs, metadatas, collection_name: str, embeddings: Embeddings, client_reset: bool = False):
    client = get_db_client()
    if client_reset:
        client.reset()  # resets the database
    
    collection = client.get_or_create_collection(name = collection_name)
        
    Chroma.from_texts(
        client=client,
        collection_name=COLLECTION_NAME,
        texts=docs,
        metadatas= metadatas,
        embedding=embeddings,
    )


if __name__ == "__main__":
    emdbeddings = get_embeddings()
    docs, metadatas = preprocess_json_data(DATA_PATH, metadata=False)
    load_data_in_db(docs = docs, metadatas = metadatas, collection_name=COLLECTION_NAME, embeddings=emdbeddings, client_reset=True)