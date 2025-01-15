import streamlit as st 

CHAT_HISTORY = "chat_history"
CHAT_HISTORY1 = "chat_history1"
CHAT_HISTORY2 = "chat_history2"
CHAT_MODEL = "chat_model"
CONVERSATION = "conversation"
DOC_ID = "doc_id"
DOCS_DF = "docs_df"
EMBEDDING_MODEL = "embedding_model"
LOGGED_IN = "logged_in"
PDF_FILE_NAME = "pdf_file_name"
PDF_PAGE_COUNT = "pdf_page_count"
PDF_PAGE_NUM = "pdf_page_num"
USER_ID = "user_id"
USER_NAME = "user_name"
VECTORDB = "vectordb"
RAG_FLAG = "RAG_flag"
SWITCH_PAGE = "switch_page"

session_keys = [CHAT_HISTORY, 
                CHAT_HISTORY1, 
                CHAT_HISTORY2, 
                CHAT_MODEL, 
                CONVERSATION, 
                DOC_ID,
                DOCS_DF, 
                EMBEDDING_MODEL, 
                LOGGED_IN, 
                PDF_FILE_NAME, 
                PDF_PAGE_COUNT,
                PDF_PAGE_NUM, 
                RAG_FLAG,
                SWITCH_PAGE,
                USER_ID, 
                USER_NAME, 
                VECTORDB
                ]

def initialize () :
    if LOGGED_IN not in st.session_state.keys() : 
        #print ("initializing ...")
        st.session_state[CHAT_HISTORY] = None
        st.session_state[CHAT_HISTORY1] = None
        st.session_state[CHAT_HISTORY2] = None
        st.session_state[CHAT_MODEL] = ""
        st.session_state[CONVERSATION] = None
        st.session_state[DOC_ID] = None
        st.session_state[DOCS_DF] = None
        st.session_state[EMBEDDING_MODEL] = ""
        st.session_state[LOGGED_IN] = False
        st.session_state[PDF_FILE_NAME] = ""
        st.session_state[PDF_PAGE_COUNT] = ""
        st.session_state[PDF_PAGE_NUM] = 0
        st.session_state[RAG_FLAG] = False
        st.session_state[SWITCH_PAGE] = ""
        st.session_state[USER_ID] = ""
        st.session_state[USER_NAME] = ""
        st.session_state[VECTORDB] = ""
        

def set_value(key, value) :
    if key in session_keys :    
        st.session_state[key] = value 
    else :
        return None 

def get_value(key) :
    if key in session_keys and key in st.session_state.keys():    
        return st.session_state[key]
    else :
        return None 
