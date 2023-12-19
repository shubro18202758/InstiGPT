from langchain_core.embeddings import Embeddings
from langchain.embeddings import HuggingFaceEmbeddings

from . import config


def get_embeddings() -> Embeddings:
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    return embeddings
