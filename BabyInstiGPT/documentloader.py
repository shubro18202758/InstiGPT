from langchain.document_loaders import JSONLoader

class DocumentLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.__extension = file_path.split(".")[-1]
        if self.__extension == 'jsonl':
            self.__json_lines = True
        else:
            self.__json_lines = False
        
    
    def load_documents(self, jq_schema):
        loader = JSONLoader(
            file_path = self.file_path,
            jq_schema = jq_schema,
            text_content = False,
            json_lines = self.__json_lines
        )
        documents = loader.load()
        return documents
        