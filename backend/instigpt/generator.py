from operator import itemgetter
from typing import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever

from . import config


def get_generator_model():
    return ChatGoogleGenerativeAI(
        model=config.GENERATOR_MODEL,
        temperature=config.GENERATOR_TEMPERATURE,
    )  # type: ignore


PROMPT = ChatPromptTemplate.from_template(
    """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
CONTEXT: {context}
----------------
CHAT HISTORY: {chat_history}
----------------
QUESTION: {question}
----------------
Helpful Answer:"""
)


class ChainInput(TypedDict):
    question: str
    chat_history: str


def get_chain(
    llm: BaseChatModel, retriever: VectorStoreRetriever
) -> RunnableSerializable[ChainInput, str]:
    # https://python.langchain.com/docs/expression_language/cookbook/retrieval
    chain: RunnableSerializable[ChainInput, str] = (
        {
            "question": RunnablePassthrough(),
            "chat_history": RunnablePassthrough(),
            "context": itemgetter("question") | retriever,
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return chain
