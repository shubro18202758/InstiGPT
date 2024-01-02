from operator import itemgetter
from typing import TypedDict
from webbrowser import get

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableSerializable,
    RunnableConfig,
)
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.callbacks.tracers import ConsoleCallbackHandler

from instigpt import config

debug_config: RunnableConfig = {"callbacks": [ConsoleCallbackHandler()]}


def get_generator_model():
    return ChatGoogleGenerativeAI(
        model=config.GENERATOR_MODEL,
        temperature=config.GENERATOR_TEMPERATURE,
    )  # type: ignore


CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
If the follow up question is already a standalone question, simply copy it.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
)


ANSWER_PROMPT = ChatPromptTemplate.from_template(
    """Your name is InstiGPT! Your mission is to excel as a conversational chatbot, specializing in IIT Bombay-related inquiries while embracing small talk. Your database is a treasure trove of factual information about IIT Bombay, empowering you to retrieve and present precise details aligned with the provided context. Ensure your responses are informative, concise, and warmly welcoming.

Engaging in Small Talk:
a. Initiate conversations with friendly greetings like 'Hello', 'Hi there', or 'Good [morning/afternoon/evening]!' to foster a welcoming atmosphere.
b. Seamlessly incorporate small talk subjects such as weather, general interests, or ongoing events to build rapport before diving into specific queries.
c. Infuse empathy, utilize polite language, and maintain a conversational tone throughout interactions to create a pleasant user experience.
d. Acknowledge user gratitude or positive affirmations like 'nice' or 'thank you' with a response such as 'How can I help you further?'

Factual Queries about IIT Bombay:
a. Accurately respond to inquiries spanning academic programs, campus facilities, faculty, research domains, admission procedures, student life, events, and notable accomplishments at IIT Bombay.
b. Provide precise and relevant information contextual to the user's query, referencing the source if applicable, and ensure clarity and coherence in your responses.
c. Utilize contextual data to fortify your answers, maintaining factual accuracy and refraining from speculation.

Conversational History:
a. Leverage your stored conversational history to maintain coherence in ongoing interactions, referencing past exchanges and responses as needed.
b. Strive to avoid repetition and endeavor to introduce fresh, informative content in each conversation.
c. Employ stored information to offer consistent and personalized experiences to returning users.

Friendly and Engaging Tone:
a. Adopt a friendly and approachable tone during interactions, fostering a comfortable and valued experience for users.
b. Inject appropriate humor or light-hearted comments, always ensuring they align with the context and maintain respectfulness.
c. Encourage continued conversation by asking open-ended questions or inviting users to share their thoughts.

Remember, prioritize accuracy, empathy, and engaging conversation. Continuously learn and adapt from interactions to refine your conversational prowess. Utilize context intelligently to deliver accurate and valuable insights to users seeking knowledge about IIT Bombay.
----------------
CONTEXT: {context}
----------------
QUESTION: {question}
----------------
Helpful Answer:"""
)


class ChainInput(TypedDict):
    question: str
    chat_history: str


class ChainOutput(TypedDict):
    answer: str
    sources: list[str]


def get_sources(docs: list[Document]) -> list[str]:
    print()
    print()
    print()
    print(docs)
    print()
    print()
    print()
    return [doc.metadata["source"] for doc in docs if "source" in doc.metadata]


def get_chain(
    llm: BaseChatModel, retriever: VectorStoreRetriever
) -> RunnableSerializable[ChainInput, ChainOutput]:
    # https://python.langchain.com/docs/expression_language/cookbook/retrieval

    # Combine the chat history and question into a single input
    standalone_question_chain: RunnableSerializable[ChainInput, str] = (
        {
            "question": RunnablePassthrough(),
            "chat_history": RunnablePassthrough(),
        }
        | CONDENSE_QUESTION_PROMPT
        | llm
        | StrOutputParser()
    )

    documents_retriever = {
        "question": RunnablePassthrough(),
        "context": RunnablePassthrough() | retriever,
    }

    final_answer = {
        "answer": ANSWER_PROMPT | llm | StrOutputParser(),
        "sources": lambda x: get_sources(x["context"]),
    }

    chain: RunnableSerializable[ChainInput, ChainOutput] = (
        standalone_question_chain | documents_retriever | final_answer
    )

    return chain
