import os 
from langchain_core.output_parsers import JsonOutputParser 
from langchain.output_parsers import OutputFixingParser
from model.models import *
from utils.models_loader import ModelLoader
from logger.custom_logger import CustomLogging
from exception.custom_exception import DocumentPortalException


class DocumentAnalyzer:
    """
        Analysis Data as per PreTrained Model
        Automatically log all the actions and supports session-based organization.
    """
    def __init__(self):
        pass  
    def analyze_metadata(self):
        pass