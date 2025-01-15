
from foi.util.process.rag_01_chunking import get_chunks
from foi.util.process.rag_02_embedding import get_embeddings 

from foi.util import session, log, pdf 
from foi.util.vector import vectordb as vdb

def read_files(pdf_file, model, vectordb): 
    
    ## get PDF text   raw_text is a dictionary with page number : raw_text 
    ##                doc_id is the unique id for the document read 
    raw_text_dic, doc_id = pdf.get_pdf_text(pdf_file)

    raw_text = "".join(raw_text_dic[key] for key in raw_text_dic.keys())
    ## 01 Chunking divide text to chunks 
    text_chunks = get_chunks(doc_id, raw_text)

    ## create a vector store with the embeddings 
    embeddings = get_embeddings(model, vectordb, text_chunks)
    
    ids = []
    metadatas = []
    for index, embedding in enumerate(embeddings): 
        ids.append(f"{doc_id}-{index}")
        metadatas.append(f"{doc_id}-{pdf_file.name}-{index}")
    metadata_dict = {"source": str(metadatas)}
    vdb.add_embeddings (vectordb, ids, embeddings, text_chunks,  metadata_dict)

    #vectorstore = FAISS.from_texts(text=text_chunks, embedding = embeddings)
    page_count = len(raw_text_dic.keys())
    return page_count