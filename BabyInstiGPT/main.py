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
    '''query = 'What should I do if I get a DX grade in a course and I dont want it to appear on my transcript?'
    answer = chain.qna(query, "")
    for chunk in answer:
        print(chunk.content)'''
        
    chain.convo_chain()
    
    
    
if __name__ == "__main__":
    main()