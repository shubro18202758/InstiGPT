import os

from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import VoyageEmbeddings

# from langchain_community.embeddings import HuggingFaceEmbeddings
# from huggingface_hub import login

# from langchain_google_genai import GoogleGenerativeAIEmbeddings


from instigpt import config


def get_embeddings() -> Embeddings:
    # login to huggingface hub to access private models
    # login(os.environ["HUGGINGFACE_API_KEY"])

    # embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL, model_kwargs = {'device': 'cpu'})
    # embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)  # type: ignore

    embeddings = VoyageEmbeddings(
        voyage_api_key=os.environ["VOYAGE_API_KEY"],  # type: ignore
        model=config.EMBEDDING_MODEL,
    )

    return embeddings
