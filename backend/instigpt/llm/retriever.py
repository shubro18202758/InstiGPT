import os
from typing import Generator

import chromadb
from chromadb.config import Settings
from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings
from langchain.vectorstores.chroma import Chroma
from langchain.tools import Tool
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper

from instigpt import config


def get_db_client() -> ClientAPI:
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

    return db.as_retriever(search_kwargs={"k": 5})


def get_search_results_retriever() -> Generator[Tool, None, None]:
    api_keys = os.environ["GOOGLE_API_KEYS"].split(",")
    wrappers = [GoogleSearchAPIWrapper(google_api_key=key) for key in api_keys]  # type: ignore
    tools = [
        Tool(
            name="Google Search",
            description="Search Google for recent results.",
            func=lambda x: wrapper.results(x, 5),
        )
        for wrapper in wrappers
    ]

    i = 0
    while True:
        yield tools[i]

        i += 1
        i %= len(api_keys)
