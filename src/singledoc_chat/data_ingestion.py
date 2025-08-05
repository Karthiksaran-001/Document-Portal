import uuid
from pathlib import Path 
import sys 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogging
from exception.custom_exception import DocumentPortalException
from utils.models_loader import ModelLoader
from dotenv import load_dotenv


class SingleDocIngestion:
    def __init__(self):
        try:
            self.log = CustomLogging().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed in Initalization" , error = str(e))
            raise DocumentPortalException(e, sys)
    def ingest_file(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed in file ingestion" , error = str(e))
            raise DocumentPortalException(e, sys)
        
    def _create_retriver(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed in create retriver" , error = str(e))
            raise DocumentPortalException(e, sys)


