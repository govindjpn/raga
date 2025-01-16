'''
Filename            : htmlPages.py
Path                : util/html 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : All user interface elements  
Copyright           : All rights Reserved to KIKU 
'''

import streamlit as st 
from util.html.htmlTemplates import css, bot_template, user_template, pdf_display
from util.html import label as lbl
from util import session 
from util import user


#headerSection = st.container()
#mainSection = st.container()
#loginSection = st.container()
#logOutSection = st.container()

st_sidebar = st.sidebar 

def view_pdf():    
    view_page = st.Page("pages/3_view.py", title="view")
    st.switch_page(view_page)

def get_chat_history_con (): 
    chat_history_con = st.container(height=500)
    return chat_history_con

def get_button (label): 
    button = st.button(label)
    return button 

def get_checkbox (label, key="", **kwargs):
    if key == "":
        key = label 
    cb = st.checkbox(label, key=key, **kwargs)
    return cb 

def text_input (msg):
    ti = st.text_input(msg)
    return ti 

def text_area (msg):
    ta = st.text_area(msg)
    return ta 

def selectbox (label, options,**kwargs) :
    sb = st.selectbox(label, options,**kwargs)
    return sb 

def pills (label, options, key="", **kwargs): 
    if key == "":
        key = label 
    p = st.pills(label, options,key=key, **kwargs)
    return p 

def tabs (list): 
    tab_tuple = st.tabs(list)
    return tab_tuple

def columns (list): 
    col_tuple = st.columns(list)
    return col_tuple

def file_uploader(label, type, accept_multiple_files):
    fu = st.file_uploader(label, type=type, accept_multiple_files=accept_multiple_files)
    return fu

def show_title(lang="en"): 
    #with headerSection: 
    st.title (lbl.msg(lang, "CHAT_HEADER"))

def set_page_layout(layout):    
    st.set_page_config(layout=layout)

def show_header(lang="en", page_title = "DOCS") :
    switch_page()
    st.set_page_config(page_title=lbl.msg(lang, page_title), page_icon=":books:", 
                        initial_sidebar_state="expanded", layout="wide",
                        menu_items = {
                            'Get help' : 'http://en.wikipedia.org/wiki/insurance',
                            'About': '# Learn the minute details of your insurance documents'
                        }
                    )
    st.write(css, unsafe_allow_html=True)
    st.header(lbl.msg(lang, "CHAT_HEADER")) 

def show_subheader(text): 
    st.subheader(text)


def show_main_page():
    #pass
    #print (f"Before showing main page ")
    #loginSection.empty()
    st.page_link("pages/1_chat.py", label="Chat")
    
def show_view_button():
    st.page_link("pages/3_view.py", label="View")

def show_pdf(doc_id, doc_name, page_num): 
    session.set_value(session.DOC_ID, doc_id)
    session.set_value(session.PDF_FILE_NAME, doc_name)
    session.set_value(session.PDF_PAGE_NUM, page_num)

    session.set_value(session.SWITCH_PAGE, "pages/3_view.py")

def show_id_button(i, doc_id, tooltip, doc_name, page_num):
    button_key = str(i) + "-" + str(doc_id)
    st.button("View", key=button_key, help=tooltip, on_click=show_pdf, args=[doc_id, doc_name, page_num])

def show_error(error_message : str): 
    st.error (error_message)

def show_success(message : str): 
    st.success (message)


def show_message(message : str): 
    st.write (message)

def show_markdown(html_text, unsafe_allow_html): 
    st.markdown (html_text, unsafe_allow_html = unsafe_allow_html)

def show_bot(msg) :
    st.write(bot_template.replace("{{MSG}}", msg), unsafe_allow_html=True)

def show_user(msg) :
    st.write(user_template.replace("{{MSG}}", msg), unsafe_allow_html=True)


def show_login_page(lang="en"): 
    #print ("Entering show_login_page")

    choice = st.selectbox(lbl.msg(lang, "Login / Signup"), ("Login", "Signup")) 
    if choice == "Login":
        #print ("show_login_page :: Choice Login" )
        email = st.text_input(lbl.msg(lang,"Email Address"))
        password = st.text_input(lbl.msg(lang,"Password"), type="password")
        if st.button("Login" ) : 
            #print (f"show_login_page :: Login Clicked {email=} ::{password=} " )
            login_clicked(email, password) 
        #print (f"show_login_page :: {email=} ::{password=} " )
    else : 
        email = st.text_input(lbl.msg(lang,"Email Address"))
        password = st.text_input(lbl.msg(lang,"Password"), type="password")
        verify_password = st.text_input(lbl.msg(lang,"Reenter Password"), type="password")
        username = st.text_input(lbl.msg(lang,"How do we call you?")) 

        if verify_password != password:
            st.error (lbl.msg(lang,"Please reenter password"))
        st.button("Create User", on_click =signup_clicked, args=(email, password, username))
    #print ("Exiting show_login_page")       


def logout_clicked(): 
    session.set_value(session.LOGGED_IN, False) 
    session.set_value(session.USER_ID, "") 
    session.set_value(session.USER_NAME, "")

def show_logout_page(lang="en"): 
    #html.loginSection.empty()
    #with html.logOutSection:
        st.button(lbl.msg(lang,"Logout"), key="logout", on_click=logout_clicked)   


def login_clicked(email, password,lang="en"): 
    #print (f"Login Clicked :: {email=} ")
    if not user.validate_emailID(email) : 
        #print (f"{email=} :: Email not in proper format ")
        session.set_value(session.LOGGED_IN, False) 
        show_error(lbl.msg(lang,"EMAIL_FORMAT_ERROR"))
    else :
        if (user_details := user.get_user (email)) is None: 
            #print (f"{user_details=} :: User not found in DB ")
            session.set_value(session.LOGGED_IN, False) 
            show_error(lbl.msg(lang,"Email / Password incorrect"))
        else : 
            db_hashedpw, user_name, active_flg  = user_details 
            if user.check_password(password, db_hashedpw):
                session.set_value(session.LOGGED_IN, True) 
                session.set_value(session.USER_ID, email) 
                session.set_value(session.USER_NAME, user_name) 
                if active_flg == "Y" :
                    st.rerun() #show_main_page()
                else: 
                    show_error(lbl.msg(lang,"Email / Password incorrect.") )


def signup_clicked(email, password, username,lang="en"): 
    if not user.validate_emailID(email):
        st.error(lbl.msg(lang,"EMAIL_FORMAT_ERROR"))
    else : 
        if not user.validate_username(username):
            show_error(lbl.msg(lang,"NAME_FORMAT_ERROR"))
        else : 
            hashedpw = user.hash_password(password)
            user_id = user.sql_add_user(email, username,  hashedpw, "", "", "")
            session.set_value (session.LOGGED_IN, True) 
            session.set_value (session.USER_ID, email) 
            show_success(lbl.msg(lang,"ACCOUNT_CREATION_SUCCESS"))
            show_main_page()

def switch_page():
    new_page = session.get_value(session.SWITCH_PAGE)
    if new_page is not None and len(new_page) != 0:
        session.set_value(session.SWITCH_PAGE, "")
        st.switch_page(new_page)
