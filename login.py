'''
Filename            : login.py
Path                : Opening page 
Author              : KIKUGO 
Created             : Dec 2024
Purpose             : Login Control    
Copyright           : All rights Reserved to KIKU 
'''

import streamlit as st
from foi.util import session 
from foi.util.html import htmlPages as html
 

def app(): 
    session.initialize() 
    #print ("Entering App")
    html.show_title()
    if session.get_value(session.LOGGED_IN) :
        #print ("within Header Section - LoggedIn True")
        html.show_logout_page()
        html.show_main_page()
    else :
        #print ("within Header Section - LoggedIn False")
        html.show_login_page()
       

if __name__ == "__main__":
    
    app()