
'''
Filename            : rag_huggingface.py
Path                : util/models
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Interface to HuggingFace  
Copyright           : All rights Reserved to KIKU 
'''

from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models.huggingface import ChatHuggingFace
#from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain_core.prompts.prompt import PromptTemplate

import util.log as log 
import util.pdf as pdf

 
def get_vectorstore(text_chunks):
    log.log_write(f"get_vectorstore -> {type(text_chunks)}" )
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")      
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding = embeddings)
    log.log_write(f"get_vectorstore <- :: vectorstore")
    return vectorstore

def get_conversation_chain(vectorstore) :
    log.log_write(f"get_conversation_chain -> ")
    #memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl",
                                 task= "conversational",
                                 model_kwargs={ "temperature":0.5,"max_length":512})
    #chat_model = ChatHuggingFace(llm=llm)
    template = "Question : {query}"
    prompt = PromptTemplate(template=template, input_variables=["query"])
    conversation_chain = LLMChain(llm=llm, prompt = prompt)

    log.log_write(f"get_conversation_chain :: conversation_chain = {type(conversation_chain)}")
    return conversation_chain


def main() : 
    page_count, chunks = pdf.get_test_pdf_chunks()
    vs = get_vectorstore(chunks)
    print (f"vector store {type(vs)} page count : {page_count} ")
    
    chain = get_conversation_chain(vs) 
    print (f"Chain {type(chain)}")
    query = "What is the capital of Japan?"
    chain.run({ "query": query})


if __name__ == "__main__" :
    main()
