from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import VoyageEmbeddings

# from langchain.embeddings import HuggingFaceEmbeddings

from instigpt import config




def get_embeddings() -> Embeddings:
    # embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    # embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)  # type: ignore
    embeddings = VoyageEmbeddings(voyage_api_key="pa-d0rh4n-08o1-yY5HkGrz8co84wUhZoidq92Ppr00lpw", model="voyage-02")
    return embeddings
