import sys
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.models_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogging
from prompt.prompt_library import PROPMT_REGISTRY
from model.models import PromptType

class ConversationalRAG:
    def __self__(self):
        try:
            self.log = CustomLogging().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed in Initalization" , error = str(e))
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed in load llm" , error = str(e))
            raise DocumentPortalException(e, sys)
    
    def _get_session_history(self,session_id):
        try:
            pass 
        except Exception as e:
            self.log.error("Failed in get session history",session_id = session_id , error = str(e))
            raise DocumentPortalException(e, sys)
        
    def load_retriver_faiss(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed in load retriver faiss" , error = str(e))
            raise DocumentPortalException(e, sys)
        
    def invoke(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed in invoke" , error = str(e))
            raise DocumentPortalException(e, sys)
        
    