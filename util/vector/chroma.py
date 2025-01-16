
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from chromadb.utils import embedding_functions
from langchain_chroma.vectorstores import Chroma
from langchain_community.embeddings.openai import OpenAIEmbeddings


from util import log

'''
By default, Chroma uses Sentence Transformers all-MiniLM-L6-v2 model to create embeddings 
  default_ef = embedding_functions.DefaultEmbeddingFunction()
embedding functions can be linked to a collection and used whenever you call add, update, upsert or query   

'''
embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2") 
oai_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

#embeddings = embedding_functions.DefaultEmbeddingFunction
vectorstore = Chroma("langchain_store", embeddings)
oai_vectorstore = Chroma("langchain_store", oai_embeddings)
retriever = vectorstore.as_retriever()
from raga.util import config as cfg

chromadb_path = cfg.HOME + cfg.path[cfg.CHROMA_DB]  
client = chromadb.PersistentClient(
    path=chromadb_path,
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

#print (f"Collections = {client.list_collections()}")
collection = client.get_or_create_collection(name="docs")
vectorstore = Chroma(collection_name="docs", embedding_function=embeddings, client=client)

def embed_and_add (vectordb, ids, docs, metadatas) : 
    log.log_write(f"add_embeddings --> {vectordb=} {ids=}")

    collection.add(ids=ids, documents=docs, metadatas=metadatas) 

def add_embeddings (vectordb, ids, embeddings, documents, metadatas) : 
    log.log_write(f"add_embeddings ==> {vectordb=} {ids=}")
    existing_id = collection.get (ids = ids)
    if existing_id is not None: 
        collection.add(ids=ids, embeddings=embeddings, documents= documents, metadatas=metadatas) 
    else : 
        log.log_write(f"add_embeddings (#001) :  {ids=} Already added")

    log.log_write(f"add_embeddings <== {vectordb=} {ids=}")

def delete_item (item):
    collection.delete(item)

def list_collections(): 
    return client.list_collections()

def get_vectorstore(model_name): 
    # Chroma(collection_name="docs", embedding_function=embeddings, client=client)
    match model_name : 
        case "OpenAI": 
            return oai_vectorstore
        case _ : 
            return vectorstore


def get_vectorstore_retriever(): 
    # Chroma(collection_name="docs", embedding_function=embeddings, client=client)
    return retriever

def semantic_search (question, question_embeddings, n_results = 1): 
    if question_embeddings is None : 
        results = collection.query (
            query_texts=question,
            n_results = n_results
            )
    else :
        results = collection.query (
            query_embeddings=question_embeddings,
            n_results = n_results
            )

    return results
