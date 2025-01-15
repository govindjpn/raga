'''
Filename            : 1_foi.py
Path                : util 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Controller of FOI    
Copyright           : All rights Reserved to KIKU 
'''

#import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader


#from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI

# from langchain.chains import ConversationalRetrievalChain
#from langchain_community.llms import OpenAI
#from langchain_community.llms import HuggingFaceHub
# from langchain_community.chat_models.huggingface import ChatHuggingFace
import pandas as pd 
import pickle
import os
from foi.util import log, session, pdf 

from foi.util.html.htmlTemplates import css, bot_template, user_template, pdf_display
from foi.util.html import htmlPages as html 
from foi.util.db import foi_sql_docs as docs



#from foi.util.process.rag_01_chunking import get_chunks
from foi.util.process.rag_02_embedding import get_embeddings, get_vectortore
#from foi.util.process.rag_03_semantic_search import get_search_result
#from foi.util.process.rag_04_reranking import get_reranking
#from foi.util.process.rag_05_prompting import get_prompt
#from foi.util.process.rag_06_consolidation import get_consolidation
from foi.util.process.rag_07_conversation import answer_question # get_conversation_chain, answer_question


def show_pdf (id, **kwargs): 

    log.log_debug(f"1_chat::show_pdf 001 -->  {str(kwargs)}")
    doc_id = int(id[0: id.find("-")])
    doc_page = int(id[id.find("-"):])
    doc_name = docs.sql_get_doc_name(doc_id)
    session.set_value(session.PDF_FILE_NAME, doc_name)
    session.set_value(session.SWITCH_PAGE, "pages/3_view.py")
    # show the PDF on screen using 3_view 
    log.log_debug(f"1_chat::show_pdf 999 <---  ")
    return 

def show_chat_history(container, chat_history): 
    with container : 
        for i, message in enumerate(chat_history): 
            if i%2 == 0 : 
                html.show_user(message)
            else :
                if "(###" in message :
                    id_index = message.find("(###")
                    message_part = message[:id_index]
                    id = message[id_index+4:-4]
                    html.show_bot(message_part)
                    doc_id = int(id[0: id.find("-")])
                    doc_page = int(id[id.find("-")+1:])
                    doc_name = docs.sql_get_doc_name(doc_id)
                    tooltip = f"{doc_name} Page {doc_page}"   
                    html.show_id_button(i, doc_id, tooltip, doc_name, doc_page)                    
                else: 
                    html.show_bot(message)

def handle_userinput (user_question, chat_history_con) : 
    """
    This function is the main controller of the chatbot. It handles a user's input 
    and generates a response based on the conversation history. It also updates the 
    conversation history and stores it in the session. 

    Parameters 
    ----------
    user_question : str 
        The user's input
    chat_history_con : streamlit.container 
        The container where the chat history is displayed

    Notes 
    -----
    This function is called every time the user types a message and presses the 
    send button. It will be called again if the user types another message 
    and presses the send button. 

    The function first retrieves the conversation history from the session. If the
    conversation history is empty, it creates a new conversation chain. 

    The function then processes the user's input and generates a response based 
    on the conversation history. 

    Finally, the function updates the conversation history and stores it in the 
    session. It also displays the chat history in the chat history container. 

    """
    log.log_write(f"handle_userinput 001 --> {user_question}")

    conversation_chain = session.get_value(session.CONVERSATION)
    embedding_model = session.get_value(session.EMBEDDING_MODEL)
    chat_model = session.get_value(session.CHAT_MODEL)
    vectordb = session.get_value(session.VECTORDB)
    chat_history = session.get_value(session.CHAT_HISTORY)
    RAG_flag = session.get_value(session.RAG_FLAG)

    vector_store = get_vectortore(chat_model, vectordb)

    if conversation_chain is None : #   or len(conversation) == 0 :
        ## Create conversation chain 
       
        chat_model = session.get_value(session.CHAT_MODEL)
        vectordb = session.get_value(session.VECTORDB)
        print (f"New Conversation is created {chat_model} :: {vectordb}")
        vector_store = get_vectortore(chat_model, vectordb)
        conversation_chain = "" ## get_conversation_chain(chat_model, vector_store)
        session.set_value(session.CONVERSATION, conversation_chain) 
    log.log_write(f"handle_userinput 002 :: chat history(before) = {chat_history}")
    if user_question is not None and len(user_question) > 0 : 
        response = answer_question(user_question)
        log.log_write(f"handle_userinput 003 :: chat history(after) = {str(response)}")
        if chat_history is not None: 
            chat_history.append(user_question)
        else : 
            chat_history = [user_question]
            log.log_write(f"handle_userinput:: Creating a new Chat history")
        chat_history.append(response)
        session.set_value(session.CHAT_HISTORY, chat_history)
        log.log_write(f"handle_userinput:: chat history(after) = {chat_history}")
    show_chat_history(chat_history_con, chat_history)
    log.log_write(f"handle_userinput <--  {str(chat_history)}")

def clear_chat_history():
    """
    Clear the chat history.

    This function is called when the user wants to start a new conversation.
    It deletes the chat history from the session and sets the chat history
    to an empty list.

    Note: This function does not delete the questions from the database.
    """
    session.set_value(session.CHAT_HISTORY, [])

def load_questions():
    pass

def main() : 
    
    if not (logged_in := session.get_value(session.LOGGED_IN)):
        html.show_error ("Please login through the login page")
        return
    load_dotenv()

    html.show_header()
    chat_history_con = html.get_chat_history_con()
    user_question = html.text_input("Ask any question about your documents")
    if user_question:
        handle_userinput(user_question, chat_history_con)


    with html.st_sidebar: 
        html.show_markdown('<img src="./app/static/images/foi.png" height="50px" />', unsafe_allow_html=True)
        #model = st.selectbox("Select your Model", ("OpenAI", "Gemma", "HuggingFace", "Llama3.1"))
        embedding_model = html.selectbox("Select your Embedding Model", ( "Llama3.1"))
        vectordb = html.selectbox("Select your VectorDB", ("Chroma"))  
        chat_model = html.selectbox("Select your Chat Model", ( "OpenAI", "Llama3.1"))
        RAG_flag = html.get_checkbox("RAG Flag")

        session.set_value(session.EMBEDDING_MODEL, embedding_model)
        session.set_value(session.CHAT_MODEL, chat_model)
        session.set_value(session.VECTORDB, vectordb)
        session.set_value(session.RAG_FLAG, RAG_flag)

        
        
        # st.subheader("Your Policies")
        # pdf_file = st.file_uploader ("Upload your policy documents here and click on Read", accept_multiple_files=False)
        # if st.button ("Read"): 
        #     if not pdf_file :
        #         st.error("Only PDF / TXT files supported. Please load the file again")
        #     else: 
        #         with st.spinner("Reading.."): 
        #             page_count = read_files(pdf_file, model, vectordb)
        #             user_question = f"I have uploaded {pdf_file.name} ({page_count} pages)."
        #             #response = st.session_state.conversation({'question': user_question}) 
        #             user_question = f"Please provide the policy details with the coverage, the insured and risk location"
        #             handle_userinput(user_question, chat_history_con)
         
        clear_button = html.get_button("Clear Button")
        if clear_button: 
            clear_chat_history()


if __name__ == "__main__" :
    main()
