import os

import chromadb
from chromadb.config import Settings
from langchain_core.embeddings import Embeddings
from langchain.vectorstores.chroma import Chroma

from instigpt import config


def get_db_client():
    return chromadb.HttpClient(
        host=os.environ["VECTOR_DB_HOST"],
        port=os.environ["VECTOR_DB_PORT"],
        settings=Settings(allow_reset=True),
    )


def get_retriever(embeddings: Embeddings):
    client = get_db_client()
    db = Chroma(
        client=client,
        collection_name=config.COLLECTION_NAME,
        embedding_function=embeddings,
    )

    return db.as_retriever(search_kwargs={"k": 10})
