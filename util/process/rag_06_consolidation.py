'''
Filename            : rag_06_consolidation.py
Path                : util/process 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : ConsolidationAlgorithms  
Copyright           : All rights Reserved to KIKU 
'''

from util import log 

def get_consolidation (responses) :
    log.log_debug(f"get_consolidation -> :: {type(responses)} :: {str(responses)}")

    gc_response = responses[0]

    log.log_debug(f"get_consolidation <- :: {type(gc_response)} :: {str(gc_response)}")
    return gc_response 