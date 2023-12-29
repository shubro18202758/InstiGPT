from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# from langchain.embeddings import HuggingFaceEmbeddings

from instigpt import config


def get_embeddings() -> Embeddings:
    # embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)  # type: ignore
    return embeddings
