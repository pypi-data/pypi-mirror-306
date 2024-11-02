from config import CONFIG
from document_processing import Document_parser, Chunking
from embeddings import Embedding
from vectorstore import get_vectorstore
from llm import get_model


class Pipeline:
    def __init__(self):
        self.parser = Document_parser()
        self.chunker = Chunking(CONFIG['app']['chunking_type'])
        self.embedder = Embedding()
        self.model = CONFIG['app']['model']
        self.db = get_vectorstore(CONFIG['app']['vectorstore_type'])
        self.llm = get_model(CONFIG['app']['model'])


    def file_in_db(self, filename):
        try:
            self.db.open_db()
            return self.db.check_existence(filename)
        finally:
            self.db.close_db()
    

    def process_file(self, file_path):
        try:
            content_dict = self.parser.parse(file_path)
            chunks = []
            for filename, content in content_dict.items():
                chunks_per_file = self.chunker.splitter(content)
                chunks.extend([(filename, chunk) for chunk in chunks_per_file])
            content_only = [chunk[1] for chunk in chunks]
            embeddings = self.embedder.encode(content_only)
            metadatas = [{'chunk': i, 'filename': chunk[0]} for i, chunk in enumerate(chunks)]
            
            self.db.open_db()
            self.db.add_objects(content_only, embeddings, metadatas)
            return {"message": "Document has been successfully processed."}
        except Exception as e:
            print(str(e))
        finally:
            self.db.close_db()
    
    
    def answer_question(self, question):
        self.db.open_db()
        question_embedding = self.embedder.encode([question])[0]
        similar_contents = self.db.search(question_embedding, question)
        
        context = ' '.join(similar_contents)
        answer = self.llm.generate_response(question, context)
        
        self.db.close_db()
        return answer