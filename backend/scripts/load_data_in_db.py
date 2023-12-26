import json
import os

from langchain_core.embeddings import Embeddings
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
import chromadb
from chromadb.config import Settings

EMBEDDING_MODEL = "thenlper/gte-large"

COLLECTION_NAME = "prototype"

#set metadata = True for ugrulebook and False for resobin_data in load_json_data

def get_embeddings() -> Embeddings:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings

def get_db_client():
    return chromadb.HttpClient(
        host=os.environ["VECTOR_DB_HOST"],
        port=os.environ["VECTOR_DB_PORT"],
        settings=Settings(allow_reset=True),
    )
    
def load_json_data(embeddings: Embeddings, document_name: str, data_path: str, metadata: bool = False, client_reset: bool = False):
    client = get_db_client()
    if client_reset:
        client.reset()  # resets the database    
    with open(data_path) as f:
        docs = json.load(f)
    
    formatted_metadatas = []
    formatted_documents = []
    ids = []
    counter = 1
    for doc in docs:
        ids.append(document_name + str(counter))
        counter+=1
        formatted_documents.append(json.dumps(doc))
        if metadata:
            metadata_dict = {"info": doc["metadata"]}
            formatted_metadatas.append(metadata_dict)
        else:
            formatted_metadatas.append(None)
    
    Chroma.from_texts(
        client=client,
        collection_name=COLLECTION_NAME,
        texts=formatted_documents,
        metadatas=formatted_metadatas,
        embedding=embeddings,
        ids = ids
    )

def load_pdf_data(embeddings: Embeddings, document_name: str, data_path: str, client_reset: bool = False):
    client = get_db_client()
    if client_reset:
        client.reset()  # resets the database 
        
    loader = PyPDFLoader(data_path)
    docs = loader.load_and_split()
    ids = []
    counter = 1
    for doc in docs:
        ids.append(document_name + str(counter))
        counter+=1
    
    Chroma.from_documents(
        client=client,
        collection_name=COLLECTION_NAME,
        documents=docs,
        embedding=embeddings,
        ids = ids
    )

if __name__ == "__main__":
    emdbeddings = get_embeddings()
    # load_pdf_data(embeddings=emdbeddings, document_name="bluebook", data_path="../data/Bluebook Edition Three.pdf", client_reset=False)
    # load_pdf_data(embeddings=emdbeddings, document_name="apping", data_path="../data/Apping Guide Booklet.pdf", client_reset=False)
    # load_pdf_data(embeddings=emdbeddings, document_name="noncoreapping", data_path="../data/Non-Core Apping Guide.pdf", client_reset=False)
    # load_pdf_data(embeddings=emdbeddings, document_name="courseinfo", data_path="../data/Course Info Booklet 2020-21.pdf", client_reset=False)
    # load_pdf_data(embeddings=emdbeddings, document_name="ugrulebook", data_path="../data/ugrulebook.pdf", client_reset=False)
    # load_json_data(embeddings=emdbeddings, document_name="resobin", metadata=False, data_path="../data/resobin_courses.json", client_reset=False)
    client = get_db_client()
    coll = client.get_collection(name = COLLECTION_NAME)
    print(client.list_collections())
    print(coll.count())