'''
Filename            : rag_01_chunking.py
Path                : util/process 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Chunking Algorithms  
Copyright           : All rights Reserved to KIKU 
'''

## 
# Token-based chunking: LangChain’s CharacterTextSplitter using tiktoken
#   Tokens in chunk: 80
#   Tokenizer: cl100k_base
# Recursive 
#   RecursiveCharacterTextSplitter, RecursiveJsonSplitter 
# HTML 
#   splits text based on HTML-specific Characters 
# Sentence-based chunking: 4 sentences per chunk
# Clustering with k-means: sklearn’s KMeans:
#   Number of clusters: 3
# Semantic chunking percentile-based: 
#   LangChain implementation of SemanticChunker with percentile 
#   breakpoint with values for breakpoint 50/60/70/80/90
# Semantic chunking double-pass merging:
#   initial_threshold: 0.7
#   appending_threshold: 0.8
#   merging_treshold: 0.7
#   spaCy model: en_core_web_md


from langchain.text_splitter import CharacterTextSplitter

import util.log as log 
from util.db import sql_docs as docs 


def get_chunks (doc_id, raw_text) :  
    log.log_write(f"Entering get_text_chunks :: {len(raw_text)}")
    text_splitter  = CharacterTextSplitter(
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
    )
    chunks = text_splitter.split_text(raw_text)    
    ## store chunks in doc_chunks table 
    chunk_dic = {}
    for index, chunk in enumerate (chunks) : 
        docs.sql_add_doc_chunk (doc_id, index, chunk)
        chunk_dic[index] = len(chunk)     
    log.log_write(f"Exiting get_text_chunks :: {str(chunk_dic)}")

    return chunks 