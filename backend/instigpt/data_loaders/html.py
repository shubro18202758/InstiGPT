from typing import Union
import re

import grequests
from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup

from instigpt import config


def has_unrecognized_characters(text):
    count = sum((not c.isascii() or not c.isprintable()) and c != "\n" for c in text)
    if (count / len(text)) * 100 > 0.1:
        return True
    else:
        return False


def load_html_data(
    client: ClientAPI,
    embeddings: Embeddings,
    data_path: Union[str, list[str]],
) -> int:
    """Fetches the html content from the link(s), converts it to markdown, splits
    it by headers and then stores it in the database along with its embeddings.

    returns: int: number of dicuments stored in the database
    """
    if type(data_path) == str:
        data_path = [data_path]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=1000,
        length_function=len,
        is_separator_regex=True,
    )
    coll = client.get_or_create_collection(config.COLLECTION_NAME)
    num_docs_added = 0

    reqs = [grequests.get(link) for link in data_path]
    for res in grequests.map(reqs, size=20):
        if res is None:
            continue

        try:
            html = res.text
            soup = BeautifulSoup(html, "lxml")
            if soup.body is None:
                continue
            body = soup.body.get_text()
            text = re.sub(r"\n+", "\n", body)
            texts = text.split("\n")
            documents = [text for text in texts if len(text) >= 1300]
            docs = []
            for doc in documents:
                docs += text_splitter.split_text(doc)
            docs = [doc for doc in docs if not has_unrecognized_characters(doc)]
            metadatas = [{"source": res.url} for _ in range(len(docs))]
            ids = [f"{res.url}-{i}" for i in range(len(docs))]
        except AssertionError:
            continue

        if len(ids) == 0:
            continue

        coll.add(
            documents=docs,
            embeddings=embeddings.embed_documents(docs),  # type: ignore
            metadatas=list(metadatas),
            ids=ids,
        )
        num_docs_added += len(docs)

    return num_docs_added
