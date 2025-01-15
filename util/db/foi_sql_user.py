'''
Filename            : foi_sql_user.py
Path                : util/db
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : user related SQL functions 
Copyright           : All rights Reserved to KIKU 
'''

import foi.util.db.foi_sql_basic as sql 
import bcrypt 

def sql_add_user(user_id, user_name, user_password, user_role, user_group, user_external_id) : 
    try : 
        insert_str = "insert into foi_user ('user_id', 'user_name', 'user_password', " + \
            " 'user_role', 'user_group', 'user_external_id', 'user_active_flg' )" + \
            " values ('" + user_id + "','" + user_name + "','" + user_password + "','" + user_role + "','" + \
                         user_group + "','" + user_external_id + "', 'Y' )"
        sql.insert(insert_str)

    except Exception as E : 
        print (f"{E} add_user :: {insert_str}")

def sql_get_user(user_id): 
    select_str = "select user_password, user_name, user_active_flg from foi_user  where user_id = '" + user_id + "'" 
    return sql.get_one(select_str)


def sql_delete_user (user_id) : 
    update_str = "update foi_user set user_active_flg = 'N' where user_id = '" + user_id + "'" 
    sql.update(update_str)

if __name__ == "__main__" : 
    pw = "12345678"
    pwd = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    sql_add_user ("govindjpn@gmail.com", "Govind Rajan", pwd, "ADMIN", "ADMIN", "govindjpn@gmail.com")
    #sql_delete_user ("test_user_001@abc.com")

