'''
Filename            : foi_sql_docs.py
Path                : util/db
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Docs related SQL functions    
Copyright           : All rights Reserved to KIKU 
'''
import bcrypt
import traceback
import json


import raga.util.db.sql_basic as sql 
import raga.util.doc_definition as doc
import raga.util.log as log


def quoted(text) : 
    # triple quotes gets syntax error ::  """even (e.g. "not even a single person")""")
    # changing double quotes to pipe if both quotes are present 
    if "'" in text and '"' in text : 
        return '"' + text.replace('"', "|") + '"'
    if "'" in text : 
        return '"' + text + '"'
    return "'" + text + "'"


def sql_get_doc_id(doc_name): 
    select_str = "select max(doc_id) from foi_doc_detail  where doc_name = '" + doc_name + "'" 
    if (row := sql.get_one(select_str)) is not None :
        return row[0]
    return None


def sql_add_doc(doc_info) : 
    try : 
        insert_str = "insert into foi_doc_detail ('doc_name', 'doc_pathname', 'doc_password', " + \
            " 'doc_type', 'doc_page_count', 'doc_summary', 'doc_active_flg' )" + \
            " values ('" + doc_info.doc_name + "','" + doc_info.doc_pathname + "','" + doc_info.doc_password + "','" + \
                doc_info.doc_type + "'," + str(doc_info.doc_page_count) + ",'" + doc_info.doc_summary + "', 'Y' )"
        sql.insert(insert_str)
        if (doc_id := sql_get_doc_id (doc_info.doc_name)) is None: 
            raise Exception
        insert_str = "insert into foi_doc_access ('user_id', 'doc_id', 'doc_access') " + \
            " values ('" + doc_info.user_id + "', "+ str(doc_id) + ", 'OWNER')"  
        sql.insert(insert_str)
        ## Move outside #LATER# 
        state = "US-NJ"
        sql_add_doc_meta(doc_id, "state", state )

        return doc_id 

    except Exception as E : 
        print (f"{E} add_docs :: {insert_str} ")


def sql_add_doc_chunk(doc_id, chunk_id, chunk ) : 
    try : 
        insert_str = "insert into foi_doc_chunk ('doc_id', 'chunk_id', 'chunk_text') " + \
            " values (" + str(doc_id) + " , " + str(chunk_id) + " , " + quoted(chunk) + " )"
        sql.insert(insert_str)
        return doc_id 

    except Exception as E : 
        print (f"{E} add_doc_chunk :: {insert_str} ")



def sql_add_doc_meta(doc_id, key, value) : 
    try : 
        insert_str = "insert into foi_doc_meta ('doc_id', 'doc_meta_id', 'doc_meta_key', " + \
            " 'doc_meta_value' )" + \
            " values (" + str(doc_id) + ", 1, '" + key + "', '" + value + "' )"
        sql.insert(insert_str)
        return doc_id 

    except Exception as E : 
        print (f"{E} add_doc_meta :: {insert_str} ")


def sql_update_summary(doc_id, summary ) : 
    try : 
        update_str = "update foi_doc_detail set doc_summary = " + quoted(summary) + " where doc_id = " + str(doc_id) 
        sql.update(update_str)
        return doc_id 

    except Exception as E : 
        print (f"{E} add_doc_chunk :: {update_str} ")

def sql_get_doc_name(doc_id): 
    select_str = "select doc_name from foi_doc_detail  where doc_id = " + str(doc_id)  
    doc_name = sql.get_one(select_str)
    return doc_name[0]

def sql_get_doc_json(doc_id): 
    select_str = "select doc_json from foi_doc_json  where doc_id = " + str(doc_id)  
    doc_json_txt = sql.get_one(select_str)
    doc_json = json.loads(doc_json_txt)
    return doc_json

def sql_get_doc_template(doc_id): 
    select_str = "select doc_template_id from foi_doc_json  where doc_id = " + str(doc_id)  
    doc_template_id = sql.get_one(select_str)[0]
    select_str = "select doc_template_name from foi_doc_template  where doc_template_id = " + str(doc_template_id)  
    doc_template_name = sql.get_one(select_str)[0]
    return doc_template_name


def sql_get_doc_detail(doc_id): 
    select_str = "select doc_name, doc_page_count, doc_type, doc_summary from foi_doc_detail  where doc_id = " + str(doc_id)  
    row = sql.get_one(select_str)
    if row is None :
        log.log_error (f"sql_get_doc_detail : {doc_id} not found")
        return None
    return row

def sql_get_doc_owner(doc_id): 
    select_str = "select user_id from foi_doc_access  where doc_id = " + str(doc_id) + " and doc_access = 'OWNER' " 
    return sql.get_one(select_str)

def sql_get_doc_meta(doc_id): 
    select_str = "select doc_meta_key, doc_meta_value  from foi_doc_meta  where doc_id = " + str(doc_id)   
    if (rows := sql.get_all(select_str)) is None:
        return None
    meta = ""
    for row in rows :  
        meta += f"{row[0]}:{row[1]};" 
    return meta

def sql_get_keyvalue_name(key, value): 
    select_str = "select name from foi_doc_key_values where system = 'foi' and key = '" + key + "' and value = '" + value + "' "  
    return sql.get_one(select_str)

def sql_is_doc_active(doc_id): 
    select_str = "select doc_active_flg from foi_doc_detail  where doc_id = '" + doc_id + "' and doc_access = 'OWNER' " 
    return sql.get_one(select_str)

def sql_delete_doc (doc_id) : 
    update_str = "update foi_docs set docs_active_flg = 'N' where doc_id = '" + doc_id + "'" 
    sql.update(update_str)

def sql_remove_doc (doc_id) : 
    update_str = "delete from foi_docs where docs_id = '" + doc_id + "'" 
    sql.update(update_str)


def sql_get_doc_list(user_id): 
    select_str = "select doc_id from foi_doc_access where user_id = '" + user_id + "'" 
    rows = sql.get_all(select_str)
    if rows is None:
        return None 
    column_names = [ "id", "name","page_count", "doc_type", "owner"]  ## "delete"
    #doc_df = pd.DataFrame(columns=column_names)
    doc_list = []

    for row in rows : 
        doc_detail = sql_get_doc_detail(row[0])
        doc_owner = sql_get_doc_owner(row[0])
        doc_meta = sql_get_doc_meta(row[0])
        row = {"id": row[0], "name": doc_detail[0], "page_count": doc_detail[1], "doc_type": doc_detail[2], 
               "owner": doc_owner[0], "meta": doc_meta
               }   ## , "delete" : 1 if doc_owner[0] == user_id else 0} ## Only the owner can delete 
        # doc_df.loc[len(doc_df)] = row
        doc_list.append(row)
    return doc_list # doc_df 

def sql_get_doc_summary (doc_id : int)  -> str: 
    try : 
        select_str = "select doc_summary from foi_doc_detail  where doc_id = " + str(doc_id)
        row =  sql.get_one(select_str)
        return row[0] if row is not None else ""
    except Exception as E : 
        print (f"sql_get_doc_summary {E} :: {select_str} ")
        traceback.print_exc()
        return None 

if __name__ == "__main__" : 

    pw = "12345678"
    #pwd = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    #sql_add_doc(user_id, doc_name, doc_pathname, doc_password, doc_type, doc_page_count, doc_summary ) : 
    #sql_add_doc ("govindjpn@gmail.com", "Test Doc", "c:\\Python\\lib", pwd, "PDF", 3, "Test")
    #sql_delete_docs ("test_docs_001@abc.com")
    
    print(sql_get_keyvalue_name("state", "US-SC")[0])