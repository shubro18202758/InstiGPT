from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

def generator_model(model = "gemini-pro", temperature = 0):
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    return llm

class QAChain:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever
    
    def qna(self, query):
        docs = self.retriever.get_relevant_documents(query)
        string_i = ""
        for i in range(0, 10):
            string_i += docs[i].page_content
        template = f"""You are BabyInstiGPT. Answer the query based on the context provided, answer in a very structured manner, and make proper and full sentences with introduction line to the topic while answering. Give short answers preferably in 50-100 words:\n
                                query : {query}\n
                                context : {string_i}"""
        result = self.llm.stream(template)
        
        '''for chunk in result:
            print(chunk.content)'''
            
        return result
    
    def __qna_change_context(self, query, past_convo, context = ""):
        docs = self.retriever.get_relevant_documents(query)
        for i in range(0, 10):
            context += docs[i].page_content
        template = f"""Your name is BabyInstiGPT, if someone asks your name, tell them this.\n 
                        Now, Answer the query based on the context provided, answer in a very structured manner, and make proper and full sentences with introduction line to the topic while answering.\n
                        Past converstion is also given as reference, if there is no past conversation, ignore it.\n
                        IMPORTANT - Do not repeat those sentences which have been answered in past conversations. :\n
                        past conversation : {past_convo}\n
                        query : {query}\n
                        context : {context}"""
        result = self.llm.stream(template)
        
        '''for chunk in result:
            print(chunk.content)'''
            
        return result, context
    
    def convo_chain(self):
        query = input("Hi, Ask me anything related to IIT Bombay UG Rulebook. \nUser : \n")
        conv = ""
        conv += "User : " + query + "\n"
        context = " "
        
        for _ in range(3):
            ans, temp = self.__qna_change_context(query, conv, context)
            context = temp + context
            reply = ""
            for chunk in ans:
                print(chunk.content)
                reply += chunk.content
            conv += "BabyInstiGPT : " + reply + "\n"
            if(_ == 2):
                break
            query = input("User : \n")
            conv += "User : " + query + "\n"
        
        return
            
        