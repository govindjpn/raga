'''
Filename            : 4_question.py
Path                : util 
Author              : KIKUGO 
Created             : Dec 2024
Purpose             : Question Loader of FOI    
Copyright           : All rights Reserved to KIKU 
'''

from util import log, session 
from util.html import htmlPages as html  
from util.db import sql_docs as docs
from util.process import rag_07_conversation as rag 


def load_questions(question_file): 
    with open(question_file, "r", encoding="utf-8") as f:
        return f.readlines()



def show_chat_history(container, chat_history): 
    with container : 
        container.empty()
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
    


    
def run_questions (container, questions, model, RAG_flag):
    ## Embedding model is always assumed to be llama 
    session.set_value(session.EMBEDDING_MODEL, "Llama3.1")
    session.set_value(session.CHAT_MODEL, model)
    session.set_value(session.RAG_FLAG, RAG_flag)
    
    chat_history = []
    if len(questions) > 0 and len(questions[0]) > 0: 
        for question in questions :
            chat_history.append(question)
            response = rag.answer_question(question)
            chat_history.append(response)
    show_chat_history(container, chat_history)
    return chat_history


col_1, col_2 = html.columns([2,2])

def show_questions ():
    questions = [] 
    with html.st_sidebar: 
        question_file = html.file_uploader("Upload your Questions and click on Load", ["txt"], accept_multiple_files=False)
        load_button = html.get_button("Load")
        if load_button: 
            questions = load_questions(question_file)
        else : 
            user_question = html.text_area("Ask any question about your documents")
            questions = [user_question]
    with col_1 :
        RAG_flag1 = html.get_checkbox("RAG Flag", "RAG_flag1")
        chat_model1 = html.pills("Select your Chat Model", ("OpenAI", "Llama3.1"), "chat_model1", default="OpenAI")
        chat_history_con1 = html.get_chat_history_con()
        if (chat_history1 := session.get_value(session.CHAT_HISTORY1)) is not None :
            show_chat_history(chat_history_con1, chat_history1)
       

    with col_2 :
        RAG_flag2 = html.get_checkbox("RAG Flag", "RAG_flag2", value=True)
        chat_model2 = html.pills("Select your Chat Model", ("Llama3.1","OpenAI"), "chat_model2", default="OpenAI")
        chat_history_con2 = html.get_chat_history_con()
        if (chat_history2 := session.get_value(session.CHAT_HISTORY2)) is not None :
            show_chat_history(chat_history_con2, chat_history2)
        
    with col_1 :    
        if len(questions) > 0 and len(questions[0]) > 0: 
            chat_history1 = run_questions (chat_history_con1, questions, chat_model1, RAG_flag1)
            session.set_value(session.CHAT_HISTORY1, chat_history1)

    with col_2 :
        if len(questions) > 0 and len(questions[0]) > 0: 
            chat_history2 = run_questions (chat_history_con2, questions, chat_model2, RAG_flag2)
            session.set_value(session.CHAT_HISTORY2, chat_history2)


if __name__ == "__main__": 
    
    if not (logged_in := session.get_value(session.LOGGED_IN)):
        html.show_error ("Please login through the login page")
    else :
        html.switch_page()
        show_questions()

