'''
Filename            : rag_03_semantic_search.py
Path                : util/process 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Semantic Search Algorithms  
Copyright           : All rights Reserved to KIKU 
'''

from raga.util.vector.vectordb import semantic_search

def get_search_result(vectordb, question, n_results = 1): 
    results = semantic_search (vectordb, question, n_results)
    return results 
