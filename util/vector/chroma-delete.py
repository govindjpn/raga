import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

from foi.util import config as cfg

chromadb_path = cfg.HOME + cfg.path[cfg.CHROMA_DB]  
client = chromadb.PersistentClient(
    path=chromadb_path,
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

def delete_specific_collection(collection_name): 
    local_collection = client.get_or_create_collection(name=collection_name)
    if local_collection is None : 
        print(f"Collection {collection_name} not available")
    else : 
        client.delete_collection(name=collection_name)
        print(f"Collection {collection_name} Deleted")

print (f"Collections = {client.list_collections()}")
coll_name  = input(f"Please enter the name of the collection to be deleted: ")
delete_specific_collection(coll_name)

