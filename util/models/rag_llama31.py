'''
Filename            : rag_llama31.py
Path                : util/process 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Interface to llama31   
Copyright           : All rights Reserved to KIKU 
'''

from datetime import datetime as dt
import glob


#from langchain_community.embeddings import HuggingFaceInstructEmbeddings
#from langchain_community.vectorstores import FAISS
#from langchain_community.llms import HuggingFaceHub
#from langchain_community.chat_models.huggingface import ChatHuggingFace
#from langchain.memory import ConversationBufferMemory
#from langchain.chains import ConversationalRetrievalChain
#from langchain.chains.question_answering import load_qa_chain
#from langchain_community.llms import Ollama
from langchain_community.document_loaders.pdf import PyPDFLoader
# Define LLM Chain
from langchain.chains.llm import LLMChain
# Prompt
from langchain_core.prompts import PromptTemplate
# Create full chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain


from langchain_ollama import ChatOllama
llm = ChatOllama(
        model="llama3.1",
        temperature=0,
        # other params...
    )


import foi.util.log as log 


def get_conversation_chain(vectorstore) :
    log.log_write(f"get_conversation_chain -> ")
    #memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    #llm = Ollama(model="llama3.1")
    conversation_chain = None   # load_qa_chain(llm=llm, chain_type="stuff")
    log.log_write(f"get_conversation_chain :: conversation_chain = {type(conversation_chain)}")
    return conversation_chain


def summarize_file(pdf_file, method): 
    loader = PyPDFLoader(pdf_file)
    document = loader.load()
    prompt_template = """Write a short summary of the following document not exceeding 100 words. 
                        Only include information that is part of the document. 
                        Do not include your own opinion or analysis.
                    Document:
                    "{document}"
                    Summary:"""
    prompt = PromptTemplate.from_template(prompt_template)
   
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="document"
    )
    result = stuff_chain.invoke(document)
    return result 





if __name__ == "__main__" :
    start_time = dt.now()
    print(start_time.strftime("%d/%m/%Y %H:%M:%S %f"), ": Main : Starting Execution")

    

    end_time = dt.now()
    print(end_time.strftime("%d/%m/%Y %H:%M:%S %f"), ": Main : Completed Execution (", end_time - start_time, ")")
    