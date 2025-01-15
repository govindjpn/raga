#import pickle 
import streamlit as st 
import load_dotenv
import re, string
import random 
import bcrypt 

import smtplib
from email.mime.text import MIMEText
from foi.util.db.foi_sql_user import sql_get_user, sql_add_user

#user_dict = pickle.load(open("user_dict.pkl","rb"))
#def sql_add_user (email, hashedpw, username,active_flag) :
#    user_dict[email] = (hashedpw, username, active_flag)
#    pickle.dump (open("user_dict.pkl","wb",encoding="utf-8"))

def get_user (email) :
   # user_password, user_name, user_active_flg
   return sql_get_user (email)

def add_user(user_id, user_name, user_password, user_role, user_group, user_external_id):
    return sql_add_user(user_id, user_name, user_password, user_role, user_group, user_external_id)


def create_strong_password(pw_len:int = 16) :
    # starts with a letter and ends with a letter 
    letter =  string.ascii_letters
    scope = string.ascii_letters + string.digits + "!#_-@" 
    password = random.choice(letter) + ''.join(random.choice(scope) for i in range(pw_len - 2)) + random.choice(letter)
    return password


def send_password_reset_mail (to_email ):
    # Taking inputs
    SENDER_EMAIL = ""
    SENDER_PASSWORD = ""
    load_dotenv()
    email_sender = SENDER_EMAIL
    email_receiver = to_email
    subject = "Password Reset Request"
    body = ""
    password = SENDER_PASSWORD 

    if st.button("Send Email"):
        try:
            msg = MIMEText(body)
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg['Subject'] = subject

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_sender, password)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()
        
            st.success('Email sent successfully! 🚀')
        except Exception as e:
            st.error(f"Error in sending EMail : {e}")

def validate_username(username:str): 
    regexp = r"^[a-zA-Z0-9_-]{1,20}$"  
    # ^ to negate, [] Square braces for disjunction of characters 
    # {} curly braces for counter $ matches end of line 
    return bool(re.match(regexp, username))

def validate_emailID(emailID: str): 
    regexp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' 
    # \b word boundary ^ to negate, {} for counter $ matches end of line 
    return bool(re.match(regexp, emailID))

def hash_password(pw:str): 
    # https://en.wikipedia.org/wiki/Bcrypt
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def check_password(pw: str, hash:str): 
    # https://en.wikipedia.org/wiki/Bcrypt
    return bcrypt.checkpw(bytes(pw,"utf-8"), bytes(hash,"utf-8"))

