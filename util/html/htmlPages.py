'''
Filename            : htmlPages.py
Path                : util/html 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : All user interface elements  
Copyright           : All rights Reserved to KIKU 
'''

import streamlit as st 
from foi.util.html.htmlTemplates import css, bot_template, user_template, pdf_display
from foi.util import session 
from foi.util import user


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

def show_title(): 
    #with headerSection: 
    st.title ("Friends of Insurance")

def set_page_layout(layout):    
    st.set_page_config(layout=layout)

def show_header(page_title = "Know your Insurance") :
    switch_page()
    st.set_page_config(page_title=page_title, page_icon=":books:", 
                        initial_sidebar_state="expanded", layout="wide",
                        menu_items = {
                            'Get help' : 'http://en.wikipedia.org/wiki/insurance',
                            'About': '# Learn the minute details of your insurance documents'
                        }
                    )
    st.write(css, unsafe_allow_html=True)
    st.header("Chat with your Documents :books:")

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


def show_login_page(): 
    #print ("Entering show_login_page")

    choice = st.selectbox("Login / Signup", ("Login", "Signup")) 
    if choice == "Login":
        #print ("show_login_page :: Choice Login" )
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        if st.button("Login" ) : 
            #print (f"show_login_page :: Login Clicked {email=} ::{password=} " )
            login_clicked(email, password) 
        #print (f"show_login_page :: {email=} ::{password=} " )
    else : 
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        verify_password = st.text_input("Reenter Password", type="password")
        username = st.text_input("How do we call you?") 

        if verify_password != password:
            st.error ("Please reenter password")
        st.button("Create User", on_click =signup_clicked, args=(email, password, username))
    #print ("Exiting show_login_page")       


def logout_clicked(): 
    session.set_value(session.LOGGED_IN, False) 
    session.set_value(session.USER_ID, "") 
    session.set_value(session.USER_NAME, "")

def show_logout_page(): 
    #html.loginSection.empty()
    #with html.logOutSection:
        st.button("Logout", key="logout", on_click=logout_clicked)   


def login_clicked(email, password): 
    #print (f"Login Clicked :: {email=} ")
    if not user.validate_emailID(email) : 
        #print (f"{email=} :: Email not in proper format ")
        session.set_value(session.LOGGED_IN, False) 
        show_error("Please enter the email ID in the format <user>@<domain>.<suffix>")
    else :
        if (user_details := user.get_user (email)) is None: 
            #print (f"{user_details=} :: User not found in DB ")
            session.set_value(session.LOGGED_IN, False) 
            show_error("Email / Password incorrect") 
        else : 
            db_hashedpw, user_name, active_flg  = user_details 
            if user.check_password(password, db_hashedpw):
                session.set_value(session.LOGGED_IN, True) 
                session.set_value(session.USER_ID, email) 
                session.set_value(session.USER_NAME, user_name) 
                if active_flg == "Y" :
                    st.rerun() #show_main_page()
                else: 
                    show_error("Email / Password incorrect.") 


def signup_clicked(email, password, username): 
    if not user.validate_emailID(email):
        st.error("Please enter the email ID in the format <user>@<domain>.<suffix>")
    else : 
        if not user.validate_username(username):
            show_error("Please enter the name within 20 characters")
        else : 
            hashedpw = user.hash_password(password)
            user_id = user.sql_add_user(email, username,  hashedpw, "", "", "")
            session.set_value (session.LOGGED_IN, True) 
            session.set_value (session.USER_ID, email) 
            show_success("Account Created successfully")
            show_main_page()

def switch_page():
    new_page = session.get_value(session.SWITCH_PAGE)
    if new_page is not None and len(new_page) != 0:
        session.set_value(session.SWITCH_PAGE, "")
        st.switch_page(new_page)
