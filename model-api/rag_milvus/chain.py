"""
Langchain chain for RAG model with Milvus
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.chat_models import ChatOllama
import langchain

from .prompt import llama_prompt_template
from .retriever import vector_db

langchain.verbose = True

prompt = ChatPromptTemplate.from_template(llama_prompt_template)

retriever = vector_db.as_retriever()

ollama = ChatOllama(model="tinyllama:1.1b-chat")

chain = (
    RunnableParallel({"context": retriever, "message": RunnablePassthrough()})
    | prompt
    | ollama
    | StrOutputParser()
)
