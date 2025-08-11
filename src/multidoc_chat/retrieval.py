import sys
import os
from typing import List , Optional
from operator import itemgetter
from pathlib import Path
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from utils.models_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogging
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

class ConversationalRAG:
    def __init__(self,session_id , retriver = None):
        try:
            self.log = CustomLogging().get_logger(__name__)
            self.session_id = session_id
            self.llm = self._load_llm()
            self.contextualize_prompt = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            if retriver is None:
                raise ValueError("retriver cannot be None")
            self.retriver = retriver
            self._build_lcel_chain()
            self.log.info("ConversationalRAG initalized" , session_id = self.session_id)
        except Exception as e:
            self.log.error("Failed in Initalization" , error = str(e))
            raise DocumentPortalException(e, sys)
    def retriever_drom_faiss(self , index_path):
        try:
            embedding = ModelLoader().load_embedding()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found: {index_path}")
            vectorstore = FAISS.load_local(index_path, 
                                           embedding,
                                           allow_dangerous_deserialization=True)
            self.retriver = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            self._build_lcel_chain()
            return self.retriver
        except Exception as e:
            self.log.error("Failed in retriever_drom_faiss" , error = str(e))
            raise DocumentPortalException(e, sys)
    
    def invoke(self):
        try:
            pass 
        except Exception as e:
            self.log.error("Failed in invoke" , error = str(e))
            raise DocumentPortalException(e, sys)
    
    def _load_llm(self):
        try:
            llm = ModelLoader().load_model()
            if llm is None:
                raise ValueError("LLM cannot be None")
            self.log.info("LLM loaded" , session_id = self.session_id)
            return llm 
        except Exception as e:
            self.log.error("Failed in load llm" , error = str(e))
            raise DocumentPortalException(e, sys)
    @staticmethod
    def _format_docs(docs):
        try:
            return "\n\n".join([d.page_content for d in docs]) 
        except Exception as e:
            raise DocumentPortalException(e, sys)
    
    def _build_lcel_chain(self):
        try:
            question_rewriter = (
                {"input" : itemgetter("input"),"chat_history": itemgetter("chat_history")}|
                self.contextualize_prompt
                |self.llm
                |StrOutputParser
            )
            retrived_docs = question_rewriter | self.retriver | self._format_docs
            self.chain =(
                {
                    "context" : retrived_docs,
                    "input" : itemgetter("input"),
                    "chat_history": itemgetter("chat_history")
                }
                |self.qa_prompt
                |self.llm
                |StrOutputParser
            ) 
        except Exception as e:
            self.log.error("Failed in build lcel chain" , error = str(e))
            raise DocumentPortalException(e, sys)
    