import os , sys 
from pathlib import Path 
from logger.custom_logger import CustomLogging
from exception.custom_exception import DocumentPortalException
from utils.models_loader import ModelLoader
from utils.config_loader import load_config
from prompt.prompt_library import PROPMT_REGISTRY
from dotenv import load_dotenv
import pandas as pd 
from model.models import *
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import JsonOutputParser

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log = CustomLogging().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_model() 
        self.parser = JsonOutputParser(pydantic_object= SummaryResponse)
        self.fixing_parser = OutputFixingParser(parser=self.parser, llm=self.llm)
        self.prompt = PROPMT_REGISTRY["document_comparison"]
        self.chain = self.prompt | self.llm | self.parser | self.fixing_parser
        self.log.info("DocumentComparatorLLM initialized with model and parser")
    def compare_documents(self):
        try:
            pass 
        except Exception as e:
            self.log.error(f"Error Occured while compare_documents : {e}")
            raise DocumentPortalException("Error Occured while compare_documents" , sys)
    
    def _format_response(self):
        try:
            pass 
        except Exception as e:
            self.log.error(f"Error Occured while compare_documents : {e}")
            raise DocumentPortalException("Error Occured while compare_documents" , sys)