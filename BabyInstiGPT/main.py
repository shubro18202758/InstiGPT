from documentloader import DocumentLoader
from vectorstore import load_retriever
from generator import generator_model
from generator import QAChain
from set_env import set_env
import os

GEMINI_API = "AIzaSyAu_91Wmojozz8LWAyWIoQKReelbkQP8L8"

def main():
    set_env(GEMINI_API= GEMINI_API)
    retriever = load_retriever()
    llm = generator_model()
    chain = QAChain(llm, retriever)
    query = 'Describe different grade points'
    answer = chain.qna(query)
    print(answer)
    
    
if __name__ == "__main__":
    main()