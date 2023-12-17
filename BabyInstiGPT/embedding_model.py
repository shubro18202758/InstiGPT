from langchain.embeddings import HuggingFaceEmbeddings

EMBEDDING_MODEL = "thenlper/gte-large"

def load_embedding_model():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings