
'''
Filename            : config.py
Path                : util/html
Author              : KIKUGO 
Created             : Jan 2025
Purpose             : Manage the labels in multiple languages   
Copyright           : All rights Reserved to KIKU 
'''

import iku.util.db.sql_basic as sql
import iku.util.session as session



TAMIL="ta"
ENGLISH="en"
JAPANESE="ja"

def get_language():
    lang = session.get_value(session.LANGUAGE)
    if lang in [TAMIL, ENGLISH, JAPANESE]:
        return lang
    return ENGLISH

def set_language(lang):
    if lang in [TAMIL, ENGLISH, JAPANESE]:
        session.set_value(session.LANGUAGE, lang)
    else : 
        session.set_value(session.LANGUAGE, ENGLISH) 
    return None

def sql_read_all_labels():
    try :
        select_str = "select * from label_main"
        return sql.get_all(select_str)
    except Exception as e :
        print (f"{e} :: sql_read_all_labels failed {select_str}")
        return None
    
def load_labels():
    if (label_list := sql_read_all_labels()) is None:
        return None
    label_dict = {}
    for label in label_list:   
        label_dict[label[0]]   = (label[1], label[2], label[3])
    return label_dict
    
label_dict = load_labels()

def msg(lang, label, **kwargs):
    if label.upper() in label_dict.keys():        
        label = label.upper()
        match lang:
            case "ta":
                s = label_dict[label][1]
            case "ja":
                s = label_dict[label][2]
            case _:         
                s = label_dict[label][0] #s = en.get(label, **kwargs)
    else :
        s = label
    for k, v in kwargs.items() :
        s = s.replace("{" + k + "}", msg(lang,v)) 
    return s

def lbl(label, **kwargs) :
    lang = get_language()
    return msg(lang, label, **kwargs)

if __name__ == "__main__":
    ## testing 
    #print(msg(TAMIL, "test"))
    #print(msg(TAMIL, "TAMIL"))
    #print(msg(ENGLISH, "TAMIL"))
    #print(msg(JAPANESE, "TAMIL"))
    #print(msg(JAPANESE, "TAMIL"))
    #set_language(TAMIL) - Streamlit session may not be available
    print(msg(TAMIL, "translation completed", source="tamil", target="english"))
    #set_language(ENGLISH)
    print(msg(ENGLISH, "translation completed", source="tamil", target="english"))
    #set_language(JAPANESE)
    print(msg(JAPANESE, "translation completed", source="tamil", target="english"))

class MessageType:
    ERROR="ERROR"
    INFO="INFO"
    WARNING="WARNING"
    SUCCESS="SUCCESS"
