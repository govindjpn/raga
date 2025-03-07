'''
Filename            : 2_cabinet.py
Path                : util 
Author              : KIKUGO 
Created             : Oct 2024
# Purpose           : Cabinet List  
Copyright           : All rights Reserved to KIKU 
'''

import streamlit as st 


from util import session, log, pdf
from util.html import htmlPages as html 
from util.db import sql_docs as docs



from util.process.rag_01_chunking import get_chunks
from util.process.rag_02_embedding import get_embeddings  # , get_vectortore
#from util.process.rag_07_conversation import get_conversation_chain

from util.vector import vectordb as vdb

#from util.models import rag_llama31 as llm

col_docs, col_summary = html.columns([4, 1])


def read_files(pdf_file, model, vectordb): 
    
    ## get PDF text   raw_text is a dictionary with page number : raw_text 
    ##                doc_id is the unique id for the document read 
    raw_text_dic, doc_info = pdf.get_pdf_text(pdf_file)

    doc_id = docs.sql_add_doc(doc_info) 


    raw_text = "".join(raw_text_dic[key] for key in raw_text_dic.keys())
    ## 01 Chunking divide text to chunks 
    text_chunks = get_chunks(doc_id, raw_text)

    ## create a vector store with the embeddings 
    embeddings = get_embeddings(model, vectordb, text_chunks)
    
    ids = []
    metadatas = []
    for index, embedding in enumerate(embeddings): 
        ids.append(f"{doc_id}-{index}")
        metadatas.append({"source": f"{doc_id}-{pdf_file.name}-{index}"})
    #metadata_dict = {"source": str(metadatas)}
    vdb.add_embeddings (vectordb, ids, embeddings, text_chunks,  metadatas)

    #vectorstore = FAISS.from_texts(text=text_chunks, embedding = embeddings)
    page_count = len(raw_text_dic.keys())
    return page_count


def show_load_menu() :     
    with html.st_sidebar: 
        html.show_subheader("Your Documents")
        embedding_model = session.get_value(session.EMBEDDING_MODEL)
        chat_model = session.get_value(session.CHAT_MODEL)
        vectordb = session.get_value(session.VECTORDB)    
        if embedding_model is None : 
            return    
        html.show_message(f"Embedding : {embedding_model} Vector DB : {vectordb}")
        pdf_file = html.file_uploader ("Upload your document here and click on Read", type=["pdf", "txt"], 
                                       accept_multiple_files=False)
        log.log_debug(f"show_load_menu File : {pdf_file}")
        if not pdf_file :
                st.error("Only PDF / TXT files supported. Please load the file again")
        else : 
            read_button = html.get_button("Read")
            if read_button: 
                with st.spinner("Reading.."):              
                    page_count = read_files(pdf_file, embedding_model, vectordb)
                    #result = llm.summarize_file(pdf_file, "stuff")
                    #docs.sql_update_summary()

def show_table(docs_list) : 
    with col_docs: 
        #docs_addl_df = docs.sql_get_doc_list(user_id, "ADDL")
        #state_set = sorted(set(list(docs_addl_df["state"])))

        selected_row = st.dataframe(
                docs_list,
                column_config={
                    "name" : st.column_config.Column(
                                "Document File Name",
                                help="File name as uploaded by the owner",
                                width="medium",
                                required=True,
                                ),
                    "id" :  None 
                },
                hide_index=True,
                use_container_width=True,
                selection_mode="single-row",
                on_select="rerun"
                )
        log.log_debug(f"Selected Row : {str(selected_row)}")
        if selected_row.selection.rows  is not None and len(selected_row.selection.rows) > 0 :
            selected_file = docs_list[selected_row.selection.rows[0]] ["name"] 
            selected_id = docs_list[selected_row.selection.rows[0]]["id"] 
        else : 
            selected_file = None
            
        log.log_debug (f"Selected File : {selected_file}")
        if selected_file is not None and len(selected_file) > 0 : 
            log.log_debug(f"ID : {selected_id=} {selected_file=}")
            session.set_value(session.PDF_FILE_NAME, selected_file)
            session.set_value(session.DOC_ID, selected_id)
            
            html.show_view_button()
            if (summary := docs.sql_get_doc_summary(selected_id)) is not None:
                show_summary(summary)
            delete_button = html.get_button("Delete")
            if delete_button: 
                ## get the user to type the file name explicitly for confirmation 
                html.show_message("Are you sure you want to delete this file?")
                file_name = html.get_text_input("Please type the file name to confirm the deletion")                
                if file_name == selected_file :
                        docs.sql_delete_doc(selected_id)
                

def show_summary(summary=None): 
    with col_summary : 
        html.show_markdown("<h1>Summary<h1>", unsafe_allow_html=True)
        if summary is None : 
            html.show_message("Please double click on a row to see the summary")
        else : 
            html.show_message(summary)
            
if __name__ == "__main__" :

    if not (logged_in := session.get_value(session.LOGGED_IN)):
        html.show_error ("Please login through the login page")
    else :
        show_load_menu()
        user_id = session.get_value(session.USER_ID)
        if user_id is None: 
            st.error("Please Login again to see the file list ")
        else :
            if ( docs_list := docs.sql_get_doc_list(user_id)) is None:   
                st.error("No files to show; please upload a file using the read button")
            else :   
                show_table(docs_list)
   


