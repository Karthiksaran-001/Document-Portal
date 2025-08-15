from __future__ import annotations
import os
import sys
from pathlib import Path
import shutil
import hashlib
import uuid
import json
import fitz
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader , PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from typing import List, Dict, Tuple, Optional, Any, Iterable
from datetime import datetime , timezone
from utils.models_loader import ModelLoader
# from utils.file_io import _session_id , save_upload_files
# from utils.document_ops import load_document , compare_for_analysis , concat_for_comparrison
from logger.custom_logger import CustomLogging
from exception.custom_exception import DocumentPortalException
import warnings
warnings.filterwarnings("ignore")





class FAISSManager:
    def __init__(self):
        pass
    def _exits(self):
        pass
    @staticmethod 
    def _fingerprint():
        pass
    def _save_metadata(self):
        pass
    def load_or_create(self):
        pass 
    def add_documents(self):
        pass


class DocHandler:
    def __init__(self):
        pass
    def read_pdf(self):
        pass
    def save_pdf(self):
        pass
class DocumentCompare:
    def __init__(self):
        pass
    def save_upload_file(self):
        pass 
    def read_pdf(self):
        pass 
    def combine_documets(self):
        pass 
    def clean_old_session(self):
        pass 

class ChatIngestor:
    def __init__(self):
        pass
    def _resolve_dir(self): 
        pass
    def _split(self):
        pass
    def built_retriver(self):
        pass 


