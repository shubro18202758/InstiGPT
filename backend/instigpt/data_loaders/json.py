import json

from chromadb.api import ClientAPI
from langchain_core.embeddings import Embeddings

from instigpt import config


def load_json_data(
    client: ClientAPI,
    embeddings: Embeddings,
    document_name: str,
    data_path: str,
) -> int:
    """Reads the data in the json file and stores it in the database along with its embeddings.
    The json file must contain a list of documents. Each document must be a dictionary with a
    "doc" key containing the text of the document and an optional "metadata" key containing the metadata
    which is a dictionary.

    returns: int: number of chunks stored in the database
    """
    with open(data_path) as f:
        docs = json.load(f)
    metadata_in_document = "metadata" in docs[0]

    ids = [f"{document_name}-{i}" for i in range(len(docs))]
    
    if len(ids) == 0: 
        return 0

    if metadata_in_document:
        metadatas = []
        for doc in docs:
            metadata = doc["metadata"]
            if "source" not in metadata:
                metadata["source"] = document_name
            metadatas.append(metadata)
    else:
        metadatas = [{"source": document_name} for _ in range(len(docs))]
    docs = [json.dumps(doc["doc"]) for doc in docs]

    coll = client.get_or_create_collection(config.COLLECTION_NAME)
    coll.add(
        documents=docs,
        embeddings=embeddings.embed_documents(docs),  # type: ignore
        metadatas=list(metadatas),
        ids=ids,
    )

    return len(docs)
