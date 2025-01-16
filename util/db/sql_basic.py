'''
Filename            : foi_sql_basic.py
Path                : util/db 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : basic sql functions    
Copyright           : All rights Reserved to KIKU 
'''

import sqlite3 as sl
from util import config as cfg
from util.log import log_error, log_warning, log_debug

#DB_name = cfg.HOME + cfg.path[cfg.DB] + cfg.filename[cfg.DB]
DB_name = "db/docs.db"
try :
    con = sl.connect(DB_name , check_same_thread=False)
    cur = con.cursor()
    print (f"DB = {DB_name} : File open success; sqlite Version {sl.sqlite_version} ")
except Exception as E :
    print (f"DB = {DB_name} : File open failed {E}")


def commit ():
     con.commit()

def get_one(select_str :str, parameters : dict = None) -> tuple : 
    if parameters is not None : 
        cur.execute(select_str, parameters)
    else : 
        cur.execute(select_str) 
    return cur.fetchone()

def get_all(select_str :str, parameters : dict = None) -> list : 
    if parameters is not None: 
        cur.execute(select_str, parameters)
    else : 
        cur.execute(select_str) 
    return cur.fetchall()

def insert (insert_str: str, commit_flg = True) -> None: 
    cur.execute(insert_str)
    if commit_flg:
        con.commit()
def update (update_str: str, commit_flg = True) -> None: 
    cur.execute(update_str)
    if commit_flg:
        con.commit()
def delete (delete_str: str, commit_flg = True) -> None: 
    cur.execute(delete_str)
    if commit_flg:
        con.commit()

