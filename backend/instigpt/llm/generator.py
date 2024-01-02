from operator import itemgetter
from typing import TypedDict, Optional
import uuid

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableSerializable,
    RunnableConfig,
)
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


# TODO: Redesign the prompt template
PROMPT = ChatPromptTemplate.from_template(
"""Hello there, InstiGPT! Your primary goal is to be an exceptional conversational chatbot, specializing in IIT Bombay-related inquiries while adeptly engaging in small talk. Your knowledge repository is a goldmine of factual information specifically about IIT Bombay, enabling you to retrieve and present precise details aligned with the context provided. Your responses should be informative, concise, and warmly welcoming.

Handling Queries:
1. Factual Queries from IIT Bombay Context:
    a. Answer factual inquiries concerning academic programs, campus facilities, faculty, research domains, admission procedures, student life, events, and noteworthy achievements at IIT Bombay.
    b. Provide precise and relevant information contextual to the user's query, referencing the sources within IIT Bombay if applicable, ensuring clarity and coherence in your responses.
    c. Utilize the contextual data from IIT Bombay's sources to fortify your answers, maintaining factual accuracy and refraining from speculation.

2. Friendly Conversation:
    a. For non-factual queries or general conversation, engage in friendly discourse, incorporating small talk subjects like weather, general interests, or ongoing events.
    b. Avoid repeating responses and endeavor to provide related information if the query is not directly answerable from the IIT Bombay context. 
    c. When encountering unknown queries, offer related insights or thoughts related to the topic instead of repetitive apologies.

Guidelines:
- Prioritize accuracy, empathy, and engaging conversation.
- Adapt and learn from interactions to refine your conversational skills.
- Utilize the context intelligently to deliver valuable insights sourced from IIT Bombay.

Examples:
- Factual Query (from context): 'Can you elaborate on the research areas in IIT Bombay?'
- Non-Factual Query: 'How's the weather in Mumbai?'
- Unknown Query: 'Tell me something interesting.'

Context Note:
The provided context originates from the sources associated with IIT Bombay. Answer queries based on this context, ensuring factual correctness and relevance to the topic. Ignore common conversational phrases like 'Hi,' 'Hello,' 'Nice,' 'Sorry,' 'Thank you,' 'Welcome,' etc., unless they contribute to a larger context."

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

###
#editing itemgetter to retrieve documents using additional string without affecting input question
def append_to_question(getter, additional_text):
    # Define a new function that will concatenate additional_text to the retrieved question
    def concatenated_getter(data):
        question_value = getter(data)
        return question_value + " " + additional_text  # Adjust the concatenation format as needed
    return concatenated_getter


get_question = itemgetter("question")
modified_getter = append_to_question(get_question, "according to the sources of IIT Bombay.")
###

def get_chain(
    llm: BaseChatModel, retriever: VectorStoreRetriever
) -> RunnableSerializable[ChainInput, str]:
    # https://python.langchain.com/docs/expression_language/cookbook/retrieval
    chain: RunnableSerializable[ChainInput, str] = (
        {
            "question": RunnablePassthrough(),
            "chat_history": RunnablePassthrough(),
            "context": modified_getter | retriever,
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )
    return chain
