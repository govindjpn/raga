
'''
Filename            : config.py
Path                : util 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Manage the folder configuration of RAGA    
Copyright           : All rights Reserved to KIKU 
'''
import os 


## LATER -- take from Environment Variables 
HOME = "C:\\python\\lib\\raga\\"
DEV_HOME = "C:\\python\\lib\\raga\\"

CHROMA_DB = "chroma_db"
DB = "db"
DOCS = "docs"
IMAGES = "images"
LOG = "log"
MODEL = "model"

path = \
    {CHROMA_DB        : 'docs\\chroma\\',
     DB               : 'db\\',
     DOCS             : 'static\\docs\\',
     IMAGES           : 'config\\',
     LOG              : 'log\\',
     MODEL            : 'config\\',
  }

filename = \
    {CHROMA_DB        : '',
     DB               : 'docs.db',
     DOCS             : '', 
     IMAGES           : 'raga.png',
     LOG              : 'log.txt',
     MODEL            : 'model.csv'
  }


if __name__ == "__main__": 
    
    pass
