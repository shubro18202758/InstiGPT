from typing import Union

import grequests
from html2text import html2text

from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings
from langchain.text_splitter import MarkdownTextSplitter

from instigpt import config


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

    text_splitter = MarkdownTextSplitter()
    coll = client.get_or_create_collection(config.COLLECTION_NAME)
    num_docs_added = 0

    reqs = [grequests.get(link) for link in data_path]
    for res in grequests.map(reqs, size=20):
        if res is None:
            continue
        
        try:
            md_text = html2text(res.text)
            docs = text_splitter.split_text(md_text)
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
