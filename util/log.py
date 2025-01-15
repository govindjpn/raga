'''
Filename            : config.py
Path                : util 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Manage the folder configuration of FOI    
Copyright           : All rights Reserved to KIKU 
'''

import logging
from datetime import datetime as dt

from raga.util import config as cfg



log_file_name = cfg.HOME + cfg.path[cfg.LOG] + cfg.filename[cfg.LOG]
logging.basicConfig(filename=log_file_name, filemode='w', level=logging.DEBUG)
logging.info("Program Start")

def log_write (s):
    logging.debug(f'{dt.now().strftime("%d/%m/%Y %H:%M:%S %f")} {s}')


def log_debug (s):
    #log_time = dt.now()
    msg = s # log_time.strftime("%d/%m/%Y %H:%M:%S %f") + "::" + s
    logging.debug (msg)

def log_warning (s):
    #log_time = dt.now()
    msg = s # log_time.strftime("%d/%m/%Y %H:%M:%S %f") + "::" + s
    logging.warning (msg)

def log_debug (s):
    #log_time = dt.now()
    msg = s # log_time.strftime("%d/%m/%Y %H:%M:%S %f") + "::" + s
    logging.debug (msg)

def log_error (s):
    #log_time = dt.now()
    msg = s # log_time.strftime("%d/%m/%Y %H:%M:%S %f") + "::" + s
    logging.error (msg)
