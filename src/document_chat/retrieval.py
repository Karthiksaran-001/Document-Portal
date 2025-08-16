import sys
import os
from typing import List , Optional 
from langchain_core.messages import BaseMessage
from operator import itemgetter
from pathlib import Path
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from utils.models_loader import ModelLoader
from exception.custom_exception_archieve import DocumentPortalException
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
            return self.retriver
        except Exception as e:
            self.log.error("Failed in retriever_drom_faiss" , error = str(e))
            raise DocumentPortalException(e, sys)
    
    def invoke(self,user_input:str , chat_history : Optional[List[BaseMessage]] = None):
        
        try:
            if chat_history is None:
                chat_history = []
            payload = {
                    "input" : user_input,
                    "chat_history" : chat_history}
            answer = self.chain.invoke(payload) 
            if answer is None:
                self.log.warning("Answer is None" ,input = user_input ,session_id = self.session_id)
                return "No answer found"
            self.log.info("Answer generated" , session_id = self.session_id, input = user_input , answer_preview = answer[:100])
            return answer
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
            # 1) Rewrite question using chat history
            question_rewriter = (
                {"input": itemgetter("input"), "chat_history": itemgetter("chat_history")}
                | self.contextualize_prompt
                | self.llm
                | StrOutputParser()
            )

            # 2) Retrieve docs for rewritten question
            retrieve_docs = question_rewriter | self.retriver | self._format_docs

            # 3) Feed context + original input + chat history into answer prompt
            self.chain = (
                {
                    "context": retrieve_docs,
                    "input": itemgetter("input"),
                    "chat_history": itemgetter("chat_history"),
                }
                | self.qa_prompt
                | self.llm
                | StrOutputParser()
            )

            self.log.info("LCEL graph built successfully", session_id=self.session_id)

        except Exception as e:
            self.log.error("Failed to build LCEL chain", error=str(e), session_id=self.session_id)
            raise DocumentPortalException("Failed to build LCEL chain", sys)
