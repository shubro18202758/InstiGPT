from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader

from instigpt import config


def load_csv_data(
    client: ClientAPI,
    embeddings: Embeddings,
    document_name: str,
    data_path: str,
) -> int:
    """Reads the data in the csv, stores it in the
    database along with its embeddings.

    returns: int: number of dicuments stored in the database
    """
    loader = CSVLoader(data_path)
    docs = loader.load()

    ids = [f"{document_name}-{i}" for i in range(len(docs))]
        
    if len(ids) == 0:
        return 0
    
    metadatas = [{"source": document_name} for _ in range(len(docs))]

    coll = client.get_or_create_collection(config.COLLECTION_NAME)
    # NOTE: The embeddings are automatically computed using the emdbedding function passed to the collection
    coll.add(
        documents=docs,
        embeddings=embeddings.embed_documents(docs),  # type: ignore
        metadatas=list(metadatas),
        ids=ids,
    )

    return len(docs)