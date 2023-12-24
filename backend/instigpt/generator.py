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

#Redesign the prompt accordingly

PROMPT = ChatPromptTemplate.from_template(
"""You are a conversational ChatBot named InstiGPT.\n
Your task is to help users with whatever taks or queries they have. Please follow the instructions they provide you in queries.\n
You answer to queries related to IIT Bombay based on the context provided or the question of the User.\n
Now, Answer the query based on the context provided, answer in a very structured manner, and make proper and full sentences with introduction line to the topic while answering.\n
Past converstion is also given as reference, if there is no past conversation, ignore it.\n
Keep these IMPORTANT points in mind while answering the queries-\n
IMPORTANT -
1> Do not repeat those sentences which have been answered in past conversations.
2> If user tells you that you are wrong or incorrect, then accept that and try to correct yourself. Be nice while conversing.\n
3> If user asks for your opinion regarding something, then tell them what you think is the best.\n 
4> If some factual information is asked and is not provided in the context or question, then tell them that you don't have information on that particular topic.:\n
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
