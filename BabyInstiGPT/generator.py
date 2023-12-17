from langchain_google_genai import ChatGoogleGenerativeAI

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
        template = f"""Answer the query based on the context provided, answer in a very structured manner, and make proper and full sentences with introduction line to the topic while answering:\n
                                query : {query}\n
                                context : {string_i}"""
        result = self.llm.stream(template)
        return result