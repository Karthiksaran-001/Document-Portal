import uuid
from pathlib import Path 
import sys 
from datetime import datetime , timezone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogging
from exception.custom_exception import DocumentPortalException
from utils.models_loader import ModelLoader



class SingleDocIngestion:
    def __init__(self,data_dir = "data/single_document_chat",faiss_dir = "faiss_index"):
        try:
            self.log = CustomLogging().get_logger(__name__)
            self.model_loader = ModelLoader()
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents= True,exist_ok=True)
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents = True,exist_ok=True)
            self.log.info("SingleDocIngestion initalized" , temp_path = str(self.data_dir) , faiss_path = str(self.faiss_dir))
        except Exception as e:
            self.log.error("Failed in Initalization" , error = str(e))
            raise DocumentPortalException(e, sys)
    def ingest_file(self , uploaded_files):
        try:
            documents = []
            for uploaded_file in uploaded_files:
                unique_filename = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.pdf"
                temp_path=self.data_dir / unique_filename
                with open(temp_path, "wb") as f_out:
                    f_out.write(uploaded_file.read()) 
                self.log.info("PDF saved for ingestion", filename=uploaded_file.name)
                loader = PyPDFLoader(str(temp_path))
                docs = loader.load()
                documents.extend(docs)
            self.log.info("PDF files loaded", count=len(documents))
            return self._create_retriver(documents)
        except Exception as e:
            self.log.error("Failed in file ingestion" , error = str(e))
            raise DocumentPortalException(e, sys)
        
    def _create_retriver(self , documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)
            chunks = splitter.split_documents(documents)
            self.log.info("Documents are splitted into Chunks", count=len(chunks))
            embedding = self.model_loader.load_embedding()
            vectorstore = FAISS.from_documents(chunks, embedding)
            vectorstore.save_local(str(self.faiss_dir))
            self.log.info("Embedding stored in the DB Successfully" , path = str(self.faiss_dir))
            retriver = vectorstore.as_retriever(search_type = "similarity" , search_kwargs = {"k" : 5})
            return retriver
        except Exception as e:
            self.log.error("Failed in create retriver" , error = str(e))
            raise DocumentPortalException(e, sys)


