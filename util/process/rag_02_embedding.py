'''
Filename            : rag_02_embedding.py
Path                : util/process 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Embedding Algorithms  
Copyright           : All rights Reserved to KIKU 
'''

import foi.util.log as log 

from langchain_community.embeddings import OpenAIEmbeddings 
#from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_chroma.vectorstores import Chroma 
import ollama 


#import foi.util.models.rag_huggingface as rag_huggingface 
#import foi.util.models.rag_gemma as rag_gemma

from foi.util.vector import vectordb as vdb

def get_embeddings(model, vectordb, text_chunks):
    log.log_write(f"get_embedding ->:: {model=} {vectordb=} {type(text_chunks)} {len(text_chunks)}")
    try : 
        match model : 
            case "OpenAI": 
                embeddings = OpenAIEmbeddings()   
            #case "HuggingFace" : 
            #    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")     
            #case "Gemma" :
            #    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")      
            case "Llama3.1" :
                embeddings = []
                for index, chunk in enumerate(text_chunks): 
                    result = ollama.embeddings(model="mxbai-embed-large", prompt=chunk)
                    embeddings.append(result ["embedding"])
                    #print (f"Get Embeddings Llama 3.1 :: {type(embeddings)} :: {len(embeddings)}  ")
            case _ : 
                embeddings = OpenAIEmbeddings()        
             
        log.log_write(f"get_vectorstore <- :: {type(embeddings) }  {len(embeddings)}")
        return embeddings
    except Exception as e : 
        log.log_write(f"get_embedding Exception :: {e}") 
        print (f"get_embedding Exception :: {e}")
        return None
    

def get_vectortore(model, vectordb): 
    return vdb.get_vectorstore(model, vectordb)