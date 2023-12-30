import json

from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings

from instigpt import data_loaders


def load_urls_data(
    client: ClientAPI,
    embeddings: Embeddings,
    data_path: str,
) -> int:
    with open(data_path) as f:
        urls = json.load(f)
    doc_links = []
    pdf_links = []
    for url in urls:
        if url[-3:] == "jpg" or url[-3:] == "png" or url[-4:] == "jpeg":
            continue
        elif url[-3:] == "pdf":
            pdf_links.append(url)
        else:
            doc_links.append(url)

    num_pdfs = sum(
        [
            data_loaders.load_pdf_data(
                client=client,
                embeddings=embeddings,
                document_name=link,
                data_path=link,
            )
            for link in pdf_links
        ]
    )
    num_docs = data_loaders.load_html_data(
        client=client,
        embeddings=embeddings,
        data_path=doc_links,
    )

    return num_pdfs + num_docs
