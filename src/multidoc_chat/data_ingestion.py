import uuid
from pathlib import Path 
import sys 
from datetime import datetime , timezone
from langchain_community.document_loaders import PyPDFLoader , Docx2txtLoader , TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogging
from exception.custom_exception import DocumentPortalException
from utils.models_loader import ModelLoader


class DocumentIngestor:
    SUYPPORTED_EXTENSIONS = {".pdf" : "" , ".txt" : "" , ".docx" : "" , ".doc" : "" , ".html" : "" , ".md" : ""}
    def __init__(self , temp_dir:str = "data\multi_document_chat" , faiss_dir:str = "faiss_index" , session_id:str = None):
        try:
            self.log = CustomLogging().get_logger(__name__)
            self.temp_dir = Path(temp_dir)
            self.temp_dir.mkdir(parents= True,exist_ok=True)
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents = True,exist_ok=True)
            # session ID
            self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_temp_dir = self.temp_dir / self.session_id
            self.session_temp_dir.mkdir(parents= True,exist_ok=True)
            self.session_faiss_dir = self.faiss_dir / self.session_id
            self.session_faiss_dir.mkdir(parents = True,exist_ok=True)
            self.model_loader = ModelLoader()
            self.log.info("DocumentIngestor initalized" , 
                          temp_path = str(self.temp_dir) , 
                          faiss_path = str(self.faiss_dir) , 
                          session_id = self.session_id,
                          temp_path = str(self.session_temp_dir) , faiss_path = str(self.session_faiss_dir))
        except Exception as e:
            self.log.error("Failed in Initalization" , error = str(e))
            raise DocumentPortalException(e, sys)
    def ingest_documents(self , uploaded_files):
        try:
            documents = []
            for file in uploaded_files:
                ext = Path(file.filename).suffix.lower()
                if ext not in self.SUYPPORTED_EXTENSIONS:
                    self.log.warning("Unsupported file" , file_name = file.filename)
                    continue
                unique_filename = f"{uuid.uuid4().hex}{ext}"
                file_path = self.session_temp_dir / unique_filename
                with open(file_path , "wb") as buffer:
                    buffer.write(file.file.read())
                self.log.info("File saved for Ingestion" , file_name = file.filename , file_path = str(file_path) , session_id = self.session_id)
                
                if ext == ".pdf":
                    loader = PyPDFLoader(str(file_path))
                elif ext == ".txt":
                    loader = TextLoader(str(file_path) , encoding = "utf-8")
                elif ext in [".docx" , ".doc"]:
                    loader = Docx2txtLoader(str(file_path))
                else:
                    self.log.warning("Unsupported File type" , file_name = file.filename,file_path = str(file_path) , session_id = self.session_id)
                    continue
                
                documents.extend(loader.load())
            if not documents:
                raise DocumentPortalException("No Valid Documents Found" , sys)
            self.log.info("All documents loaded" , session_id = self.session_id, no_of_docs = len(documents)) 
            return self._create_retriver(documents)

        except Exception as e:
            self.log.error("Failed in Ingesting Documents" , error = str(e))
            raise DocumentPortalException(e, sys)
    def _create_retriver(self , documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 200)
            chunks = splitter.split_documents(documents)
            self.log.info("All documents splitted" , session_id = self.session_id, chunks = len(chunks)) 
            embedding = self.model_loader.load_embedding()
            retriever = FAISS.from_documents(chunks , embedding)
            retriever.save_local(str(self.session_faiss_dir))
            self.log.info("Retriver created and saved in the path" , path = str(self.session_faiss_dir) , session_id = self.session_id) 
            return retriever
            
        except Exception as e:
            self.log.error("Failed in create retriver" , error = str(e))
            raise DocumentPortalException(e, sys)
    
