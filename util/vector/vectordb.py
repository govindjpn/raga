
## change to a class implementation later 

from util.vector import chroma

def create_collection(vectordb, doc_name) :
    match vectordb :
        case "chroma" : 
            collection = chroma.create_collection(vectordb, doc_name)
        case _ :
            collection = chroma.create_collection(vectordb, doc_name)
    return collection 

def add_embeddings(vectordb, ids, embeddings, documents, metadatas) : 
    match vectordb :
        case "chroma" : 
            chroma.add_embeddings(vectordb,  ids, embeddings, documents, metadatas)
        case _ :
            chroma.add_embeddings(vectordb, ids, embeddings, documents, metadatas)
    return None

def store(vectordb, collection) : 
    match vectordb :
        case "chroma" : 
            chroma.store(vectordb, collection)
        case _ :
            chroma.store(vectordb, collection)
    return None 

def get_vectorstore(model_name, vectordb): 
     match vectordb :
        case "chroma" : 
            return chroma.get_vectorstore(model_name)
        case _ :
            return chroma.get_vectorstore(model_name)
         
def semantic_search(vectordb, user_question, question_embeddings = None, n_results = 1) : 
    match vectordb : 
        case "chroma" : 
            return chroma.semantic_search (user_question, question_embeddings, n_results)
        case _ :
            return chroma.semantic_search (user_question, question_embeddings, n_results)
            
