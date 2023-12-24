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
#Use "ugrulebook" for ugrulebook or "resonin_courses" for resobin data
COLLECTION_NAME = "resonin_courses"

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

def load_data_in_db(embeddings: Embeddings, client_reset: bool = True, metadata: bool = True):
    client = get_db_client()
    if client_reset:
        client.reset()  # resets the database

    with open(DATA_PATH) as f:
        docs = json.load(f)
    
    formatted_metadatas = []
    formatted_documents = []
    for doc in docs:
        # Assuming 'metadata' contains URLs
        formatted_documents.append(json.dumps(doc))
        if metadata:
            metadata_dict = {"url": doc["metadata"]}
            formatted_metadatas.append(metadata_dict)
        else:
            formatted_metadatas.append(None)


    Chroma.from_texts(
        client=client,
        collection_name=COLLECTION_NAME,
        texts=formatted_documents,
        metadatas= formatted_metadatas,
        embedding=embeddings,
    )


if __name__ == "__main__":
    emdbeddings = get_embeddings()
    load_data_in_db(embeddings=emdbeddings, client_reset=True, metadata=False)
