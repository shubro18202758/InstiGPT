from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

from instigpt import config


def load_pdf_data(
    client: ClientAPI,
    embeddings: Embeddings,
    document_name: str,
    data_path: str,
) -> int:
    """Reads the data in the pdf, chunks it and stores the chunks in the
    database along with its embeddings.

    returns: int: number of chunks stored in the database
    """
    loader = PyPDFLoader(data_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=1000,
        length_function=len,
        is_separator_regex=True,
    )
    docs = loader.load()
    docs = [
        "\n".join([docs[i + j].page_content for j in range(4)])
        for i in range(len(docs) - 3)
    ]
    docs = text_splitter.create_documents(docs)
    docs = [doc.page_content for doc in docs]

    ids = [f"{document_name}-{i}" for i in range(len(docs))]
    metadatas = [{"source": document_name} for _ in range(len(docs))]

    if len(ids) == 0: 
        return 0

    coll = client.get_or_create_collection(config.COLLECTION_NAME)
    coll.add(
        documents=docs,
        embeddings=embeddings.embed_documents(docs),  # type: ignore
        metadatas=list(metadatas),
        ids=ids,
    )

    return len(docs)
