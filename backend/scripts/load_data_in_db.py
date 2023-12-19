import json

from langchain_core.embeddings import Embeddings
from langchain.vectorstores.chroma import Chroma

from instigpt import config
from instigpt.embeddings import get_embeddings
from instigpt.retriever import get_db_client


def load_data_in_db(embeddings: Embeddings):
    client = get_db_client()
    client.reset()  # resets the database

    with open(config.DATA_PATH) as f:
        docs = json.load(f)

    Chroma.from_texts(
        client=client,
        collection_name=config.COLLECTION_NAME,
        texts=list(map(lambda doc: doc["doc"], docs)),
        metadatas=list(map(lambda doc: doc["metadata"], docs)),
        embedding=embeddings,
    )


if __name__ == "__main__":
    emdbeddings = get_embeddings()
    load_data_in_db(embeddings=emdbeddings)
