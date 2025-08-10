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
    def ingest_documents(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed in Ingesting Documents" , error = str(e))
            raise DocumentPortalException(e, sys)
    def _create_retriver(self , documents):
        try:
            pass 
        except Exception as e:
            self.log.error("Failed in create retriver" , error = str(e))
            raise DocumentPortalException(e, sys)
    
