import os

from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoModel
from huggingface_hub import login

# from langchain_google_genai import GoogleGenerativeAIEmbeddings


from instigpt import config


def get_embeddings() -> Embeddings:
    # login to huggingface hub to access private models
    login(os.environ["HUGGINGFACE_API_KEY"])

    # Manually load the model first as a workaround for specifying `trust_remote_code=True`
    AutoModel.from_pretrained(
        "jinaai/jina-embeddings-v2-base-en",
        trust_remote_code=True,
    )

    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    # embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)  # type: ignore

    return embeddings
