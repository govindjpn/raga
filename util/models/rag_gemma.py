'''
Filename            : rag_gemma.py
Path                : util/models 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Interface to Gemma  
Copyright           : All rights Reserved to KIKU 
'''


#from langchain_community.embeddings import HuggingFaceInstructEmbeddings
#from langchain.vectorstores import FAISS
#from langchain_community.llms import HuggingFaceHub
#from langchain_community.chat_models.huggingface import ChatHuggingFace
#from langchain.memory import ConversationBufferMemory
#from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
import pandas as pd 
import pickle
import os
import util.log as log 
import ollama



def get_conversation_chain(vectorstore) :
    log.log_write(f"get_conversation_chain -> ")
    #memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    llm = ollama(model="gemma")
    #chat_model = ChatHuggingFace(llm=llm)
    conversation_chain = load_qa_chain(llm=llm, chain_type="stuff")
    log.log_write(f"get_conversation_chain :: conversation_chain = {type(conversation_chain)}")
    return conversation_chain


def main() : 
    cc = get_conversation_chain("vs")
    print ("Converstation Chain = " , cc)

if __name__ == "__main__" :
    main()
